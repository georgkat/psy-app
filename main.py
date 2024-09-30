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
                         DocScheldure,
                         ApproveTherapistToken,
                         DocUpdate)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

# EMAIL IMPORTS
from smtplib import SMTP_SSL as smtp
from email.mime.text import MIMEText
# email password = pQ6-c8K-Wph-Z2p
# no_reply password = BPW-XGN-r7g-p8v

config = {
    'host': 'localhost', # для сборки на пеке
    # 'host': '127.0.0.1' # для деплоя в прод
    # 'host': 'mariadb', # для деплоя с докера
    'port': 3306,
    'user': 'root',
    'password': '',
    # 'password': 'Ru3-H84-BPg-WkX'
    'database': 'testdb'
}

app = FastAPI()

origins = ['http://localhost:3000', 'https://localhost:3000', 'http://127.0.0.1:3000', 'http://0.0.0.0:3000', 'http://www.speakyourmind.help/*']
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


def send_email_func(to_addr, sender = '', noreply = True, author = None, password = None, subject = '', content = ''):
    if noreply:
        try:
            password = 'BPW-XGN-r7g-p8v'
            text_subtype = 'plain'
            msg = MIMEText(content, text_subtype)
            msg['Subject'] = subject
            msg['From'] = 'no_reply@speakyourmind.help'  # some SMTP servers will do this automatically, not all
            SMTPserver = ('mail.speakyourmind.help', 465)
            conn = smtp(host='mail.speakyourmind.help', port=465)
            conn.set_debuglevel(False)
            conn.login('no_reply@speakyourmind.help', password)
            try:
                conn.sendmail('no_reply@speakyourmind.help', to_addr, msg.as_string())
            finally:
                conn.quit()
        except:
            raise Exception



@app.get("/doc")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json")

@app.get("/")
def root():
    return {"You should not be here": "!"}


@app.post("/send_email")
def send_email():
    send_email_func(to_addr='georgkat@yandex.ru', subject='OK', content='OK OK OKJ')
    return {'ok': 'ok'}

# DEBUG DELITE
@app.post("/make_admin")
def make_admin():
    email = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)]) + '@' + 'admin.adm'
    password = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)])
    sql = f"INSERT INTO users (email, password, is_therapist, is_admin) VALUES ('{email}', '{password}', 0, 1)"
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    return {"email": email,
            "password": password}


