# TODO - LOGIN
# TODO - REGISTRATION
# TODO - CABINET USER
# TODO
# TODO - DATABASE
# TODO
import copy
import datetime

import mariadb
import uuid
import string
from fastapi import FastAPI, applications, Request, HTTPException
from pydantic import ValidationError
import random
from json_actions import parse_doctor_register
from models.actions import ActionUserLogin
from models.user import (UserCreate,
                         UserUpdate,
                         UserClient,
                         UserTherapist,
                         SingleToken,
                         ApproveTime,
                         SelectTime,
                         ReSelectTime,
                         DocRegister,
                         DocScheldure)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware



config = {
    'host': 'localhost',
    # 'host': 'mariadb', # для деплоя с докера
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'testdb'
}

app = FastAPI()

origins = ['http://localhost:3000', 'https://localhost:3000', 'http://127.0.0.1:3000', 'http://0.0.0.0:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

con = mariadb.connect(**config)
cur = con.cursor()
cur.execute("DESCRIBE users")
print(cur)

def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css"
    )

applications.get_swagger_ui_html = swagger_monkey_patch


def db_connection(sql: str):
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()


@app.get("/doc")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json")

@app.get("/")
def root():
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute("DESCRIBE users")
    cur.fetchall()
    cur.close()
    print('123')
    print(cur)
    return {"123": "345"}


@app.get("/test/{item_id}")
def test(item_id: str):
    return {"item_id": item_id}


@app.post("/login")
def login(data: ActionUserLogin):
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
    f = cur.fetchall()
    print(f)
    if f != []:
        print('if1')
        cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}' AND password = '{data.password}';")
        f2 = cur.fetchall()
        print(f2)
        if f2 != []:
            print('if2')
            user_id = f2[0][0]
            print('userid', user_id)
            token = uuid.uuid4()
            cur.execute(f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');")
            con.commit()
            cur.close()
            con.close()
            return {'status': True,
                    'token': token,
                    'error': ''}
        else:
            print('incorrect password')
            print(f2)
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'incorrect email/password'}
    else:
        print('incorrect email')
        cur.close()
        con.close()
        return {'status': False,
                'error': 'incorrect email/password'}


@app.post("/register")
def register(data:UserCreate):
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
    f = cur.fetchall()
    if f == []:
        cur.execute(f"INSERT INTO users (email, password) VALUES ('{data.user_email}', '{data.password}');")
        con.commit()
        cur.close()
        con.close()
        return {'status': True}
    else:
        cur.close()
        con.close()
        return {'status': False,
                'error': 'registration error'}

@app.post('/register_therapist')
# TODO сделать генерацию пользователя
def register_therapist(data: DocRegister):
    try:
        mail = data.doc_email
        password = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)])

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{mail}';")
        f = cur.fetchall()
        if f == []:
            cur.execute(f"INSERT INTO users (email, password) VALUES ('{mail}', '{password}');")
            con.commit()
            cur.close()
            con.close()
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'user_already_registred'}

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(f"SELECT id FROM users WHERE email = '{mail}' AND password = '{password}';")
        f = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        date = datetime.datetime.now()
        token = uuid.uuid4()
        user_id = f[0][0]
        sql = f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');"
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        doc_id = user_id
        columns = 'doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method, doc_method_other, doc_language, doc_edu_additional, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo'
        # data.user_photo = [x.replace("'", '"') for x in data.user_photo]
        # print(data.user_photo)


        # save photos
        photos = ', '.join([f"('{str(x)}')" for x in data.user_photo])
        print(photos)
        if photos:
            sql = f'INSERT INTO images (img) VALUES {photos} RETURNING img_id;'
            print(sql)
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            f = cur.fetchall()
            print('photos added')
            con.commit()
            cur.close()
            con.close()

            photo_ids = ', '.join([str(x[0]) for x in f])
            print(photo_ids)
            data.user_photo = photo_ids
        else:
            data.user_photo = ''

        items = ', '.join([f"'{str(x)}'" for x in data.model_dump().values()])

        sql = f"INSERT INTO doctors ({columns}) VALUES ({doc_id}, {items})"
        print(sql)

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        # take everything back with token
        sql = f'SELECT doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method, doc_method_other, doc_language, doc_edu_additional, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo FROM doctors JOIN tokens ON doctors.doc_id = tokens.user_id WHERE token = "{token}"'

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        print('latest')
        print(f)
        doc_id, doc_photos_ids = f[0][0], f[0][29]
        print(doc_id, doc_photos_ids)

        for i in f:
            print(i)

        if doc_photos_ids:
            sql = f'SELECT img FROM images WHERE img_id IN ({doc_photos_ids})'
            print(sql)

            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            fph = cur.fetchall()
            con.commit()
            cur.close()
            con.close()

            fph = [ph[0] for ph in fph]
        else:
            fph = []

        out = {'status': True,
               'password': f'{password}',
               'token': f'{token}',
               'doc_name': f[0][1],
               'doc_date_of_birth': f[0][2],
               'doc_gender': f[0][3],
               'doc_edu': f[0][4],
               'doc_method': f[0][5],
               'doc_method_other': f[0][6],
               'doc_language': f[0][7],
               'doc_edu_additional': f[0][8],
               'doc_comunity': f[0][9],
               'doc_practice_start': f[0][10],
               'doc_online_experience': f[0][11],
               'doc_customers_amount_current': f[0][12],
               'doc_therapy_length': f[0][13],
               'doc_personal_therapy': f[0][14],
               'doc_supervision': f[0][15],
               'doc_another_job': f[0][16],
               'doc_customers_slots_available': f[0][17],
               'doc_socials_links': f[0][18],
               'doc_citizenship': f[0][19],
               'doc_citizenship_other': f[0][20],
               'doc_ref': f[0][21],
               'doc_ref_other': f[0][22],
               'doc_phone': f[0][23],
               'doc_email': f[0][24],
               'doc_additional_info': f[0][25],
               'doc_question_1': f[0][26],
               'doc_question_2': f[0][27],
               'doc_contact': f[0][28],
               'user_photo': fph}

        print(out)

        return out
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))



