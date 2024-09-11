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
from fastapi import FastAPI, applications, Request
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
    'host': 'mariadb',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'testdb'
}

app = FastAPI()

origins = ["*"]
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
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")

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
            dt = datetime.datetime.now()
            date = str(datetime.datetime.date(dt))
            time = str(datetime.datetime.time(dt))
            cur.execute(f"INSERT INTO tokens (user_id, token, date) VALUES ('{user_id}', '{token}', '{date}');")
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
def register_therapist(data: DocRegister):
    columns = data.keys()
    items = data.items()

    sql = f'INSERT INTO docs ({columns}) VALUES ({items})'

    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    return {'status': True}


# @app.post('/create_schedule_table')
# def create_schedule_table():
#     sql = None

@app.post('/doctor_schedule')
def doctor_schedule(data: DocScheldure):
    # разбираю данные с фронта
    token = data.token
    schedule = data.schedule

    sh_dict = dict(schedule)
    sh_list = []
    sq_dict = {}

    for key in sh_dict:
        for item in sh_dict[key]:
            sh_list.append(item)

    # формирую словарик
    for item in sh_list:
        d = datetime.datetime.strptime(item, '%d.%m.%Y %H:%M')
        day = f'{d.day}-{d.month}-{d.year}'
        if day in sq_dict:
            sq_dict[day][d.hour] = 'vacant'
        else:
            sq_dict[day] = [None] * 24

    # sql part
    sql = f'SELECT id FROM tokens WHERE token = {token}'
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

    # чекаю есть ли в расписании доктор
    sql = f'SELECT * FROM schedule WHERE doc_id = {doc_id}'
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    f = cur.fetchall()
    cur.close()
    con.close()
    # если нет добавляю доктора в расписание
    if not f:
        sql = f'INSERT INTO schedule (doc_id) values ({doc_id})'''
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        cur.close()
        con.close()
        # и заполняю таблицу соответствующими данныем
        for key in sq_dict.keys():
            sql = f'UPDATE schedule SET {key} = {sq_dict[key]} WHERE doc_id = {doc_id}'''
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            f = cur.fetchall()
            cur.close()
            con.close()
    else:
        # и заполняю таблицу соответствующими данныем
        for key in sq_dict.keys():
            sql = f'UPDATE schedule SET {key} = {sq_dict[key]} WHERE doc_id = {doc_id}'''
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            f = cur.fetchall()
            cur.close()
            con.close()


    # timezone = data.timezone

    # print('TOKEN:')
    # print(token)
    print('SCHELDURE:')
    print(sh_dict)
    for k in sh_dict.keys():
        print(k, sh_dict[k])
    # print('TIMEZONE:')
    # print(timezone)
    print(data
    )
    return {'status': True}

@app.post('/update_client')
def client_update(data: UserClient):
    return {'status': True}

@app.post('/update_therapist')
def client_update(data: UserTherapist):
    return {'status': True}

@app.post('/get_available_slots')
def get_available_slots(data: SingleToken):
    # sql part
    sql = f'SELECT id FROM tokens WHERE token = {token}'
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

    sql = f'SELECT * FROM calendar WHERE therapist_id = {f}'
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