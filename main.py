# TODO - LOGIN
# TODO - REGISTRATION
# TODO - CABINET USER
# TODO
# TODO - DATABASE
# TODO
import datetime

import mariadb
import uuid
from fastapi import FastAPI, applications, Request
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
                    'token': token}
        else:
            print('else2')
            print(f2)
            cur.close()
            con.close()
            return {'status': False}
    else:
        print('else0')
        cur.close()
        con.close()
        return {'status': False}


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
        return {'status': False}

@app.post('/register_therapist')
def register_therapist(data: DocRegister):
    print(data)
    return {'status': True}

@app.post('/doctor_schedule')
def doctor_schedule(data: DocScheldure):
    # token = data.token
    schedule = data.schedule

    sh_dict = dict(schedule)
    sh_list = []
    for key in sh_dict:
        for item in sh_dict[key]:
            sh_list.append(item)
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
    return {'status': True, 'slots': ['01.01.2024 20:00', '01.02.2024 21:00', '01.03.2024 22:00']}

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