@app.post('/get_doc_data')
def get_doc_data(data: SingleToken):
    token = data.session_token
    columns = 'doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method, doc_method_other, doc_language, doc_edu_additional, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo'
    sql = f'SELECT doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method, doc_method_other, doc_language, doc_edu_additional, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo FROM doctors JOIN tokens ON doctors.doc_id = tokens.user_id WHERE token = "{token}"'

    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    doc_id, doc_photos_ids = f[0][0], f[0][29]

    if doc_photos_ids:
        sql = f'SELECT img FROM images WHERE img_id IN ({doc_photos_ids})'
        print(sql)

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        fph = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        fph = [ph[0] for ph in fph]
    else:
        fph = []

    out = {'status': True,
           'doc_name': f[0][1],
           'doc_date_of_birth': f[0][2],
           'doc_gender': f[0][3],
           'doc_edu': f[0][4],
           'doc_method': f[0][5],
           'doc_method_other': f[0][6],
           'doc_language': f[0][7],
           'doc_edu_additional': f[0][8],
           'doc_comunity': f[0][9],
           'doc_practice_start': f[0][10],
           'doc_online_experience': f[0][11],
           'doc_customers_amount_current': f[0][12],
           'doc_therapy_length': f[0][13],
           'doc_personal_therapy': f[0][14],
           'doc_supervision': f[0][15],
           'doc_another_job': f[0][16],
           'doc_customers_slots_available': f[0][17],
           'doc_socials_links': f[0][18],
           'doc_citizenship': f[0][19],
           'doc_citizenship_other': f[0][20],
           'doc_ref': f[0][21],
           'doc_ref_other': f[0][22],
           'doc_phone': f[0][23],
           'doc_email': f[0][24],
           'doc_additional_info': f[0][25],
           'doc_question_1': f[0][26],
           'doc_question_2': f[0][27],
           'doc_contact': f[0][28],
           'user_photo': fph}

    return out

@app.post('/doctor_schedule')
def doctor_schedule(data: DocScheldure):
    # разбираю данные с фронта
    token = data.session_token
    schedule = data.schedule
    timezone = 0
    if data.timezone:
        timezone = data.timezone

    sql = f'SELECT user_id FROM tokens WHERE token = "{token}"'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    cur.close()
    con.close()

    if not f:
        return {'status': False,
                'error': """user not auth-ed"""}
    if f:
        doc_id = f[0][0]

    sh_list = []

    sql = f'DELETE FROM schedule WHERE doctor_id = "{doc_id}" AND client IS NULL'
    print(sql)
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    to_sql = ''
    to_sql_check = ''
    if schedule:
        print(schedule)
        print(type(schedule))
        for item in schedule:
            date_time = datetime.datetime.strptime(item, '%d-%m-%Y %H:%M')
            # date_time = datetime.datetime.strftime(date_time, '%d-%m-%Y %H:%M:%S')
            print(date_time)
            print(type(date_time))
            # if item[1]:
            #     client_id = item[1]
            # else:
            client_id = 'NULL'
            sh_list.append([date_time, client_id])

            if to_sql:
                to_sql = to_sql + f', ({doc_id}, "{date_time}", {client_id})'
                to_sql_check = to_sql + f', ({doc_id}, {date_time})'
            else:
                to_sql = f'({doc_id}, "{date_time}", {client_id})'
                to_sql_check = f'({doc_id}, {client_id})'

    # TODO check

    sql = f'INSERT INTO schedule (doctor_id, date_time, client) values {to_sql}'
    print(sql)
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    sql = f'SELECT date_time, client FROM schedule WHERE doctor_id = {doc_id}'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    fetch = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    print(fetch)

    out = []
    for item in fetch:
        out.append([datetime.datetime.strftime(item[0], '%d-%m-%Y %H:%M'), item[1]])

    # формирую словарик

    return {'status': True, 'schedule': out, 'timezone': timezone}

@app.post('/update_client')
def client_update(data: UserClient):
    return {'status': True}

@app.post('/update_therapist')
def client_update(data: UserTherapist):
    return {'status': True}

@app.post('/get_available_slots')
def get_available_slots(data: SingleToken):
    # sql part

    token = data.session_token

    sql = f'SELECT user_id FROM tokens WHERE token = {token}'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    cur.close()
    con.close()

    if not f:
        return {'status': False,
                'error': """user not auth-ed"""}
    if f:
        doc_id = f

    sql = f'SELECT * FROM schedule WHERE doctor_id = {f}'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    ff = cur.fetchall()
    cur.close()
    con.close()

    sh_dict = {}
    sh_list = []

    for key in ff:
        if key == 'doc_id':
            pass
        else:
            for i, data in ff[key]:
                if data:
                    sh_list.append(f'{key} {i}:00')
            sh_dict[key] = copy.copy(sh_list)

    return {'status': True, 'slots': sh_list}

@app.post('/select_slot')
def select_slot_client(data: SelectTime):
    return {'status': True}

@app.post('/approve_post_therapist')
def approve_post_therapist(data: ApproveTime):
    return {'status': True}

@app.post('/change_slot')
def change_slot(data: ReSelectTime):
    return {'status': True}

@app.get('/refrash')
def refrash_data():
    return {'status': True, 'data': None}