@app.post("/login")
def login(data: ActionUserLogin):
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
    f = cur.fetchall()
    if f != []:
        cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}' AND password = '{data.password}';")
        f2 = cur.fetchall()
        # f2 : 0 user_id 1 email 2 password 3 therapist
        if f2 != []:
            user_id = f2[0][0]
            is_therapist = True if f2[0][3] == 1 else False
            token = uuid.uuid4()
            cur.execute(f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');")
            con.commit()
            cur.close()
            con.close()
            return {'status': True,
                    'token': token,
                    'error': '',
                    'is_therapist': is_therapist}
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'incorrect email/password'}
    else:
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
        is_therapist = 1
        if f == []:
            cur.execute(f"INSERT INTO users (email, password, is_therapist) VALUES ('{mail}', '{password}', {is_therapist});")
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
        columns = 'doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method_other, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo'

        # save photos
        img_data = []
        for item in data.user_photo:
            img_data.append(str((item['data'], item['name'], item['type'])))

        if img_data:
            sql = f'INSERT INTO images (data, name, type) VALUES {", ".join(img_data)} RETURNING img_id;'
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            f = cur.fetchall()
            con.commit()
            cur.close()
            con.close()

            photo_ids = ', '.join([str(x[0]) for x in f])
            data.user_photo = photo_ids
        else:
            data.user_photo = ''

        # doc_edu part
        # doc_edu_list = []
        # for line in data.doc_edu:
        #     doc_edu_list.append((line['year'],
        #                          line['university'],
        #                          line['faculty'],
        #                          line['degree']))

        # method
        # language
        # doc_edu_additional

        additional_columns = []
        additional_items = []
        # DATA doc_method
        if str(data.doc_method):
            for code in data.doc_method:
                additional_columns.append(f'doc_method_{int(code)}')
                additional_items.append('1')
        # DATA doc_language
        if str(data.doc_language):
            for code in data.doc_language:
                additional_columns.append(f'doc_language_{int(code)}')
                additional_items.append('1')
        # DATA doc_edu_additional
        if str(data.doc_edu_additional):
            for code in data.doc_edu_additional:
                additional_columns.append(f'doc_edu_additional_{int(code)}')
                additional_items.append('1')

        additional_columns = ', '.join(additional_columns)
        additional_items = ', '.join(additional_items)

        items = [data.doc_name, data.doc_date_of_birth, data.doc_gender, data.doc_edu, data.doc_method_other, data.doc_comunity, data.doc_practice_start, data.doc_online_experience, data.doc_customers_amount_current, data.doc_therapy_length, data.doc_personal_therapy, data.doc_supervision, data.doc_another_job, data.doc_customers_slots_available, data.doc_socials_links, data.doc_citizenship, data.doc_citizenship_other, data.doc_ref, data.doc_ref_other, data.doc_phone, data.doc_email, data.doc_additional_info, data.doc_question_1, data.doc_question_2, data.doc_contact, data.user_photo]
        items = ', '.join([f'"{str(x)}"' for x in items])

        columns = columns + ', ' + additional_columns
        items = items + ', ' + additional_items

        sql = f"INSERT INTO doctors ({columns}) VALUES ({doc_id}, {items})"

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        # take everything back with token
        sql = (f'SELECT '                           # 0
               f'doc_id, '                          # 0
               f'doc_name, '                        # 1
               f'doc_date_of_birth, '               # 2
               f'doc_gender, '                      # 3
               f'doc_edu, '                         # 4
               f'doc_method_other, '                # 5
               f'doc_comunity, '                    # 6
               f'doc_practice_start, '              # 7
               f'doc_online_experience, '           # 8
               f'doc_customers_amount_current, '    # 9
               f'doc_therapy_length, '              # 10
               f'doc_personal_therapy, '            # 11
               f'doc_supervision, '                 # 12
               f'doc_another_job, '                 # 13
               f'doc_customers_slots_available, '   # 14
               f'doc_socials_links, '               # 15
               f'doc_citizenship, '                 # 16
               f'doc_citizenship_other, '           # 17
               f'doc_ref, '                         # 18
               f'doc_ref_other, '                   # 19
               f'doc_phone, '                       # 20
               f'doc_email, '                       # 21
               f'doc_additional_info, '             # 22
               f'doc_question_1, '                  # 23
               f'doc_question_2, '                  # 24
               f'doc_contact, '                     # 25
               f'user_photo, '                      # 26
               f'doc_method_0, '                    # 27
               f'doc_method_1, '                    # 28
               f'doc_method_2, '                    # 29
               f'doc_method_3, '                    # 30
               f'doc_method_4, '                    # 31
               f'doc_method_5, '                    # 32
               f'doc_method_6, '                    # 33
               f'doc_method_7, '                    # 34
               f'doc_method_8, '                    # 35
               f'doc_method_9, '                    # 36
               f'doc_language_0, '                  # 37
               f'doc_language_1, '                  # 38
               f'doc_language_2, '                  # 39
               f'doc_edu_additional_0, '            # 40
               f'doc_edu_additional_1, '            # 41
               f'doc_edu_additional_2, '            # 42
               f'doc_edu_additional_3, '            # 43
               f'doc_edu_additional_4 '             # 44
               f'FROM doctors JOIN tokens ON doctors.doc_id = tokens.user_id WHERE token = "{token}"')

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        doc_id, doc_photos_ids = f[0][0], f[0][26]
        print(doc_photos_ids)

        if doc_photos_ids:
            sql = f'SELECT data, name, type FROM images WHERE img_id IN ({doc_photos_ids})'

            con = mariadb.connect(**config)
            cur = con.cursor()
            print(sql)
            cur.execute(sql)
            fph = cur.fetchall()
            con.commit()
            cur.close()
            con.close()

            fph = [{'data': ph[0], 'name': ph[1], 'type': ph[2]} for ph in fph]
        else:
            fph = []

        method_edu_language = f[0][27:]
        doc_method = method_edu_language[0:10]
        doc_language = method_edu_language[10:13]
        doc_edu_additional = method_edu_language[13:]

        doc_method_out = []
        for index, x in enumerate(doc_method):
            if x:
                doc_method_out.append(index)

        doc_language_out = []
        for index, x in enumerate(doc_language):
            if x:
                doc_language_out.append(index)

        doc_edu_additional_out = []
        for index, x in enumerate(doc_edu_additional):
            if x:
                doc_edu_additional_out.append(index)

        subj = "Speak your mind password"
        cont = f'''Hello, {data.doc_name}!\nYour first one time password is {password}!\nSincerely yours, SPEAK YOUR MIND team!'''

        send_email_func(to_addr=data.doc_email, subject=subj, content=cont)

        out = {'status': True,
               'password': f'{password}',
               'token': f'{token}',
               'doc_name': f[0][1],
               'doc_date_of_birth': f[0][2],
               'doc_gender': f[0][3],
               'doc_edu': f[0][4],
               'doc_method': doc_method_out,
               #'doc_method_other': f[0][6],
               'doc_language': doc_language_out,
               'doc_edu_additional': doc_edu_additional_out,
               'doc_comunity': f[0][6],
               'doc_practice_start': f[0][7],
               'doc_online_experience': f[0][8],
               'doc_customers_amount_current': f[0][9],
               'doc_therapy_length': f[0][10],
               'doc_personal_therapy': f[0][11],
               'doc_supervision': f[0][25],
               'doc_another_job': f[0][13],
               'doc_customers_slots_available': f[0][14],
               'doc_socials_links': f[0][15],
               'doc_citizenship': f[0][16],
               'doc_citizenship_other': f[0][17],
               'doc_ref': f[0][18],
               'doc_ref_other': f[0][19],
               'doc_phone': f[0][20],
               'doc_email': f[0][21],
               'doc_additional_info': f[0][22],
               'doc_question_1': f[0][23],
               'doc_question_2': f[0][24],
               'doc_contact': f[0][25],
               'user_photo': fph}

        return out
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))



@app.post('/get_doc_data')
def get_docf_data(data: SingleToken):
    token = data.session_token
    sql = (f'SELECT '
           f'doc_id, '
           f'doc_name, '
           f'doc_date_of_birth, '
           f'doc_gender, '
           f'doc_edu, '
           f'doc_method, '
           f'doc_method_other, '
           f'doc_language, '
           f'doc_edu_additional, '
           f'doc_comunity, '
           f'doc_practice_start, '
           f'doc_online_experience, '
           f'doc_customers_amount_current, '
           f'doc_therapy_length, '
           f'doc_personal_therapy, '
           f'doc_supervision, '
           f'doc_another_job, '
           f'doc_customers_slots_available, '
           f'doc_socials_links, '
           f'doc_citizenship, '
           f'doc_citizenship_other, '
           f'doc_ref, '
           f'doc_ref_other, '
           f'doc_phone, '
           f'doc_email, '
           f'doc_additional_info, '
           f'doc_question_1, '
           f'doc_question_2, '
           f'doc_contact, '
           f'user_photo, '
           f'doc_method_0, '
           f'doc_method_1, '
           f'doc_method_2, '
           f'doc_method_3, '
           f'doc_method_4, '
           f'doc_method_5, '
           f'doc_method_6, '
           f'doc_method_7, '
           f'doc_method_8, '
           f'doc_method_9, '
           f'doc_language_0, '
           f'doc_language_1, '
           f'doc_language_2, '
           f'doc_edu_additional_0, '
           f'doc_edu_additional_1, '
           f'doc_edu_additional_2, '
           f'doc_edu_additional_3, '
           f'doc_edu_additional_4 '
           f'FROM doctors JOIN tokens ON doctors.doc_id = tokens.user_id WHERE token = "{token}"')

    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    doc_id, doc_photos_ids = f[0][0], f[0][29]

    if doc_photos_ids:
        sql = f'SELECT data, name, type FROM images WHERE img_id IN ({doc_photos_ids})'

        con = mariadb.connect(**config)
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        fph = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        fph = [{'data': ph[0], 'name': ph[1], 'type': ph[2]} for ph in fph]
    else:
        fph = []

    method_edu_language = f[0][30:]
    doc_method = method_edu_language[0:10]
    doc_language = method_edu_language[10:13]
    doc_edu_additional = method_edu_language[13:]

    doc_method_out = []
    for index, x in enumerate(doc_method):
        if x:
            doc_method_out.append(index)

    doc_language_out = []
    for index, x in enumerate(doc_language):
        if x:
            doc_language_out.append(index)

    doc_edu_additional_out = []
    for index, x in enumerate(doc_edu_additional):
        if x:
            doc_edu_additional_out.append(index)

    out = {'status': True,
           'doc_name': f[0][1],
           'doc_date_of_birth': f[0][2],
           'doc_gender': f[0][3],
           'doc_edu': f[0][4],
           'doc_method': doc_method_out,
           # 'doc_method_other': f[0][6],
           'doc_language': doc_language_out,
           'doc_edu_additional': doc_edu_additional_out,
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
    # TODO Возврат timezone
    if not data.schedule:
        sql = f'SELECT date_time, client FROM schedule WHERE doctor_id = {doc_id}'
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        fetch = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        out = []
        for item in fetch:
            out.append(datetime.datetime.strftime(item[0], '%d-%m-%Y %H:%M'))

        # формирую словарик

        return {'status': True, 'schedule': out, 'timezone': timezone}


    sh_list = []

    sql = f'DELETE FROM schedule WHERE doctor_id = "{doc_id}" AND client IS NULL'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    to_sql = ''
    to_sql_check = ''
    if schedule:
        for item in schedule:
            date_time = datetime.datetime.strptime(item, '%d-%m-%Y %H:%M')
            # date_time = datetime.datetime.strftime(date_time, '%d-%m-%Y %H:%M:%S')
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

    out = []
    for item in fetch:
        out.append(datetime.datetime.strftime(item[0], '%d-%m-%Y %H:%M'))

    # формирую словарик

    return {'status': True, 'schedule': out, 'timezone': timezone}


@app.post('/update_client')
def client_update(data: UserClient):
    return {'status': True}

@app.post('/update_therapist')
def client_update(data: DocUpdate):
    token = data.session_token

    sql = f'SELECT user_id FROM tokens WHERE token = "{token}"'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    fetch = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    doc_id = fetch[0][0]

    additional_columns = []
    additional_items = []

    symptoms_columns = []
    symptoms_items = []
    # DATA doc_method
    if str(data.doc_method):
        for code in data.doc_method:
            additional_columns.append(f'doc_method_{int(code)}')
            additional_items.append('1')
    # DATA doc_language
    if str(data.doc_language):
        for code in data.doc_language:
            additional_columns.append(f'doc_language_{int(code)}')
            additional_items.append('1')

    if str(data.symptoms):
        for code in data.symptoms:
            symptoms_columns.append(f's_{int(code)}')
            symptoms_items.append('1')

    columns = ['doc_date_of_birth', 'client_age', 'lgbtq', 'therapy_type', 'doc_additional_info']
    columns = columns + additional_columns
    items = [data.doc_date_of_birth, data.client_age, data.lgbtq, data.therapy_type, data.doc_additional_info]
    items = items + additional_items

    set_list = []

    print(columns)
    print(items)
    for i in range(len(columns)):
        set_list.append(f'{columns[i]} = "{items[i]}"')

    set_list = ' ,'.join(set_list)

    sql = f'UPDATE doctors SET {set_list} WHERE doc_id = {doc_id}'
    con = mariadb.connect(**config)
    cur = con.cursor()
    print(sql)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    sql = f'SELECT * FROM symptoms WHERE doc_id = {doc_id}'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    if not f:
        sql = f'INSERT INTO symptoms (doc_id, {", ".join(symptoms_columns)}) VALUES ({doc_id}, {", ".join(symptoms_items)})'
        con = mariadb.connect(**config)
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
        return {'status': True}
    else:
        set_list = []
        for i in range(len(symptoms_columns)):
            set_list.append(f'{symptoms_columns[i]} = "{symptoms_items[i]}"')
        set_list = ', '.join(set_list)
        sql = f'UPDATE symptoms SET {set_list} WHERe doc_id = {doc_id}'
        con = mariadb.connect(**config)
        cur = con.cursor()
        print(sql)
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
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

@app.post('/login_admin')
def login_admin(data: ActionUserLogin):

    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
    f = cur.fetchall()
    if f != []:
        cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}' AND password = '{data.password} AND is_admin = 1';")
        f2 = cur.fetchall()
        # f2 : 0 user_id 1 email 2 password 3 therapist
        if f2 != []:
            user_id = f2[0][0]
            is_therapist = True if f2[0][3] == 1 else False
            token = uuid.uuid4()
            cur.execute(f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');")
            con.commit()
            cur.close()
            con.close()
            return {'status': True,
                    'token': token,
                    'error': '',
                    'is_admin': True}
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'incorrect email/password'}
    else:
        cur.close()
        con.close()
        return {'status': False,
                'error': 'incorrect email/password'}

@app.post('/approve_therapist')
def approve_therapist(data: ApproveTherapistToken):
    token = data.session_token
    doc_id = data.doc_id

    sql = f"SELECT id FROM tokens JOIN users ON users.id = tokens.user_id WHERE token = '{token}' AND users.is_admin = 1"

    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    con.commit()
    cur.close()

    if f:
        sql = f"UPDATE doctors SET approved = 1 WHERE doc_id = {doc_id}"
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()

        return {'status': True}
    return {'status': False,
            'error': 'No such admin, or admin not registred'}


@app.post('/list_therapists')
def list_therapists(data: SingleToken):
    token = data.session_token

    sql = f"SELECT id FROM tokens JOIN users ON users.id = tokens.user_id WHERE token = '{token}' AND users.is_admin = 1"

    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    con.commit()
    cur.close()

    out = []
    if f:
        sql = 'SELECT doc_id, doc_name, doc_gender, email, doc_date_of_birth FROM users JOIN doctors ON doc_id = users.id'
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        con.commit()
        cur.close()
        for row in res:
            out.append({'doc_id': row[0],
                        'doc_name': row[1],
                        'doc_gender': row[2],
                        'email': row[3],
                        'doc_date_of_birth': row[4]})
        return {'status': True,
                'list': out}