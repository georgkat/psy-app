# TODO - REGISTRATION
# TODO - CABINET USER
# TODO
# TODO - DATABASE
# TODO
import copy
import datetime
# import stripe_module

import asyncio
import mariadb
import uuid
import string
import traceback # for debug
from fastapi import FastAPI, applications, Request, HTTPException
from pydantic import ValidationError
from operator import sub
from collections import OrderedDict
import random
from json_actions import parse_doctor_register
from models.actions import ActionUserLogin
from models.user import (UserCreate,
                         UserLogin,
                         UserLoginGen,
                         UserUpdate,
                         UserClient,
                         UserMainData,
                         UserRequestData,
                         CancelSession,
                         UserTherapistReview,
                         SingleToken,
                         ApproveTime,
                         SelectTime,
                         ReSelectTime,
                         GetSomeoneData,
                         GetSomeoneDataBatch,
                         CancelTherapy,
                         DocAppoint,
                         DocRegister,
                         DocScheldure,
                         ApproveTherapistToken,
                         AdminReport,
                         DocUpdate,
                         AdminUpdateDoc,
                         CardData,
                         ChargeSomeUser,
                         DBHandler)
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

# EMAIL IMPORTS
from smtplib import SMTP_SSL as smtp
from email.mime.text import MIMEText
# email password = pQ6-c8K-Wph-Z2p
# no_reply password = BPW-XGN-r7g-p8v

config_pc = {
    'host': 'localhost', # для сборки на пеке
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'testdb'
}

config_dock = {
    'host': 'mariadb', # для деплоя с докера
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'testdb'
}

config_serv = {
    'host': '127.0.0.1', # для деплоя в прод
    'port': 3306,
    'user': 'root',
    'password': 'Ru3-H84-BPg-WkX',
    'database': 'testdb'
}

configs = [config_serv, config_dock, config_pc]

# app = FastAPI(ssl_keyfile = "/etc/letsencrypt/live/www.speakyourmind.help/privkey.pem", ssl_certfile = "/etc/letsencrypt/live/www.speakyourmind.help/fullchain.pem")
app = FastAPI()

# origins = ['http://localhost:3000', 'https://localhost:3000', 'http://127.0.0.1:3000', 'http://0.0.0.0:3000', 'http://www.speakyourmind.help/*', 'http://www.speakyourmind.help/']
origins = ['*', 'http://localhost:3000', 'https://localhost:3000', 'http://127.0.0.1:3000', 'http://0.0.0.0:3000', 'http://www.speakyourmind.help/*', 'http://www.speakyourmind.help/']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print('** DB connection config **')
for current_config in configs:
    config = current_config
    try:
        print(f'! Trying {config}')
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute("DESCRIBE users")
        print(f'+ Success!')
        print(f'Using {config}')
        break
    except:
        print('- Fail')
        config = {}
if config == {}:
    print('** DB connection failed **')
cur.close()
con.close()
print('** DB connection config complete **')

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

async def send_email_func(to_addr, sender = '', noreply = True, author = None, password = None, subject = '', content = ''):
    # Попробовать асинх
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
            print('SEND MAIL ERROR')
            # TODO 550 ERROR RETURN
            pass

def mail_to_notify(token, subject, content):
    try:
        sql = f'SELECT email FROM users JOIN tokens ON users.id = tokens.user_id WHERE token = "{token}"'
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        email = cur.fetchall()[0]
        cur.execute(sql)

        send_email_func(to_addr=email, subject=subject, content=content)
    except Exception as e:
        print(e)


def create_session_func(doc_id, client_id, sh_id):
    room_id = uuid.uuid4()

    sql_create_session = f'INSERT INTO sessions (room_id, doc_id, client_id, sh_id) VALUES ("{room_id}", {doc_id}, {client_id}, {sh_id})'

    return {'status': True, 'room_id': room_id}

def format_time(time, timezone: int, to_utc: bool = True):
    if to_utc:
        return time - datetime.timedelta(hours=timezone)
    elif not to_utc:
        return time + datetime.timedelta(hours=timezone)

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


@app.post("/generate_password")
def gen_password(data: UserLoginGen):
    try:
        email = data.user_email
        password = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)])

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_0 = f'SELECT * FROM users WHERE email = "{email}";'
        cur.execute(sql_0)
        fetch = cur.fetchall()
        print(fetch)

        if fetch[0][3] == 1:
            sql_0 = f'SELECT approved FROM doctors JOIN users ON users.id = doctors.doc_id WHERE users.email = "{email}";'
            cur.execute(sql_0)
            fetch_0 = cur.fetchall()
            print(fetch_0)
            if fetch_0[0][0] == 0:
                return {'status': False,
                        'error': f"Therapist not approved"}

        if not fetch:
            cur.close()
            con.close()
            return {'status': False,
                    'error': f"Can't find user with email {email}"}

        sql = f'UPDATE users SET password = "{password}" WHERE email = "{email}";'

        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        content = f'Hello!\n Your new password is {password}'
        asyncio.run(send_email_func(to_addr=f'{email}', subject='SYM New Password', content=content))

        print({"status": True,
               "password": password})

        return {"status": True,
                "password": password}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'/login error: {e} {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'/login error: {e} {traceback.extract_stack()}'}





@app.post("/logout")
def logout(data: SingleToken):
    """
    Logout user/therapist/admin
    """
    token = data.session_token
    sql_0 = f'SELECT email FROM users JOIN tokens ON users.id = tokens.user_id'
    sql = f"DELETE FROM tokens WHERE token = '{token}'"
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql_0)
    email = cur.fetchall()[0]
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    content = 'You have succesfully logged out from speakyourmind.help. Have a nice day!'
    asyncio.run(send_email_func(to_addr=f'{email}', subject='SYM Logout', content=content))

    print({"status": True})
    return {"status": True}


@app.post("/login")
def login(data: ActionUserLogin):
    try:
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
                cur.execute(f'DELETE FROM tokens WHERE user_id = "{user_id}"')
                cur.execute(f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');")
                con.commit()
                cur.close()
                con.close()
                mail_to_notify(token, subject='SYM Login', content='You have successfully logged in!')
                return {'status': True,
                        'token': token,
                        'is_therapist': is_therapist}
            else:
                cur.close()
                con.close()
                return {'status': False,
                        'error': 'login error: incorrect email/password'}
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'login error: incorrect email/password'}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        return {'status': False,
                'error': f'/login error: {e} {traceback.extract_stack()}'}


@app.post("/register")
def register(data:UserCreate):
    # TODO добавить токен
    try:
        if not data.password:
            password = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)])
        else:
            password = data.password
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
        f = cur.fetchall()
        if f == []:
            cur.execute(f"INSERT INTO users (email, password) VALUES ('{data.user_email}', '{password}') RETURNING id;")
            f = cur.fetchall()
            client_id = f[0][0]
            cur.execute(f"INSERT INTO clients (client_id, name) VALUES ('{client_id}', '{data.user_name}');")
            token = uuid.uuid4()
            sql = f"INSERT INTO tokens (user_id, token) VALUES ('{client_id}', '{token}');"
            cur.execute(sql)
            sql = f"INSERT INTO client_languages (client_id) VALUES ('{client_id}');"
            cur.execute(sql)
            sql = f"INSERT INTO client_symptoms (client_id) VALUES ('{client_id}');"
            cur.execute(sql)

            content=f'Hello!\nYou have registred on Speakyourmind.help!\nYour new password is {password}'
            asyncio.run(send_email_func(to_addr=f'{data.user_email}', subject='SYM Registration', content=content))


            con.commit()
            cur.close()
            con.close()

            return {'status': True,
                    'token': f'{token}',
                    'password': password}
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'registration error, user exists'}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print(e)
        return {'status': False,
                'error': f'/register error: {e} {traceback.extract_stack()}'}


@app.post("/get_client_data")
def get_client_data(data: SingleToken):
    try:
        token = data.session_token

        data_cols = ('clients.client_id, '
                     'clients.name, '
                     'user_age, '
                     'user_experience, '
                     'user_type, '
                     'user_therapist_gender, '
                     'user_time, '
                     'user_specific_date_time, '
                     'user_price, '
                     'user_phone, '
                     'email, '
                     'has_therapist, '
                     'user_timezone, '
                     'user_photo, '
                     'card_number ')
        language_list = [f'l_{i}' for i in range(0,3)]
        language_cols = ', '.join(language_list)
        symptoms_list = [f's_{i}' for i in range(0,28)]
        symptoms_cols = ', '.join(symptoms_list)

        sql_1 = (f'SELECT {data_cols}, {language_cols}, {symptoms_cols} '
                 f'FROM clients '
                 f'JOIN tokens ON clients.client_id = tokens.user_id '
                 f'LEFT JOIN client_languages ON clients.client_id = client_languages.client_id '
                 f'LEFT JOIN client_symptoms ON clients.client_id = client_symptoms.client_id '
                 f'LEFT JOIN users ON clients.client_id = users.id '
                 f'LEFT JOIN card_data ON clients.client_id = card_data.user_id '
                 f'WHERE token = "{token}";')

        print(sql_1)
        # '''
        # f'FROM doctors '
        # f'JOIN tokens ON doctors.doc_id = tokens.user_id '
        # f'JOIN methods ON doctors.doc_id = methods.doc_id '
        # f'JOIN languages ON doctors.doc_id = languages.doc_id '
        # f'JOIN educations ON doctors.doc_id = educations.doc_id '
        # f'WHERE token = "{token}"')
        # '''

        con = mariadb.connect(**config)
        cur = con.cursor()


        # try:
        #     ch_sql = '''ALTER TABLE `testdb`.`images` CHANGE COLUMN `data` `data` TEXT NULL DEFAULT NULL ;'''
        #     cur.execute(ch_sql)
        #     con.commit()
        # except:
        #     pass

        cur.execute(sql_1)
        desc = cur.description
        fetch_0 = cur.fetchall()

        timezone = fetch_0[0][12]
        print('timezone')
        print(timezone)
        pre_out = {}
        try:
            for i in range(10, len(fetch_0[0])):
                pre_out[desc[i][0]] = fetch_0[0][i]
        except:
            pass

        pre_user_symptoms = []
        user_symptoms = []
        pre_user_languages = []
        user_languages = []
        if pre_out:
            for item in symptoms_list:
                pre_user_symptoms.append(pre_out[item])
            for item in language_list:
                pre_user_languages.append(pre_out[item])
            for i, x in enumerate(pre_user_symptoms):
                if x:
                    user_symptoms.append(i)
            for i, x in enumerate(pre_user_languages):
                if x:
                    user_languages.append(i)

        out = {}
        if pre_out:
            for i in range(0, 14):
                out[desc[i][0]] = fetch_0[0][i]
            print('out 367')
            print(out)
            print('fetc 0 13')
            print(fetch_0)
            print(fetch_0[0][13])

            photo_check = True
            if fetch_0[0][13] == 'None' or fetch_0[0][13] == None:
                photo_check = False

            if photo_check:
                sql_photo = f'SELECT * FROM images WHERE img_id = {int(fetch_0[0][13])}'
                cur.execute(sql_photo)
                fetch_photo = cur.fetchall()
                print('out_user_photo')
                out["user_photo"] = str(fetch_photo[0][3]) + ';' + str(fetch_photo[0][1].decode())
                print(out["user_photo"])
            else:
                out['user_photo'] = ""
            #except:
            #    out['user_photo'] = ""
            out['user_card_data'] = str(fetch_0[0][14])[12:] if fetch_0[0][14] else ''
            print(out)

            print('382')
        else:
            out['client_id'] = fetch_0[0][0]
            out['name'] = fetch_0[0][1]
            out['email'] = fetch_0[0][10]
            out['user_card_data'] = str(fetch_0[0][14])[12:] if fetch_0[0][14] else ''
            out["user_age"] = None
            out["user_experience"] = None
            out["user_type"] = None
            out["user_therapist_gender"] = None
            out["user_time"] = None
            out["user_specific_date_time"] = None
            out["user_price"] = None
            out["user_phone"] = None
            out["has_therapist"] = None
            out['user_timezone'] = None
            out['user_photo'] = None

        # out['user_photo'] = ""
        out['user_symptoms'] = user_symptoms
        out['user_languages'] = user_languages

        print('402')
        if out["has_therapist"]:
            sql = (f"SELECT doc_name, "
                   f"date_time, "
                   f"pending_change, "
                   f"sh_id, "
                   f"accepted,"
                   f"doc_avatar "
                   f"FROM schedule "
                   f"JOIN doctors ON schedule.doctor_id = doctors.doc_id "
                    f"WHERE doctor_id = {out['has_therapist']} AND client = {out['client_id']}")
            print(sql)
            cur.execute(sql)
            fetch = cur.fetchall()
            if fetch:
                print('out has therapist')
                print(fetch)
                pending = fetch[0][2]
                accepted = fetch[0][4]
                doc_avatar = fetch[0][5]
                if doc_avatar:
                    sql_avatar = f'SELECT data, type FROM images WHERE img_id = {doc_avatar}'
                    print(sql_avatar)
                    cur.execute(sql_avatar)
                    fetch_avatar = cur.fetchall()
                    print('fetch_avatar')
                    avatar = fetch_avatar[0][1] + ';' + fetch_avatar[0][0].decode() if fetch_avatar else None
                    print('avatar')
                else:
                    avatar = None
                old_time = format_time(time=fetch[0][1], timezone=timezone, to_utc=False)
                new_time = format_time(time=fetch[0][1], timezone=timezone, to_utc=False)
                print('old_sh_id')
                old_sh_id = fetch[0][3]
                new_sh_id = None
                if pending:
                    old_sh_id = fetch[0][3]
                    sql_1 = f"SELECT new_sh_id, who_asked, old_sh_id FROM change_schedule WHERE old_sh_id = {old_sh_id} OR new_sh_id = {old_sh_id} "
                    cur.execute(sql_1)
                    fetch_1 = cur.fetchall()
                    print(sql_1)
                    print(fetch_1)
                    new_sh_id = fetch_1[0][0]
                    pending = fetch_1[0][1]
                    sql_1 = f"SELECT date_time FROM schedule WHERE sh_id = {new_sh_id}"
                    cur.execute(sql_1)
                    fetch_2 = cur.fetchall()

                    sql_1 = f"SELECT date_time FROM schedule WHERE sh_id = {fetch_1[0][2]}"
                    cur.execute(sql_1)
                    fetch_3 = cur.fetchall()
                    new_time = format_time(time=fetch_2[0][0], timezone=timezone, to_utc=False)
                    old_time = format_time(time=fetch_3[0][0], timezone=timezone, to_utc=False)
                print(fetch)
                out["has_therapist"] = {'doc_id': out['has_therapist'], 'doc_photo': avatar, 'doc_name': fetch[0][0], 'sh_id': old_sh_id, 'sch_time': old_time, 'pending': pending, 'new_sh_id': new_sh_id, 'new_sch_time': new_time, 'accepted': accepted}
            else:
                print('else')
                sql = f"SELECT doc_name, images.data, images.type FROM doctors LEFT JOIN images ON doctors.doc_avatar = images.img_id WHERE doc_id = {out['has_therapist']}"
                print(sql)
                cur.execute(sql)
                fetch = cur.fetchall()
                avatar = fetch[0][2] + ';' + fetch[0][1].decode() if fetch[0][1] else None
                out["has_therapist"] = {'doc_id': out['has_therapist'], 'doc_name': fetch[0][0], 'doc_photo': avatar, 'sh_id': None,
                                        'sch_time': None, 'pending': None, 'new_sh_id': None,
                                        'new_sch_time': None, 'accepted': None}

        con.commit()
        cur.close()
        con.close()

        return out
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'return_client_data error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'return_client_data error: {e}, {traceback.extract_stack()}'}

@app.post("/update_client_data")
def update_user(data: UserClient):
    try:
    # if True:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_0)
        fetch_0 = cur.fetchall()
        if not fetch_0:
            raise Exception
        client_id = fetch_0[0][0]

        sql_1_cols = 'user_age, user_experience, user_type, user_therapist_gender, user_time, user_specific_date_time, user_price, user_phone, user_photo, user_timezone'
        sql_1_cols_list = sql_1_cols.split(', ')
        sql_1_vals = f'"{data.user_age}", {data.user_experience}, {data.user_type}, {data.user_therapist_gender}, "{data.user_time}", "{data.user_specific_date_time}", {data.user_price}, "{data.user_phone}", NULL, {data.user_timezone}'
        sql_1_vals_list = sql_1_vals.split(', ')
        update_data = []
        for i in range(0, len(sql_1_cols_list)):
            update_data.append(f'{sql_1_cols_list[i]} = {sql_1_vals_list[i]}')
        update_data = ', '.join(update_data)
        sql_1 = f"INSERT clients (client_id, {sql_1_cols}) VALUES ({client_id}, {sql_1_vals}) ON DUPLICATE KEY UPDATE {update_data}"
        print(sql_1)
        cur.execute(sql_1)

        sql_2_cols = [f'l_{i}' for i in range(0, 3)]
        sql_2_vals = ['0', '0', '0']
        if data.user_languages:
            for index in data.user_languages:
                sql_2_vals[index] = '1'
        update_data = []
        for i in range(0, len(sql_2_cols)):
            update_data.append(f'{sql_2_cols[i]} = {sql_2_vals[i]}')
        update_data = ', '.join(update_data)
        sql_2 = f"INSERT INTO client_languages (client_id, {', '.join(sql_2_cols)}) VALUES ({client_id}, {', '.join(sql_2_vals)}) ON DUPLICATE KEY UPDATE {update_data}"
        cur.execute(sql_2)

        sql_3_cols = [f's_{i}' for i in range(0, 29)]
        sql_3_vals = ["0" for i in range(0, 29)]
        print(data.user_symptoms)
        if data.user_symptoms:
            for index in data.user_symptoms:
                sql_3_vals[index] = "1"
        update_data = []
        for i in range(0, len(sql_3_cols)):
            update_data.append(f'{sql_3_cols[i]} = {sql_3_vals[i]}')
        update_data = ', '.join(update_data)
        sql_3 = f"INSERT INTO client_symptoms (client_id, {', '.join(sql_3_cols)}) VALUES ({client_id}, {', '.join(sql_3_vals)}) ON DUPLICATE KEY UPDATE {update_data}"
        cur.execute(sql_3)

        if data.user_photo:
            photo_splitteed = data.user_photo.split(';')
            photo_type = photo_splitteed[0]
            base_64 = photo_splitteed[1]
            sql_4 = f"INSERT INTO images (data, name, type) VALUES ('{base_64}', 'avatar', '{photo_type}') RETURNING img_id"
            cur.execute(sql_4)
            photo_id = cur.fetchall()[0][0]

            sql_5 = f'''UPDATE clients SET user_photo = {photo_id} WHERE client_id = {client_id}'''
            cur.execute(sql_5)
        con.commit()
        cur.close()
        con.close()

        mail_to_notify(token, subject='SYM Update Info', content='You have successfully updated your data!')
        return {'status': True}

    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'update_client error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'update_client error: {e}, {traceback.extract_stack()}'}


@app.post("/user_therapist_cancel_review")
def user_therapist_cancel_review(data: UserTherapistReview):
    try:
        token = data.session_token
        problems = ['0' for i in range(0, 11)]
        for i in data.problems:
            problems[i] = '1'
        more_problems = data.more_problems
        call_me = data.call_me

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        fetch = cur.fetchall()
        client_id = fetch[0][0]
        sql_doc = f'SELECT has_therapist FROM clients WHERE client_id = {client_id}'
        print(sql_doc)
        cur.execute(sql_doc)
        fetch = cur.fetchall()
        doc_id = fetch[0][0]

        problems_list = ', '.join(problems)

        columns_list = 'pr_0, pr_1, pr_2, pr_3, pr_4, pr_5, pr_6, pr_7, pr_8, pr_9, pr_10, more_problems, call_me, doc_id, client_id'

        sql = f"INSERT INTO cancelled_therapies ({columns_list}) VALUES ({problems_list}, '{more_problems}', {call_me}, {doc_id}, {client_id})"
        cur.execute(sql)
        sql_1 = f'UPDATE schedule SET client = NULL, accepted = NULL WHERE client = {client_id} AND doctor_id = {doc_id}'
        cur.execute(sql_1)
        sql_2 = f'UPDATE clients SET has_therapist = NULL WHERE client_id = {client_id} AND has_therapist = {doc_id}'
        cur.execute(sql_2)
        sql_3 = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
        cur.execute(sql_3)
        con.commit()
        cur.close()
        con.close()

        mail_to_notify(token, subject='SYM therapy cancelled', content='You have canceled therapy session!')

        return {'status': True}

    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'user_therpist_cancel_review error: {e}, {traceback.extract_stack()}'})

        return {'status': False,
                'error': f'user_therpist_cancel_review error: {e}, {traceback.extract_stack()}'}

@app.post("/update_client_main_data")
def update_user_main(data: UserMainData):
    try:
        token = data.session_token
        name = data.name
        email = data.email
        user_languages = data.user_languages
        user_timezone = data.user_timezone

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        fetch = cur.fetchall()
        if not fetch:
            raise Exception
        client_id = fetch[0][0]

        if email:
            sql_0 = f"UPDATE users SET email = '{email}' WHERE id = {client_id}"
            cur.execute(sql_0)
        if name:
            sql_1 = f"UPDATE clients SET name = '{name}' WHERE client_id = {client_id}"
            cur.execute(sql_1)
        if user_languages:
            languages = [0, 0, 0]
            for i in user_languages:
                languages[i] = 1
            sql_2 = f"UPDATE client_languages SET l_0 = {languages[0]}, l_1 = {languages[1]}, l_2 = {languages[2]} WHERE client_id = {client_id}"
            cur.execute(sql_2)
        if user_timezone:
            sql_3 = f"UPDATE clients SET user_timezone = {user_timezone} WHERE client_id = {client_id}"
            cur.execute(sql_3)
        if data.user_photo:
            photo_splitteed = data.user_photo.split(';')
            photo_type = photo_splitteed[0]
            base_64 = photo_splitteed[1]
            sql_4 = f"INSERT INTO images (data, name, type) VALUES ('{base_64}', 'avatar', '{photo_type}') RETURNING img_id"
            print(sql_4)
            cur.execute(sql_4)
            photo_id = cur.fetchall()[0][0]
            print(photo_id)

            sql_5 = f'''UPDATE clients SET user_photo = {photo_id} WHERE client_id = {client_id}'''
            cur.execute(sql_5)

        con.commit()
        cur.close()
        con.close()

        mail_to_notify(token, subject='SYM update data', content='You have successfully updated your data!')

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'update_client_main_data error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'update_client_main_data error: {e}, {traceback.extract_stack()}'}


@app.post("/update_client_request")
def update_client_request(data: UserRequestData):
    try:
        token = data.session_token
        user_type = data.user_type
        user_symptoms = data.user_symptoms
        user_therapist_gender = data.user_therapist_gender
        user_time = data.user_time
        user_specific_date_time = data.user_specific_date_time
        user_price = data.user_price

        symptoms = ['0' for i in range(0, 28)]
        for i in user_symptoms:
            symptoms[i] = '1'

        symptoms_cols = [f's_{i}' for i in range(0, 28)]

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        fetch = cur.fetchall()
        if not fetch:
            raise Exception
        client_id = fetch[0][0]

        sql_0 = (f"UPDATE clients SET "
                 f"user_type = {user_type}, "
                 f"user_therapist_gender = {user_therapist_gender}, "
                 f"user_time = {user_time}, "
                 f"user_specific_date_time = '{user_specific_date_time}', "
                 f"user_price = {user_price} "
                 f"WHERE client_id = {client_id};")

        sql_symptoms_list = []
        for idx, item in enumerate(symptoms_cols):
            sql_symptoms_list.append(f'{item} = {symptoms[idx]}')
        sql_symptoms_list = ', '.join(sql_symptoms_list)
        sql_1 = f"UPDATE client_symptoms SET {sql_symptoms_list} WHERE client_id = {client_id}"

        cur.execute(sql_0)
        cur.execute(sql_1)

        con.commit()
        cur.close()
        con.close()

        mail_to_notify(token, subject='SYM update request data', content='You have successfully updated your request data!')

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'/update_user_request error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'/update_user_request error: {e}, {traceback.extract_stack()}'}



@app.post("/get_therapist_list")
def get_therapist_list(data: SingleToken):
    # TODO ДОПИЛИТЬ ФИЛЬТРЫ ПО ЯЗЫКУ И ПОЛУ
    try:
        con = mariadb.connect(**config)
        cur = con.cursor()
        token = str(data.session_token)
        sql = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql)
        client_id = cur.fetchall()[0][0]
        symptoms = [f's_{i}' for i in range(0, 28)]
        sql_0 = f'SELECT {", ".join(symptoms)} FROM client_symptoms WHERE client_id = {client_id};'
        print(sql_0)
        cur.execute(sql_0)
        client_symptoms = cur.fetchall()[0]

        sql_0 = f'SELECT clients.user_therapist_gender, clients.user_type, client_languages.l_0, client_languages.l_1, client_languages.l_2 FROM clients JOIN client_languages WHERE clients.client_id = "{client_id}"'
        cur.execute(sql_0)
        fetch = cur.fetchall()
        client_gender_pref = fetch[0][0]
        client_therapy_type = fetch[0][1]
        client_languages = fetch[0][2:]

        sql_1 = f'SELECT doc_symptoms.doc_id, doctors.doc_gender, doctors.doc_therapy_type, languages.l_0, languages.l_1, languages.l_2, {", ".join(symptoms)} FROM doc_symptoms JOIN doctors ON doc_symptoms.doc_id = doctors.doc_id JOIN languages ON doc_symptoms.doc_id = languages.doc_id WHERE doctors.approved = 1'
        cur.execute(sql_1)
        docs = cur.fetchall()

        print(client_symptoms)
        print('docs')
        for doc in docs:
            print(doc)

        valid_docs = {}

        print('sorting')
        print('client_therapy_type')
        print(client_therapy_type)
        for doc_info in docs:
            print(f'CHEKIN DOC {doc_info[0]}')
            doc_gender = doc_info[1]
            doc_therapy_type = doc_info[2]
            doc_langauges = doc_info[3:6]


            print('client_therapy_type')
            print(client_therapy_type)
            print('doc_therapy_type')
            print(doc_therapy_type)

            if client_therapy_type == doc_therapy_type or doc_therapy_type == 2:
                print('we are here')

                # Всрратая лямбда функция умнее в 5 утра не придумал
                print([1 if doc_langauges[x] == client_languages[x] and doc_langauges != 0 else 0 for x in range(len(doc_langauges))])
                if sum([1 if doc_langauges[x] == client_languages[x] and doc_langauges != 0 else 0 for x in range(len(doc_langauges))]) > 0:
                    print('next_step')
                # if client_gender_pref == doc_gender or client_gender_pref == 2:
                    intersections = sum(tuple(map(sub, doc_info[4:], client_symptoms)))
                    print('intersections')
                    print(doc_info[6:])
                    print(client_symptoms)
                    print(intersections)
                    if intersections > 0:
                        valid_docs[doc_info[0]] = intersections
        print('valid_docs')
        print(valid_docs)
        valid_docs = list({k: v for k, v in sorted(valid_docs.items(), key=lambda item: item[1], reverse=True)}.keys())
        #for item in docs:


        valid_docs = [str(x) for x in valid_docs]

        print('GOT VAILID DOCS')
        print(valid_docs)

        if not valid_docs:
            valid_docs = ['0']

        sql_2 = (f'SELECT doctors.doc_id, '
                 f'doctors.doc_name, '
                 f'doctors.doc_additional_info, '
                 f'images.name, '
                 f'images.data, '
                 f'images.type, '
                 f'doctors.doc_practice_start, '
                 f'doctors.doc_therapy_type, '
                 f'doctors.doc_session_cost '
                 f'FROM doctors LEFT JOIN images ON doctors.doc_avatar = images.img_id WHERE doc_id IN ({", ".join(valid_docs)})')
        # sql_photos = f'SELECT doc_id,  '
        print(sql_2)
        cur.execute(sql_2)
        out_docs = cur.fetchall()

        sql_3 = f'SELECT doc_id, year, university, faculty, degree FROM educations_main WHERE doc_id IN ({", ".join(valid_docs)})'
        cur.execute(sql_3)
        out_edu = cur.fetchall()

        edu_dict = {}
        for doc_id in valid_docs:
            edu_dict[int(doc_id)] = []

        for row in out_edu:
            doc_id = row[0]
            year = row[1]
            university = row[2]
            faculty = row[3]
            degree = row[4]
            edu_dict[int(doc_id)].append({'year': year, 'university': university, 'faculty': faculty, 'degree': degree})



        sql_4 = f'SELECT doctor_id, sh_id, date_time FROM schedule WHERE client IS NULL and doctor_id IN ({", ".join(valid_docs)}) AND date_time > NOW()'
        cur.execute(sql_4)
        out_sch = cur.fetchall()

        print('pos 926')

        sh_dict = {}
        for doc_id in valid_docs:
            sh_dict[int(doc_id)] = []

        sql_tz = f'SELECT user_timezone FROM clients WHERE client_id = {client_id}'
        cur.execute(sql_tz)
        timezone = cur.fetchall()[0][0]

        for row in out_sch:
            doc_id = row[0]
            sh_id = row[1]
            date_time = format_time(time=row[2], timezone=timezone, to_utc=False)
            # print(doc_id, sh_id, date_time)
            sh_dict[int(doc_id)].append({'sh_id': sh_id, 'time': date_time})
        for key in sh_dict.keys():
            print(key)
            print(sh_dict[key])

        # print(sh_dict)

        out_docs = [{"doc_id": row[0],
                     "doc_name": row[1],
                     "doc_additional_info": row[2],
                     "doc_practice_start": row[6],
                     "doc_therapy_type": row[7],
                     "doc_session_cost": row[8],
                     "doc_edu": edu_dict[row[0]],
                     "doc_schedule": sh_dict[row[0]],
                     "user_photo": row[5] + ';' + row[4].decode() if row[4] else None} for row in out_docs]

        out_docs_new = []
        for item in out_docs:
            if item['doc_schedule']:
                out_docs_new.append(item)
        cur.close()
        con.close()

        out = {"status": True,
               "list_of_doctors": out_docs_new}
        return out
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'list_therapist for client error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'list_therapist for client error: {e}, {traceback.extract_stack()}'}




@app.post('/register_therapist')
# TODO сделать генерацию пользователя
def register_therapist(data: DocRegister):
    try:
    # if True:
        mail = data.doc_email
        password = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)])
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{mail}';")
        f = cur.fetchall()
        is_therapist = 1
        if f == []:
            cur.execute(f"INSERT INTO users (email, password, is_therapist) VALUES ('{mail}', '{password}', {is_therapist}) RETURNING id;")
            user_id = cur.fetchall()[0][0]
            print(f'WE GOT AN ID {user_id}')
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'register_therapist error: user_already_registred'}

        token = uuid.uuid4()
        sql = f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');"
        cur.execute(sql)

        doc_id = user_id
        columns = 'doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method_other, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo, doc_contact_other, doc_timezone'

        # save photos
        img_data = []

        if data.user_photo:
            for key in data.user_photo:
                if key == 'avatar':
                    name = 'avatar'
                    for item in data.user_photo[key]:
                        photo_splitteed = item.split(';')
                        photo_type = photo_splitteed[0]
                        base_64 = photo_splitteed[1]
                        img_data.append((base_64, name, photo_type))
                else:
                    name = 'document'
                    for item in data.user_photo[key]:
                        photo_splitteed = item.split(';')
                        photo_type = photo_splitteed[0]
                        base_64 = photo_splitteed[1]
                        img_data.append((base_64, name, photo_type))
            print('IMG DATA')
            print(img_data)
            img_data = [str(x) for x in img_data]
            img_data = ', '.join(img_data)
            sql_4 = f"INSERT INTO images (data, name, type) VALUES {img_data} RETURNING img_id"
            # sql_4 = f"INSERT INTO images VALUES {img_data} RETURNING img_id"
            print(sql_4)
            cur.execute(sql_4)
            photo_id = cur.fetchall()
            print('photo_id')
            print(photo_id)
            photo_id = ', '.join([str(x[0]) for x in photo_id])
            data.user_photo = photo_id
            sql_5 = f'''UPDATE doctors SET user_photo = "{photo_id}" WHERE doc_id = {doc_id}'''
            print(sql_5)
            cur.execute(sql_5)

        # raise Exception

        # for item in data.user_photo:
        #     img_data.append(str((item['data'], item['name'], item['type'])))
        print(img_data)
        # if img_data:
        #     sql = f'INSERT INTO images (data, name, type) VALUES {", ".join(img_data)} RETURNING img_id;'
        #     print(sql)
        #     cur.execute(sql)
        #     f = cur.fetchall()
        #     photo_ids = ', '.join([str(x[0]) for x in f])
        #     data.user_photo = photo_ids
        # else:
        #     data.user_photo = ''

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

        sql_method = []
        sql_language = []
        sql_edu = []
        sql_edu_main = []
        sql_method_items = []
        sql_language_items = []
        sql_edu_items = []
        sql_edu_main_items = []

        # DATA doc_method
        if str(data.doc_method):
            for code in data.doc_method:
                sql_method.append(f'm_{int(code)}')
                sql_method_items.append('1')
                print(sql_method)
                print(sql_method_items)
            sql_method = ', '.join([f'{str(x)}' for x in sql_method])
            sql_method_items = ', '.join([f'{str(x)}' for x in sql_method_items])
        # DATA doc_language
        if str(data.doc_language):
            for code in data.doc_language:
                sql_language.append(f'l_{int(code)}')
                sql_language_items.append('1')
            sql_language = ', '.join([f'{str(x)}' for x in sql_language])
            sql_language_items = ', '.join([f'{str(x)}' for x in sql_language_items])
        # DATA doc_edu_additional
        if str(data.doc_edu_additional):
            for code in data.doc_edu_additional:
                sql_edu.append(f'e_{int(code)}')
                sql_edu_items.append('1')
            sql_edu = ', '.join([f'{str(x)}' for x in sql_edu])
            sql_edu_items = ', '.join([f'{str(x)}' for x in sql_edu_items])
        # DATA doc_edu MAIN
        if str(data.doc_edu):
            print(data.doc_edu)
            for line in data.doc_edu:
                print(line)
                sql_edu_main_items.append(f'''({doc_id}, {line['year']}, "{line['university']}", "{line['faculty']}", "{line['degree']}")''')
                print(sql_edu_main_items)
            print(sql_edu_main_items)
            sql_edu_main_items = ', '.join([x for x in sql_edu_main_items])


        items = [data.doc_name, data.doc_date_of_birth, data.doc_gender, data.doc_edu, data.doc_method_other, data.doc_comunity, data.doc_practice_start, data.doc_online_experience, data.doc_customers_amount_current, data.doc_therapy_length, data.doc_personal_therapy, data.doc_supervision, data.doc_another_job, data.doc_customers_slots_available, data.doc_socials_links, data.doc_citizenship, data.doc_citizenship_other, data.doc_ref, data.doc_ref_other, data.doc_phone, data.doc_email, data.doc_additional_info, data.doc_question_1, data.doc_question_2, data.doc_contact, data.user_photo, data.doc_contact_other, data.doc_timezone]
        items = ', '.join([f'"{str(x)}"' for x in items])

        # sql = (f"INSERT INTO doctors ({columns}) VALUES ({doc_id}, {items});")
        # sql = (f"INSERT INTO methods (doc_id, {sql_method}) VALUES ({doc_id}, {sql_method_items});")
        # sql = (f"INSERT INTO languages (doc_id, {sql_language}) VALUES ({doc_id}, {sql_language_items});")
        # sql = (f"INSERT INTO education (doc_id, {sql_edu}) VALUES ({doc_id}, {sql_edu_items});")

        sql = f"INSERT INTO doctors ({columns}) VALUES ({doc_id}, {items});"
        cur.execute(sql)
        sql = f"INSERT INTO methods (doc_id, {sql_method}) VALUES ({doc_id}, {sql_method_items});"
        print(sql)
        cur.execute(sql)
        sql = f"INSERT INTO languages (doc_id, {sql_language}) VALUES ({doc_id}, {sql_language_items});"
        print(sql)
        cur.execute(sql)
        if sql_edu:
            sql = f"INSERT INTO educations (doc_id, {sql_edu}) VALUES ({doc_id}, {sql_edu_items});"
        else:
            sql = f"INSERT INTO educations (doc_id) VALUES ({doc_id});"
        print(sql)
        cur.execute(sql)
        sql = f"INSERT INTO educations_main (doc_id, year, university, faculty, degree) VALUES {sql_edu_main_items};"
        print(sql)
        cur.execute(sql)
        sql = f"INSERT INTO doc_symptoms (doc_id) VALUES ({doc_id});"
        print(sql)
        cur.execute(sql)
        # raise Exception
        con.commit()
        # cur.close()
        # con.close()

        # take everything back with token
        sql = (f'SELECT '
               f'doctors.doc_id, '  # 0
               f'doc_name, '  # 1
               f'doc_date_of_birth, '  # 2
               f'doc_gender, '  # 3
               f'doc_edu, '  # 4
               f'doc_method_other, '  # 5
               f'doc_comunity, '  # 6
               f'doc_practice_start, '  # 7
               f'doc_online_experience, '  # 8
               f'doc_customers_amount_current, '  # 9
               f'doc_therapy_length, '  # 10
               f'doc_personal_therapy, '  # 11
               f'doc_supervision, '  # 12
               f'doc_another_job, '  # 13
               f'doc_customers_slots_available, '  # 14
               f'doc_socials_links, '  # 15
               f'doc_citizenship, '  # 16
               f'doc_citizenship_other, '  # 17
               f'doc_ref, '  # 18
               f'doc_ref_other, '  # 19
               f'doc_phone, '  # 20
               f'doc_email, '  # 21
               f'doc_additional_info, '  # 22
               f'doc_question_1, '  # 23
               f'doc_question_2, '  # 24
               f'doc_contact, '  # 25
               f'user_photo, '  # 26
               f'doc_contact_other, '  # 27
               f'doc_timezone, '  # 28
               f'm_0, '  # 29 0
               f'm_1, '  # 30 1
               f'm_2, '  # 31 2
               f'm_3, '  # 32 3
               f'm_4, '  # 33 4
               f'm_5, '  # 34 5
               f'm_6, '  # 35 6
               f'm_7, '  # 36 7
               f'm_8, '  # 37 8
               f'm_9, '  # 38 9
               f'm_10, '  # 39 10
               f'm_11, '  # 40 11
               f'm_12, '  # 41 12
               f'm_13, '  # 42 13
               f'm_14, '  # 43 14
               f'm_15, '  # 44 15
               f'l_0, '  # 45  16
               f'l_1, '  # 46  17
               f'l_2, '  # 47  18
               f'e_0, '  # 48  19
               f'e_1, '  # 49  20
               f'e_2, '  # 50  21
               f'e_3, '  # 51  22
               f'e_4 '  # 52  23
               f'FROM doctors '
               f'JOIN tokens ON doctors.doc_id = tokens.user_id '
               f'LEFT JOIN methods ON doctors.doc_id = methods.doc_id '
               f'LEFT JOIN languages ON doctors.doc_id = languages.doc_id '
               f'LEFT JOIN educations ON doctors.doc_id = educations.doc_id '
               f'WHERE token = "{token}"')

        # con = mariadb.connect(**config)
        # cur = con.cursor()
        print('TAKE BACK THIS DATA')
        print(sql)
        cur.execute(sql)
        # con.commit()
        # cur.close()
        # con.close()

        f = cur.fetchall()
        doc_id, doc_photos_ids = [0][0], f[0][26]
        print(f[0])
        print(doc_photos_ids)

        if doc_photos_ids:
            sql = f'SELECT data, name, type FROM images WHERE img_id IN ({doc_photos_ids})'
            print(sql)
            cur.execute(sql)
            fph = cur.fetchall()
            print(fph)
            # con.commit()
            # cur.close()
            # con.close()

            fph = [{'data': ph[2] + ';' + ph[0].decode(), 'name': ph[1]} for ph in fph]
        else:
            fph = []

        method_edu_language = f[0][29:]
        doc_method = method_edu_language[0:16]
        doc_language = method_edu_language[16:19]
        doc_edu_additional = method_edu_language[19:]

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

        # DOC EDU MAIN
        print('DOC EDU MAIN')
        # con = mariadb.connect(**config)
        # cur = con.cursor()
        sql = f'SELECT * FROM educations_main WHERE doc_id = {doc_id}'
        cur.execute(sql)
        fetch_edu_main = cur.fetchall()
#        raise Exception
        con.commit()
        cur.close()
        con.close()

        doc_edu = []
        for item in fetch_edu_main:
            doc_edu.append({"year": item[1],
                            "university": item[2],
                            "faculty": item[3],
                            "degree": item[4]})

        subj = "Speak your mind password"
        cont = f'''Hello, {data.doc_name}!\nYour first one time password is {password}!\nSincerely yours, SPEAK YOUR MIND team!'''

        # send_email_func(to_addr=data.doc_email, subject=subj, content=cont)

        out = {'status': True,
               'password': f'{password}',
               'token': f'{token}',
               'doc_name': f[0][1],
               'doc_date_of_birth': f[0][2],
               'doc_gender': f[0][3],
               'doc_edu': doc_edu,
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
               'user_photo': fph,
               'doc_contact_other': f[0][27],
               'doc_timezone': f[0][28]}
        print(out)
        return out
    except ValidationError as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'register_therapist error: validation error, {e}, {traceback.extract_stack()}, ЭТО ЗНАЧИТ С ФРОНТА ПРИШЛО ЧТО-ТО НЕ ТО!'})
        return {'status': False,
                'error': f'register_therapist error: validation error, {e}, {traceback.extract_stack()}, ЭТО ЗНАЧИТ С ФРОНТА ПРИШЛО ЧТО-ТО НЕ ТО!'}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'register_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'register_therapist error: {e}, {traceback.extract_stack()}'}



@app.post('/get_doc_data')
def get_doc_data(data: SingleToken):
    # try:
    if True:
        token = data.session_token
        sql = (f'SELECT '  # 0
               f'doctors.doc_id, '  # 0
               f'doc_name, '  # 1
               f'doc_date_of_birth, '  # 2
               f'doc_gender, '  # 3
               f'doc_edu, '  # 4
               f'doc_method_other, '  # 5
               f'doc_comunity, '  # 6
               f'doc_practice_start, '  # 7
               f'doc_online_experience, '  # 8
               f'doc_customers_amount_current, '  # 9
               f'doc_therapy_length, '  # 10
               f'doc_personal_therapy, '  # 11
               f'doc_supervision, '  # 12
               f'doc_another_job, '  # 13
               f'doc_customers_slots_available, '  # 14
               f'doc_socials_links, '  # 15
               f'doc_citizenship, '  # 16
               f'doc_citizenship_other, '  # 17
               f'doc_ref, '  # 18
               f'doc_ref_other, '  # 19
               f'doc_phone, '  # 20
               f'doc_email, '  # 21
               f'doc_additional_info, '  # 22
               f'doc_question_1, '  # 23
               f'doc_question_2, '  # 24
               f'doc_contact, '  # 25
               f'doc_avatar, '  # 26

               f'm_0, '  # 27 0
               f'm_1, '  # 28 1
               f'm_2, '  # 29 2
               f'm_3, '  # 30 3
               f'm_4, '  # 31 4
               f'm_5, '  # 32 5
               f'm_6, '  # 33 6
               f'm_7, '  # 34 7
               f'm_8, '  # 35 8
               f'm_9, '  # 36 9
               f'm_10, '  # 37 10
               f'm_11, '  # 38 11
               f'm_12, '  # 39 12
               f'm_13, '  # 40 13
               f'm_14, '  # 41 14
               f'm_15, '  # 42 15
               f'l_0, '  # 43  16
               f'l_1, '  # 44  17
               f'l_2, '  # 45  18
               f'e_0, '  # 46  19
               f'e_1, '  # 47  20
               f'e_2, '  # 48  21
               f'e_3, '  # 49  22
               f'e_4, '  # 50  23
               f's_0, '  # 51  24
               f's_1, '  # 52  25
               f's_2, '  # 53  25
               f's_3, '  # 54  25
               f's_4, '  # 55  25
               f's_5, '  # 56  25
               f's_6, '  # 57  25
               f's_7, '  # 58  25
               f's_8, '  # 59  25
               f's_9, '  # 60  25
               f's_10, '  # 61  26
               f's_11, '  # 62  27
               f's_12, '  # 63  28
               f's_13, '  # 64  29
               f's_14, '  # 65  30
               f's_15, '  # 66  31
               f's_16, '  # 67  32
               f's_17, '  # 68  33
               f's_18, '  # 69  34
               f's_19, '  # 70  35
               f's_20, '  # 71  36
               f's_21, '  # 72  37
               f's_22, '  # 73  38
               f's_23, '  # 74  39
               f's_24, '  # 75  40
               f's_25, '  # 76  41
               f's_26, '  # 77  42
               f's_27, '  # 78  43
               f's_28, '  # 79  44
               
               f'doc_client_age, '  # 80
               f'doc_lgbtq, '  # 81
               f'doc_therapy_type, '  # 82
               f'doc_contact_other, '  # 83
               f'doc_timezone, '  # 84
               
               f'card_number, ' # 85
               f'approved '
               f'FROM doctors '
               f'JOIN tokens ON doctors.doc_id = tokens.user_id '
               f'JOIN languages ON doctors.doc_id = languages.doc_id '
               f'JOIN methods ON doctors.doc_id = methods.doc_id '
               f'JOIN educations ON doctors.doc_id = educations.doc_id '
               f'JOIN doc_symptoms ON doctors.doc_id = doc_symptoms.doc_id '
               f'LEFT JOIN card_data ON doctors.doc_id = card_data.user_id '
               f'WHERE token = "{token}"')

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        # d = cur.description
        # print('______________________________')
        # for i, x in enumerate(d):
        #     print(f'{i} / {x[0]} / {f[0][i]}')
        # print('______________________________')
        # con.commit()
        # cur.close()
        # con.close()

        doc_id, doc_photos_ids = f[0][0], f[0][26]

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

            fph = [{'data': ph[0].decode(), 'name': ph[1], 'type': ph[2]} for ph in fph]
        else:
            fph = []

        # DOC EDU MAIN
        print('DOC EDU MAIN')
        con = mariadb.connect(**config)
        cur = con.cursor()
        sql = f'SELECT * FROM educations_main WHERE doc_id = {doc_id}'
        cur.execute(sql)
        fetch_edu_main = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        doc_edu = []
        for item in fetch_edu_main:
            doc_edu.append({"year": item[1],
                            "university": item[2],
                            "faculty": item[3],
                            "degree": item[4]})

        print(f)
        method_edu_language_sym = f[0][27:80]
        print(method_edu_language_sym)
        doc_method = method_edu_language_sym[0:16]
        print(doc_method)
        doc_language = method_edu_language_sym[16:19]
        print(doc_language)
        doc_edu_additional = method_edu_language_sym[19:24]
        print(doc_edu_additional)
        doc_symptoms = method_edu_language_sym[24:]
        print(doc_symptoms)

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

        doc_symptoms_out = []
        for index, x in enumerate(doc_symptoms):
            if x:
                doc_symptoms_out.append(index)


        out = {'status': True,
               'doc_name': f[0][1],
               'doc_date_of_birth': f[0][2],
               'doc_gender': f[0][3],
               'doc_edu': doc_edu,
               'doc_method': doc_method_out,
               # 'doc_method_other': f[0][6],
               'doc_language': doc_language_out,
               'doc_edu_additional': doc_edu_additional_out,
               'doc_comunity': f[0][6],
               'doc_practice_start': f[0][7],
               'doc_online_experience': f[0][8],
               'doc_customers_amount_current': f[0][9],
               'doc_therapy_length': f[0][10],
               'doc_personal_therapy': f[0][11],
               'doc_supervision': f[0][12],
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
               'doc_client_age': f[0][80],
               'doc_lgbtq': f[0][81],
               'doc_therapy_type': f[0][82],
               'doc_card_data': str(f[0][85])[12:] if f[0][85] else '',
               'doc_symptoms': doc_symptoms_out,
               'user_photo': fph,
               'doc_contact_other': f[0][83],
               'doc_timezone': f[0][84],
               'approved': f[0][86]
               }
        print(out)
        return out
    # except Exception as e:
    #     print({'status': False,
    #             'error': f'get_doc_data error: {e}, {traceback.extract_stack()}'})
    #     return {'status': False,
    #             'error': f'get_doc_data error: {e}, {traceback.extract_stack()}'}

@app.post('/doctor_schedule')
def doctor_schedule(data: DocScheldure):
    try:
        # разбираю данные с фронта
        print('STARTING doctor_schedule')
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

        if not f:
            cur.close()
            con.close()
            print({'status': False,
                    'error': """doctor_schedule error: user not auth-ed"""})
            return {'status': False,
                    'error': """doctor_schedule error: user not auth-ed"""}
        if f:
            doc_id = f[0][0]
        # TODO Возврат timezone
        sql_tz = f'SELECT doc_timezone FROM doctors WHERE doc_id = {doc_id}'
        cur.execute(sql_tz)
        timezone = cur.fetchall()[0][0]

        if not data.schedule:
            print('not schedule')
            sql = f'SELECT date_time, client, sh_id, clients.name, accepted, pending_change FROM schedule LEFT JOIN clients ON clients.client_id = schedule.client WHERE doctor_id = {doc_id}'
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            fetch = cur.fetchall()

            print('tz')
            print(timezone)
            print(type(timezone))

            out = []
            for item in fetch:
                non_utc_time = format_time(time=item[0], timezone=timezone, to_utc=False)
                item_time = datetime.datetime.strftime(non_utc_time, '%d-%m-%Y %H:%M')
                out_item = {'sh_id': item[2],
                            'date_time': item_time,
                            'client_id': item[1],
                            'client_name': item[3],
                            'accepted': item[4],
                            'pending_change': item[5]}
                out.append(out_item)
                # out.append(datetime.datetime.strftime(item[0], '%d-%m-%Y %H:%M'))

            # формирую словарик
            print({'status': True, 'schedule': out, 'timezone': timezone})
            cur.close()
            con.close()
            return {'status': True, 'schedule': out, 'timezone': timezone}


        sh_list = []

        sql = f'DELETE FROM schedule WHERE doctor_id = "{doc_id}" AND client IS NULL'

        cur.execute(sql)

        to_sql = ''
        to_sql_check = ''
        if schedule:
            print('schedule')
            for item in schedule:
                print(item)
                print(datetime.datetime.strptime(item, '%d-%m-%Y %H:%M'))
                date_time = format_time(time=datetime.datetime.strptime(item, '%d-%m-%Y %H:%M'), timezone=timezone, to_utc=True)
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

        sql = f'INSERT INTO schedule (doctor_id, date_time, client) values {to_sql} ON DUPLICATE KEY UPDATE doctor_id = doctor_id, date_time = date_time'
        print('SQL')
        print(sql)
        cur.execute(sql)
        con.commit()

        sql = f'SELECT date_time, client, sh_id, clients.name, accepted, pending_change FROM schedule LEFT JOIN clients ON clients.client_id = schedule.client WHERE doctor_id = {doc_id} AND pending_change = 0'

        cur.execute(sql)
        fetch = cur.fetchall()

        out = []
        for item in fetch:
            #item_time = datetime.datetime.strptime(item[0], '%d-%m-%Y %H:%M')
            print('tz')
            item_time = format_time(time=item[0], timezone=timezone, to_utc=False)
            out_item = {'sh_id': item[2],
                        'date_time': item_time,
                        'client_id': item[1],
                        'client_name': item[3],
                        'accepted': item[4],
                        'pending_change': item[5]}
            # out_item = {item[2]: datetime.datetime.strftime(item[0], '%d-%m-%Y %H:%M')}
            out.append(out_item)
            # out.append(datetime.datetime.strftime(item[0], '%d-%m-%Y %H:%M'))


        # формирую словарик
        print({'status': True, 'schedule': out, 'timezone': timezone})
        cur.close()
        con.close()
        return {'status': True, 'schedule': out, 'timezone': timezone}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'doctor_schedule error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'doctor_schedule error: {e}, {traceback.extract_stack()}'}



# @app.post('/update_client')
# def client_update(data: UserClient):
#     return {'status': True}

@app.post('/update_therapist')
def update_therapist(data: DocUpdate):
    try:
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

        sql_method = []
        # sql_method_items = []
        sql_language = []
        sql_language_items = []
        sql_edu = []
        sql_edu_items = []
        sql_sympthoms = []
        sql_sympthoms_items = []

        timezone = None
        if data.doc_timezone:
            timezone = data.doc_timezone

        # DATA doc_method
        # if str(data.doc_method):
        #     for code in data.doc_method:
        #         sql_method.append(f'm_{int(code)}')
        #         sql_method_items.append('1')
        #         print(sql_method)
        #         print(sql_method_items)
        #     sql_method = ', '.join([f'{str(x)}' for x in sql_method])
        #     sql_method_items = ', '.join([f'{str(x)}' for x in sql_method_items])
        # DATA doc_language
        if str(data.doc_language):
            for code in data.doc_language:
                sql_language.append(f'l_{int(code)}')
                sql_language_items.append('1')
            sql_language = ', '.join([f'{str(x)}' for x in sql_language])
            sql_language_items = ', '.join([f'{str(x)}' for x in sql_language_items])

        if str(data.symptoms):
            for code in data.symptoms:
                sql_sympthoms.append(f's_{int(code)}')
                sql_sympthoms_items.append('1')

        columns = ['doc_date_of_birth', 'doc_client_age', 'doc_lgbtq', 'doc_therapy_type', 'doc_additional_info']
        items = [data.doc_date_of_birth, data.doc_client_age, data.doc_lgbtq, data.doc_therapy_type, data.doc_additional_info]

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

        if timezone:
            sql = f'UPDATE doctors SET doc_timezone = {timezone} WHERE doc_id = {doc_id};'
            print(sql)
            cur.execute(sql)

        sql = f"DELETE FROM languages WHERE doc_id= {doc_id};"
        cur.execute(sql)
        sql = f"INSERT INTO languages (doc_id, {sql_language}) VALUES ({doc_id}, {sql_language_items});"
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        sql = f'SELECT * FROM doc_symptoms WHERE doc_id = {doc_id}'
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        if not f:
            print(964)
            sql = f'INSERT INTO doc_symptoms (doc_id, {", ".join(sql_sympthoms)}) VALUES ({doc_id}, {", ".join(sql_sympthoms_items)})'
            con = mariadb.connect(**config)
            cur = con.cursor()
            print(sql)
            cur.execute(sql)
            con.commit()
            cur.close()
            con.close()
            print({'status': True})
            return {'status': True}
        else:
            print(doc_id)
            con = mariadb.connect(**config)
            cur = con.cursor()
            sql = f'DELETE FROM doc_symptoms WHERE doc_id = {doc_id}'
            cur.execute(sql)
            if sql_sympthoms_items:
                sql = f'INSERT INTO doc_symptoms (doc_id, {", ".join(sql_sympthoms)}) VALUES ({doc_id}, {", ".join(sql_sympthoms_items)})'
                cur.execute(sql)
            else:
                sql = f'INSERT INTO doc_symptoms (doc_id) VALUES ({doc_id})'
                cur.execute(sql)
            con.commit()
            cur.close()
            con.close()

            mail_to_notify(token, subject='SYM update data', content='You have successfully updated your data!')
            print({'status': True})
            return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'update_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'update_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/get_available_slots')
def get_available_slots(data: SingleToken):
    try:
        # sql part
        token = data.session_token

        sql = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        cur.close()
        con.close()

        if not f:
            print(
                {'status': False,
                 'error': """get_available_slots error: user not auth-ed"""}
            )
            return {'status': False,
                    'error': """get_available_slots error: user not auth-ed"""}
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
        print({'status': True, 'slots': sh_list})
        return {'status': True, 'slots': sh_list}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False, 'error': f'get_available_slots error: {e}, {traceback.extract_stack()}'})
        return {'status': False, 'error': f'get_available_slots error: {e}, {traceback.extract_stack()}'}

@app.post('/select_slot')
def select_slot_client(data: SelectTime):
    token = data.session_token
    sh_id = data.sh_id
    doc_id = data.doc_id

    con = mariadb.connect(**config)
    cur = con.cursor()

    sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
    cur.execute(sql_0)
    client_id = cur.fetchall()[0][0]
    # TODO Сохранение в архив
    sql_1 = f'UPDATE schedule SET client = NULL WHERE client = {client_id} AND doctor_id = {doc_id}'
    print(sql_1)
    cur.execute(sql_1)

    sql_1 = f'UPDATE schedule SET client = {client_id}, accepted = 1 WHERE sh_id = {sh_id} AND doctor_id = {doc_id} AND client IS NULL'
    print(sql_1)
    cur.execute(sql_1)
    sql_2 = f'SELECT date_time FROM schedule WHERE client = {client_id} AND sh_id = {sh_id} AND doctor_id = {doc_id}'
    cur.execute(sql_2)
    try:
        date_time = cur.fetchall()[0][0]
        sql_tz = f'SELECT user_timezone FROM clients WHERE client_id = {client_id}'
        cur.execute(sql_tz)
        timezone = cur.fetchall()[0][0]
        date_time = format_time(time=date_time, timezone=timezone, to_utc=False)

    except:
        date_time = None

    if date_time:
        sql_3 = f'UPDATE clients SET has_therapist = {doc_id} WHERE client_id = {client_id}'
        cur.execute(sql_3)
    else:
        return {"status": False}

    sql_4 = f'SELECT email FROM users WHERE id = {doc_id}'
    cur.execute(sql_4)
    therapist_email = cur.fetchall()[0][0]
    con.commit()
    cur.close()
    con.close()



    mail_to_notify(token, subject='SYM chosen therapy', content='You have successfully chosen therapy time!')
    asyncio.run(send_email_func(to_addr=therapist_email, subject='SYM chosen therapy', content='You have client!'))

    return {"status": True,
            "time": date_time}

    con.commit()
    cur.close()
    con.close()

    return {'status': True}

@app.post('/approve_time_therapist')
def approve_time_therapist(data: ApproveTime):
    try:
        token = data.session_token
        sh_id = data.sh_id

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        print(sql_0)
        cur.execute(sql_0)
        doc_id = cur.fetchall()[0][0]

        if data.approved:
            print('data.approved')
            sql_0 = f'UPDATE schedule SET accepted = 1, pending_change = 0 WHERE sh_id = {sh_id} AND doctor_id = {doc_id}'
            print(sql_0)
            cur.execute(sql_0)
            sql_1 = f'SELECT client FROM schedule WHERE sh_id = "{sh_id}"'
            cur.execute(sql_1)
            fetch_1 = cur.fetchall()
            client_id = fetch_1[0][0]
            sql_2 = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
            print(sql_2)
            cur.execute(sql_2)

            ch_id = None

            try:
                sql_2 = f'SELECT ch_id FROM change_schedule WHERE client_id = {client_id} AND doc_id = {doc_id} AND new_sh_id = {sh_id}'
                print(sql_2)
                cur.execute(sql_2)
                fetch_2 = cur.fetchall()
                ch_id = fetch_2[0][0]
                print(f'ch_id = {ch_id}')
                print('we got ch_id')
            except:
                pass

            if not ch_id:
                ch_id = data.ch_id

            if ch_id:
                print(ch_id)
                sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {ch_id}'
                print(sql)
                cur.execute(sql)
                fetch = cur.fetchall()
                old_sh_id = fetch[0][0]
                print(old_sh_id)
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id}'
                print(sql)
                cur.execute(sql)
                sql = f'DELETE FROM change_schedule WHERE ch_id = {ch_id} OR (doc_id = {doc_id} AND client_id = {client_id})'
                print(sql)
                cur.execute(sql)
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id} OR (doctor_id = {doc_id} AND client = {client_id}) AND accepted = 0'
                print(sql)
                cur.execute(sql)
                sql = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
                print(sql)
                cur.execute(sql)


        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False, 'error': f'approve_time_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False, 'error': f'approve_time_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/approve_time_client')
def approve_time_client(data: ApproveTime):
    try:
        token = data.session_token
        sh_id = data.sh_id

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        print(sql_0)
        cur.execute(sql_0)
        client_id = cur.fetchall()[0][0]

        if data.approved:
            sql = f'SELECT ch_id, new_sh_id FROM change_schedule WHERE old_sh_id = {sh_id} AND who_asked = 2'
            print(sql)
            cur.execute(sql)
            fetch = cur.fetchall()

            ch_id = None
            if fetch:
                ch_id = fetch[0][0]
                sh_id = fetch[0][1]

            sql_0 = f'UPDATE schedule SET accepted = 1, pending_change = 0 WHERE sh_id = {sh_id} AND client = {client_id} AND pending_change = 2'
            print(sql_0)
            cur.execute(sql_0)

            sql_check = f'SELECT accepted FROM schedule WHERE pending_change = 0 AND sh_id = {sh_id} AND client = {client_id}'
            print(sql_check)
            cur.execute(sql_check)
            fetch_check = cur.fetchall()
            print('!!!')
            if not fetch_check:
                return {'status': False, 'error': 'wrong input data, cant find data in DB'}

            sql_1 = f'SELECT doctor_id FROM schedule WHERE sh_id = "{sh_id}"'
            cur.execute(sql_1)
            fetch_1 = cur.fetchall()
            doc_id = fetch_1[0][0]

            try:
                sql_2 = f'SELECT ch_id FROM change_schedule WHERE client_id = {client_id} AND doc_id = {doc_id} AND new_sh_id = {sh_id}'
                print(sql_2)
                cur.execute(sql_2)
                fetch_2 = cur.fetchall()
                ch_id = fetch_2[0][0]
                print(f'ch_id = {ch_id}')
            except:
                pass

            if not ch_id:
                ch_id = data.ch_id

            if ch_id:
                print(ch_id)
                sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {ch_id}'
                cur.execute(sql)
                fetch = cur.fetchall()
                old_sh_id = fetch[0][0]
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id} AND pending_change = 2'
                cur.execute(sql)
                sql = f'DELETE FROM change_schedule WHERE ch_id = {ch_id} AND who_asked = 2'
                cur.execute(sql)
                sql = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
                print(sql)
                cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        mail_to_notify(token, subject='SYM time approved', content='You have approved new therapy time!')

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False, 'error': f'approve_time_client error: {e}, {traceback.extract_stack()}'})
        return {'status': False, 'error': f'approve_time_client error: {e}, {traceback.extract_stack()}'}




@app.post('/login_admin')
def login_admin(data: ActionUserLogin):
    try:
        print(data.user_email)
        print(data.password)

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
        f = cur.fetchall()
        if f != []:
            cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}' AND password = '{data.password}' AND is_admin = 1;")
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
                print({'status': True,
                        'token': token,
                        'is_admin': True})
                return {'status': True,
                        'token': token,
                        'is_admin': True}
            else:
                cur.close()
                con.close()
                print({'status': False,
                        'error': 'login_admin error: incorrect email/password'})
                return {'status': False,
                        'error': 'login_admin error: incorrect email/password'}
        else:
            cur.close()
            con.close()
            print({'status': False,
                    'error': 'login_admin error: incorrect email/password'})
            return {'status': False,
                    'error': 'login_admin error: incorrect email/password'}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'login_admin error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'login_admin error: {e}, {traceback.extract_stack()}'}


@app.post('/report_to_admin')
def send_report_to_admin(data: AdminReport):
    try:
        if data.session_token:
            sql = f"SELECT email FROM tokens JOIN users ON users.id = tokens.user_id WHERE token = '{data.session_token}'"
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            f = cur.fetchall()
            con.commit()
            cur.close()

            if f:
                report_email = f[0][0]
                # report_email = f[0][1]
            else:
                pass
        elif data.user_email:
            report_email = data.user_email
            # report_name = 'None'
        else:
            report_email = 'None'
            # report_name = 'None'

        report_name = data.user_name if data.user_name else "anonymous"
        asyncio.run(
        asyncio.run(send_email_func(to_addr='admin@speakyourmind.help',
                        sender=report_email,
                        noreply=True,
                        author=report_email,
                        subject=data.report_subject + f': {str(datetime.datetime.now().ctime())}',
                        content=f'REPORT FROM {report_name} ({report_email}):\n' + data.report_text)
        ))
        return {"status": True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'report_to_admin error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'report_to_admin error: {e}, {traceback.extract_stack()}'}
@app.post('/approve_therapist')
def approve_therapist(data: ApproveTherapistToken):
    try:
        token = data.session_token
        doc_id = data.doc_id

        sql = f"SELECT id FROM tokens JOIN users ON users.id = tokens.user_id WHERE token = '{token}' AND users.is_admin = 1"
        print(sql)

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        con.commit()
        cur.close()

        if f and not data.deactivate:
            sql = f"UPDATE doctors SET approved = 1 WHERE doc_id = {doc_id}"
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            cur.close()
            print({'status': True})
            return {'status': True}
        elif f and data.deactivate == 1:
            sql = f"UPDATE doctors SET approved = 0 WHERE doc_id = {doc_id}"
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            cur.close()
            print({'status': True})
            return {'status': True}
        print({'status': False,
                'error': 'approve_therapist error: no such admin, or admin not logged in'})
        return {'status': False,
                'error': 'approve_therapist error: no such admin, or admin not logged in'}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'approve_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'approve_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/list_therapists')
def list_therapists(data: SingleToken):
    try:
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
            sql = 'SELECT doc_id, doc_name, doc_gender, email, registred_date, approved FROM users JOIN doctors ON doc_id = users.id'
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
                            'registred_date': row[4],
                            'approved': row[5]})
            print({'status': True,
                    'list': out})
            return {'status': True,
                    'list': out}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'list_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'list_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/list_clients')
def list_clients(data: SingleToken):
    try:
        token = data.session_token

        sql = f"SELECT id FROM tokens JOIN users ON users.id = tokens.user_id WHERE token = '{token}'"# AND users.is_admin = 1"

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()

        out = []
        if f:
            sql = 'SELECT client_id, name, NULL, user_age, email, registred_date FROM users JOIN clients ON clients.client_id = users.id'
            cur.execute(sql)
            res = cur.fetchall()

            for row in res:
                out.append({'client_id': row[0],
                            'name': row[1],
                            'user_age': row[3],
                            'email': row[4],
                            'registred_date': row[5]})
            print({'status': True,
                    'list': out})
            con.commit()
            cur.close()
            return {'status': True,
                    'list': out}
        else:
            return {'status': False}
        con.commit()
        cur.close()

    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
                'error': f'list_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'list_therapist error: {e}, {traceback.extract_stack()}'}




@app.post('/client_change_session_time')
def client_change_session_time(data: ReSelectTime):
    try:
        token = data.session_token
        old_sh_id = data.old_sh_id
        sh_id = data.new_sh_id
        # doc_id = data.doc_id

        con = mariadb.connect(**config)
        cur = con.cursor()



        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_0)
        client_id = cur.fetchall()[0][0]
        print(f'client id = {client_id}')

        sql_1 = f'SELECT has_therapist FROM clients WHERE client_id = {client_id}'
        cur.execute(sql_1)
        doc_id = cur.fetchall()[0][0]

        therapist_email = f'SELECT email FROM users WHERE id = {doc_id}'
        cur.execute(therapist_email)
        therapist_email = cur.fetchall()[0][0]

        # sql_check_accepted = f'SELECT accepted FROM schedule WHERE sh_id = {old_sh_id}'
        # cur.execute(sql_check_accepted)
        # accepted = cur.fetchall()[0][0]

        print(2)
        sql_2 = f'UPDATE schedule SET pending_change = 0, accepted = 0, client = NULL WHERE sh_id = {old_sh_id}'
        cur.execute(sql_2)

        sql_2 = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
        cur.execute(sql_2)

        print(3)
        sql_3 = f'UPDATE schedule SET client = {client_id}, pending_change = 1 WHERE sh_id = {sh_id} AND doctor_id = {doc_id} AND client IS NULL'
        cur.execute(sql_3)

        print(4)
        sql_4 = f'INSERT INTO change_schedule (client_id, doc_id, old_sh_id, new_sh_id, who_asked) VALUES ({client_id}, {doc_id}, {old_sh_id}, {sh_id}, 1)'
        print(sql_4)
        cur.execute(sql_4)

        ch_id = None
        print(5)
        try:
            sql_2 = f'SELECT ch_id FROM change_schedule WHERE client_id = {client_id} AND doc_id = {doc_id} AND new_sh_id = {old_sh_id}'
            cur.execute(sql_2)
            fetch_2 = cur.fetchall()
            ch_id = fetch_2[0][0]
        except:
            pass

        print(4.5)


        if not ch_id:
            ch_id = data.ch_id

        if ch_id:
            print(5)
            sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {ch_id}'
            cur.execute(sql)
            fetch = cur.fetchall()
            old_sh_id = fetch[0][0]
            print(6)
            sql = f'UPDATE schedule SET client = NULL WHERE sh_id = {old_sh_id}'
            cur.execute(sql)
            print(7)
            sql = f'DELETE FROM change_schedule WHERE ch_id = {ch_id}'
            cur.execute(sql)

        mail_to_notify(token, subject='SYM time changed', content='You selected another session slot!')
        asyncio.run(send_email_func(to_addr=therapist_email, subject='SYM therapy time changed', content='Your client changed session time, check SYM to approve'))

        con.commit()
        cur.close()
        con.close()

        return {"status": True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'client_change_session_time error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'client_change_session_time error: {e}, {traceback.extract_stack()}'}


@app.post('/therapist_change_session_time')
def therapist_change_session_time(data: ReSelectTime):
    try:
        token = data.session_token
        old_sh_id = data.old_sh_id
        sh_id = data.new_sh_id
        # doc_id = data.doc_id

        con = mariadb.connect(**config)
        cur = con.cursor()

        print(0)
        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        print(sql_0)
        cur.execute(sql_0)
        doc_id = cur.fetchall()[0][0]

        print(1)
        sql_1 = f'SELECT client FROM schedule WHERE sh_id = {old_sh_id}'
        print(sql_1)
        cur.execute(sql_1)
        client_id = cur.fetchall()[0][0]
        print(client_id)

        print(2)
        sql_2 = f'UPDATE schedule SET pending_change = 2, accepted = 0, client = NULL WHERE sh_id = {old_sh_id}'
        print(sql_2)
        cur.execute(sql_2)

        sql_2 = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
        print(sql_2)
        cur.execute(sql_2)

        print(3)
        sql_3 = f'UPDATE schedule SET client = {client_id}, pending_change = 2 WHERE sh_id = {sh_id} AND doctor_id = {doc_id} AND client IS NULL'
        print(sql_3)
        cur.execute(sql_3)

        print(4)
        sql_4 = f'INSERT INTO change_schedule (client_id, doc_id, old_sh_id, new_sh_id, who_asked) VALUES ({client_id}, {doc_id}, {old_sh_id}, {sh_id}, 2)'
        print(sql_4)
        cur.execute(sql_4)

        ch_id = None

        try:
            sql_2 = f'SELECT ch_id FROM change_schedule WHERE client_id = {client_id} AND doc_id = {doc_id} AND new_sh_id = {old_sh_id}'
            print(sql_2)
            cur.execute(sql_2)
            fetch_2 = cur.fetchall()
            ch_id = fetch_2[0][0]
        except:
            pass

        if not ch_id:
            ch_id = data.ch_id

        if data.ch_id:
            sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {ch_id}'
            cur.execute(sql)
            fetch = cur.fetchall()
            old_sh_id = fetch[0][0]
            sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id}'
            cur.execute(sql)
            sql = f'DELETE FROM change_schedule WHERE ch_id = {ch_id}'
            cur.execute(sql)
            sql = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id} AND doc_id = {doc_id}'
            print(sql_2)
            cur.execute(sql)

        client_email = f'SELECT email FROM users WHERE id = {client_id}'
        cur.execute(client_email)
        client_email = cur.fetchall()[0][0]
        mail_to_notify(token, subject='SYM time changed', content='You selected another session slot!')
        asyncio.run(send_email_func(to_addr=client_email, subject='SYM therapy time changed',
                                    content='Your client changed session time, check SYM to approve'))

        con.commit()
        cur.close()
        con.close()

        return {"status": True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'therapist_change_session_time error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'therapist_change_session_time error: {e}, {traceback.extract_stack()}'}





# @app.post('/change_therapist')
# def change_therapist(data: CancelTherapy):
#     token = data.session_token
#     doc_id = data.doc_id
#
#     sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
#     cur.execute(sql_0)
#     client_id = cur.fetchall()[0][0]
#
#     sql_1 = f'UPDATE schedule SET client = NULL, accepted = NULL WHERE client_id = {client_id} AND doc_id = {doc_id}'
#     cur.execute(sql_1)
#     sql_2 = f'UPDATE clients SET has_therapist = NULL client_id = {client_id} AND has_therapist = {doc_id}'
#     cur.execute(sql_2)
#     cur.commit()
#     cur.close()
#     con.close()
#     return {"status": True}

@app.post('/recieve_sessions_list_for_therapist')
def recieve_sessions_for_therapist(data: SingleToken):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_0)
        doc_id = cur.fetchall()[0][0]

        # client_id, name, date_time, pending_change<
        sql_0 = f'SELECT client_id, name, sh_id, date_time, accepted, pending_change FROM schedule JOIN clients ON clients.client_id = schedule.client WHERE doctor_id = {doc_id} AND pending_change = 0'
        cur.execute(sql_0)
        fetch_0 = cur.fetchall()
        sql_tz = f'SELECT doc_timezone FROM doctors WHERE doc_id = {doc_id}'
        cur.execute(sql_tz)
        timezone = cur.fetchall()[0][0]
        normal_sessions_list = []
        for row in fetch_0:
            out_normal = {}
            out_normal['client_id'] = row[0]
            out_normal['name'] = row[1]
            out_normal['sh_id'] = row[2]
            out_normal['time'] = format_time(time=row[3], timezone=timezone, to_utc=False)
            out_normal['accepted'] = row[4]
            normal_sessions_list.append(out_normal)

        pending_sessions_list = []
        sql_1 = f'SELECT ch_id, ch.client_id, name, old_sh_id, new_sh_id, old_sh.date_time, new_sh.date_time, new_sh.pending_change FROM testdb.change_schedule ch JOIN schedule old_sh ON ch.old_sh_id = old_sh.sh_id JOIN schedule new_sh ON ch.new_sh_id = new_sh.sh_id JOIN clients ON ch.client_id = clients.client_id WHERE ch.doc_id = {doc_id} ORDER BY ch_id DESC;'
        cur.execute(sql_1)
        fetch_1 = cur.fetchall()
        for row in fetch_1:
            out_pending = {}
            out_pending['ch_id'] = row[0]
            out_pending['client_id'] = row[1]
            out_pending['name'] = row[2]
            out_pending['old_sh_id'] = row[3]
            out_pending['new_sh_id'] = row[4]
            out_pending['old_time'] = format_time(time=row[5], timezone=timezone, to_utc=False)
            out_pending['new_time'] = format_time(time=row[6], timezone=timezone, to_utc=False)
            out_pending['pending'] = row[7]

            pending_sessions_list.append(out_pending)

        sql_2 = f'SELECT client_id, clients.name, user_photo, images.data, images.type FROM clients LEFT JOIN images ON clients.user_photo = images.img_id WHERE has_therapist = {doc_id}'
        cur.execute(sql_2)
        fetch_2 = cur.fetchall()
        clients_out = []
        if fetch_2:
            for row in fetch_2:
                client_out = {}
                client_out['client_id'] = row[0]
                client_out['name'] = row[1]
                if row[3]:
                    client_out['avatar'] = row[4] + ';' + row[3].decode()
                else:
                    client_out['avatar'] = None
                clients_out.append(client_out)

        con.commit()
        cur.close()
        con.close()

        return {'status': True,
                'normal_sessions_list': normal_sessions_list,
                'pending_sessions_list': pending_sessions_list,
                'clients_list': clients_out}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'recieve_sessions_list_for_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'recieve_sessions_list_for_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/get_clients_therapist_schedule')
def get_clients_therapist_schedule(data: SingleToken):
    try:
        token = data.session_token
        con = mariadb.connect(**config)
        cur = con.cursor()

        sql = f'SELECT user_id, has_therapist FROM tokens JOIN clients ON tokens.user_id = clients.client_id WHERE token = "{token}"'
        cur.execute(sql)
        fetch = cur.fetchall()
        print(fetch)
        client_id = fetch[0][0]
        doc_id = fetch[0][1]

        if doc_id:
            sql_1 = f'SELECT sh_id, date_time, client, accepted FROM schedule WHERE doctor_id = {doc_id} AND (client IS NULL OR client = {client_id})'
            cur.execute(sql_1)
            fetch = cur.fetchall()
            sql_tz = f'SELECT user_timezone FROM clients WHERE client_id = {client_id}'
            cur.execute(sql_tz)
            timezone = cur.fetchall()[0][0]
            # print(fetch)
            sh_out = []
            for row in fetch:
                # print(row)
                sh_row = {}
                sh_row['sh_id'] = row[0]
                sh_row['date_time'] = format_time(time=row[1], timezone=timezone, to_utc=False)
                sh_row['client'] = row[2] if row[2] else None
                sh_row['accepted'] = row[3] if row[3] else None

                sh_out.append(sh_row)

            return {'status': True,
                    'doctor_id': doc_id,
                    'schedule': sh_out}

            con.commit()
            cur.close()
            con.close()
        else:
            con.commit()
            cur.close()
            con.close()
            return {'status': False, 'error': 'Client have no therapist'}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'get_clients_therapist_schedule error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'get_clients_therapist_schedule error: {e}, {traceback.extract_stack()}'}



@app.post('/get_user_data')
def get_user_data(data: GetSomeoneData):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql = f'SELECT user_id, is_therapist FROM tokens JOIN users ON tokens.user_id = users.id WHERE token = "{token}"'
        cur.execute(sql)

        fetch = cur.fetchall()
        is_therapist = fetch[0][1]

        if is_therapist:
            print('is therapist')
            doc_id = fetch[0][0]
            s = [f's_{i}' for i in range(0, 29)]
            s = ', '.join(s)
            sql = (f'SELECT clients.client_id, '
                   f'clients.name, '
                   f'user_age, '
                   f'NULL, '
                   f'schedule.pending_change, '
                   f'images.data, '
                   f'images.type, '
                   f'{s} '
                   f'FROM clients '
                   f'JOIN schedule ON clients.client_id = schedule.client '
                   f'JOIN client_symptoms ON clients.client_id = client_symptoms.client_id '
                   f'LEFT JOIN images ON clients.user_photo = images.img_id '
                   f'WHERE clients.client_id = {data.user_id} AND schedule.doctor_id = {doc_id}')  # TODO добавить has_therapist = doc_id
            cur.execute(sql)
            fetch = cur.fetchall()

            sql_tz = f'SELECT user_timezone FROM clients WHERE client_id = {data.user_id}'
            cur.execute(sql_tz)
            timezone = cur.fetchall()[0][0]

            if fetch:
                client_id = fetch[0][0]
                client_name = fetch[0][1]
                client_age = fetch[0][2]
                client_photo = fetch[0][6] + ';' + fetch[0][5].decode() if fetch[0][5] else None
                client_sessions_count = fetch[0][3]
                s = fetch[0][8:]
                s_out = []
                for idx, i in enumerate(s):
                    if i != 0:
                        s_out.append(idx)

                pending = fetch[0][4]
                if pending:
                    sql = f'SELECT ch_id, old_sh_id, old_sh.date_time, new_sh_id, new_sh.date_time, who_asked FROM change_schedule JOIN schedule AS old_sh ON change_schedule.old_sh_id = old_sh.sh_id JOIN schedule AS new_sh ON change_schedule.new_sh_id = new_sh.sh_id WHERE change_schedule.client_id = {data.user_id} AND change_schedule.doc_id = {doc_id}'
                    print(sql)
                    cur.execute(sql)
                    fetch_pending = cur.fetchall()
                    sch_data = {}
                    sch_data['pending'] = True
                    sch_data['ch_id'] = fetch_pending[0][0]
                    sch_data['old_sh_id'] = fetch_pending[0][1]
                    sch_data['old_sh_date_time'] = format_time(time=fetch_pending[0][2], timezone=timezone, to_utc=False)
                    sch_data['new_sh_id'] = fetch_pending[0][3]
                    sch_data['new_sh_date_time'] = format_time(time=fetch_pending[0][4], timezone=timezone, to_utc=False)
                    sch_data['who_asked'] = fetch_pending[0][5]
                    sch_data['accepted'] = 0
                else:
                    sql = f'SELECT sh_id, date_time, accepted FROM schedule WHERE client = {data.user_id} AND doctor_id = {doc_id}'
                    print(sql)
                    cur.execute(sql)
                    fetch_normal = cur.fetchall()
                    sch_data = {}
                    sch_data['pending'] = False
                    sch_data['ch_id'] = None
                    sch_data['old_sh_id'] = fetch_normal[0][0]
                    sch_data['old_sh_date_time'] = format_time(time=fetch_normal[0][1], timezone=timezone, to_utc=False)
                    sch_data['new_sh_id'] = None
                    sch_data['new_sh_date_time'] = None
                    sch_data['who_asked'] = None
                    sch_data['accepted'] = fetch_normal[0][2]
            else:
                s = [f's_{i}' for i in range(0, 29)]
                s = ', '.join(s)

                sql = (f'SELECT '
                       f'clients.name, '
                       f'user_age, '
                       f'NULL, '
                       f'images.data, '
                       f'images.type, '
                       f'{s} '
                       f'FROM clients '
                       f'JOIN client_symptoms ON clients.client_id = client_symptoms.client_id '
                       f'LEFT JOIN images ON clients.user_photo = images.img_id '
                       f'WHERE clients.client_id = {data.user_id}')
                cur.execute(sql)
                fetch_others = cur.fetchall()

                s = fetch_others[0][5:]
                print('s')
                s_out = []
                for idx, i in enumerate(s):
                    if i != 0:
                        s_out.append(idx)

                client_id = data.user_id
                client_name = fetch_others[0][0]
                client_age = fetch_others[0][1]
                print('cliph')
                client_photo = fetch_others[0][4] + ';' + fetch_others[0][3].decode() if fetch_others[0][3] else None
                user_age = 0
                sch_data = []

            con.commit()
            cur.close()
            con.close()


            return {'status': True,
                    'client_id': client_id,
                    'name': client_name,
                    'age': client_age,
                    'client_photo': client_photo,
                    'sessions_count': 0,
                    'sch_data': sch_data,
                    'client_symptoms': s_out}

        con.commit()
        cur.close()
        con.close()
        return {'status': False}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'get_user_data error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'get_user_data error: {e}, {traceback.extract_stack()}'}


@app.post('/get_user_data_batch')
def get_user_data_batch(data: GetSomeoneDataBatch):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql = f'SELECT user_id, is_therapist FROM tokens JOIN users ON tokens.user_id = users.id WHERE token = "{token}"'
        cur.execute(sql)

        fetch = cur.fetchall()
        is_therapist = fetch[0][1]

        clients_out = []

        if is_therapist:
            print('is therapist')
            doc_id = fetch[0][0]
            s = [f's_{i}' for i in range(0, 29)]
            s = ', '.join(s)
            clients = str(tuple(data.user_id))
            sql = (f'SELECT clients.client_id, '
                   f'clients.name, '
                   f'user_age, '
                   f'NULL, '
                   f'schedule.pending_change, '
                   f'images.data, '
                   f'images.type, '
                   f'{s} '
                   f'FROM clients '
                   f'JOIN schedule ON clients.client_id = schedule.client '
                   f'JOIN client_symptoms ON clients.client_id = client_symptoms.client_id '
                   f'LEFT JOIN images ON clients.user_photo = images.img_id '
                   f'WHERE clients.client_id IN {clients} AND schedule.doctor_id = {doc_id}')  # TODO добавить has_therapist = doc_id
            print(sql)
            cur.execute(sql)
            fetch = cur.fetchall()

            if fetch:
                # print(fetch)
                for row in range(0, len(fetch)):
                    client_id = fetch[row][0]
                    client_name = fetch[row][1]
                    client_age = fetch[row][2]
                    client_photo = fetch[row][6] + ';' + fetch[row][5].decode() if fetch[row][5] else None
                    client_sessions_count = fetch[row][3]
                    s = fetch[row][8:]
                    s_out = []
                    for idx, i in enumerate(s):
                        if i != 0:
                            s_out.append(idx)

                    pending = fetch[row][4]
                    if pending:
                        sql = f'SELECT ch_id, old_sh_id, old_sh.date_time, new_sh_id, new_sh.date_time, who_asked FROM change_schedule JOIN schedule AS old_sh ON change_schedule.old_sh_id = old_sh.sh_id JOIN schedule AS new_sh ON change_schedule.new_sh_id = new_sh.sh_id WHERE change_schedule.client_id = {client_id} AND change_schedule.doc_id = {doc_id}'
                        print(sql)
                        cur.execute(sql)
                        fetch_pending = cur.fetchall()
                        sch_data = {}
                        sch_data['pending'] = True
                        sch_data['ch_id'] = fetch_pending[0][0]
                        sch_data['old_sh_id'] = fetch_pending[0][1]
                        sch_data['old_sh_date_time'] = fetch_pending[0][2]
                        sch_data['new_sh_id'] = fetch_pending[0][3]
                        sch_data['new_sh_date_time'] = fetch_pending[0][4]
                        sch_data['who_asked'] = fetch_pending[0][5]
                        sch_data['accepted'] = 0
                    else:
                        sql = f'SELECT sh_id, date_time, accepted FROM schedule WHERE client IN {clients} AND doctor_id = {doc_id}'
                        print(sql)
                        cur.execute(sql)
                        fetch_normal = cur.fetchall()
                        for row in range(0, len(fetch_normal)):
                            sch_data = {}
                            sch_data['pending'] = False
                            sch_data['ch_id'] = None
                            sch_data['old_sh_id'] = fetch_normal[row][0]
                            sch_data['old_sh_date_time'] = fetch_normal[row][1]
                            sch_data['new_sh_id'] = None
                            sch_data['new_sh_date_time'] = None
                            sch_data['who_asked'] = None
                            sch_data['accepted'] = fetch_normal[row][2]
                        clients_out.append({'client_id': client_id, 'name': client_name, 'age': client_age, 'client_photo': client_photo, 'sessions_count': 0, 'sch_data': sch_data, 'client_symptoms': s_out})
            else:
                s = [f's_{i}' for i in range(0, 29)]
                s = ', '.join(s)

                sql = (f'SELECT '
                       f'clients.name, '
                       f'user_age, '
                       f'NULL, '
                       f'images.data, '
                       f'images.type, '
                       f'{s} '
                       f'FROM clients '
                       f'JOIN client_symptoms ON clients.client_id = client_symptoms.client_id '
                       f'LEFT JOIN images ON clients.user_photo = images.img_id '
                       f'WHERE clients.client_id = {data.user_id}')
                print(sql)
                cur.execute(sql)
                fetch_others = cur.fetchall()

                s = fetch_others[0][5:]
                print('s')
                s_out = []
                for idx, i in enumerate(s):
                    if i != 0:
                        s_out.append(idx)

                client_id = data.user_id
                client_name = fetch_others[0][0]
                client_age = fetch_others[0][1]
                print('cliph')
                client_photo = fetch_others[0][4] + ';' + fetch_others[0][3].decode() if fetch_others[0][3] else None
                user_age = 0
                sch_data = []
                clients_out.append({'client_id': client_id, 'name': client_name, 'age': client_age, 'client_photo': client_photo, 'sessions_count': 0, 'sch_data': sch_data, 'client_symptoms': s_out})

            con.commit()
            cur.close()
            con.close()


            return {'status': True, 'clients_data': clients_out}
                    # 'client_id': client_id,
                    # 'name': client_name,
                    # 'age': client_age,
                    # 'client_photo': client_photo,
                    # 'sessions_count': 0,
                    # 'sch_data': sch_data,
                    # 'client_symptoms': s_out}

        con.commit()
        cur.close()
        con.close()
        return {'status': False}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'get_user_data_batch error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'get_user_data_batch error: {e}, {traceback.extract_stack()}'}



@app.post('/cancel_session')
def cancel_session(data: CancelSession):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql = f'SELECT user_id, is_therapist FROM tokens JOIN users ON tokens.user_id = users.id WHERE token = "{token}"'
        cur.execute(sql)
        fetch = cur.fetchall()
        user_id = fetch[0][0]
        is_therapist = fetch[0][1]
        print(f'is_therapist {is_therapist}')
        if is_therapist:
            sh_id = data.sh_id
        ch_id = None
        try:
            sh_id = data.sh_id
            sql = f'SELECT old_sh_id, ch_id FROM change_schedule WHERE new_sh_id = {sh_id} OR old_sh_id = {sh_id}'
            print(sql)
            cur.execute(sql)
            fetch = cur.fetchall()
            print(fetch)
            old_sh_id = fetch[0][0]

            ch_id = fetch[0][1]

            sql = f'DELETE FROM change_schedule WHERE ch_id = {ch_id}'
            print(sql)
            cur.execute(sql)
        except:
            pass

        if is_therapist:
            doc_id = user_id

            sql = f'DELETE FROM ongoing_sessions WHERE client_id = (SELECT client FROM schedule WHERE sh_id = {sh_id} AND doctor_id = {doc_id}) AND doc_id = {doc_id}'
            print(sql)
            cur.execute(sql)

            sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {sh_id} AND doctor_id = {doc_id}'
            print(sql)
            cur.execute(sql)

            if ch_id:
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id} AND doctor_id = {doc_id}'
                print(sql)
                cur.execute(sql)

            client_email = f'SELECT email FROM users WHERE (SELECT client FROM schedule WHERE sh_id = {sh_id} AND doctor_id = {doc_id})'
            cur.execute(client_email)
            client_email = cur.fetchall()[0][0]
            mail_to_notify(token, subject='SYM session canceled', content='You canceled session!')
            asyncio.run(send_email_func(to_addr=client_email, subject='SYM therapist cancelled session',
                                        content='Your therapist has changed session!'))

        else:
            client_id = user_id

            sql = f'SELECT ch_id, old_sh_id, new_sh_id FROM change_schedule WHERE client_id = {client_id}'
            print(sql)
            cur.execute(sql)
            fetch = cur.fetchall()
            print(fetch)
            if fetch:
                ch_id  = fetch[0][0]
                old_sh_id = fetch[0][1]
                sh_id = fetch[0][2]

                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id} AND client = {client_id}'
                print(sql)
                cur.execute(sql)
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {sh_id} AND client = {client_id}'
                print(sql)
                cur.execute(sql)
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {old_sh_id} AND client = {client_id}'
                print(sql)
                cur.execute(sql)
                sql = f'DELETE FROM change_schedule WHERE ch_id = {ch_id}'
                print(sql)
                cur.execute(sql)
                sql = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id}'
                print(sql)
                cur.execute(sql)
            else:
                sql = f'SELECT sh_id FROM schedule WHERE client = {client_id}'
                print(sql)
                cur.execute(sql)
                fetch = cur.fetchall()
                sh_id = fetch[0][0]
                sql = f'UPDATE schedule SET client = NULL, accepted = 0, pending_change = 0 WHERE sh_id = {sh_id} AND client = {client_id}'
                print(sql)
                cur.execute(sql)
                sql = f'DELETE FROM ongoing_sessions WHERE client_id = {client_id}'
                print(sql)
                cur.execute(sql)

            # therapist = f'SELECT email FROM users WHERE (SELECT client FROM schedule WHERE sh_id = {sh_id} AND doctor_id = {doc_id})'
            # cur.execute(client_email)
            # client_email = cur.fetchall()[0][0]
            # mail_to_notify(token, subject='SYM session canceled', content='You canceled session!')
            # asyncio.run(send_email_func(to_addr=client_email, subject='SYM therapist cancelled session',
            #                             content='Your therapist has changed session!'))




        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'cancel_session error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'cancel_session error: {e}, {traceback.extract_stack()}'}


@app.post('/admin_get_client')
def admin_get_client(data: GetSomeoneData):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        # NULL iS PHOTO
        sql = f'SELECT client_id, name, user_phone, user_age, NULL, has_therapist, email FROM clients JOIN users ON clients.client_id = users.id WHERE clients.client_id = {data.user_id}'
        cur.execute(sql)
        fetch = cur.fetchall()

        name = fetch[0][1]
        user_phone = fetch[0][2]
        user_age = fetch[0][3]
        user_photo = None
        doc_id = fetch[0][5]
        user_email = fetch[0][6]

        user_card = None
        user_cashflow = None

        # Session_data

        sql = f'SELECT sh_id, date_time, pending_change FROM schedule WHERE client = {data.user_id}'
        cur.execute(sql)
        fetch = cur.fetchall()
        if fetch:
            sh_id = fetch[0][0]
            date_time = fetch[0][1]
            pending_change = fetch[0][2]

            sql_tz = f'SELECT user_timezone FROM clients WHERE client_id = {data.user_id}'
            cur.execute(sql_tz)
            timezone = cur.fetchall()[0][0]

            if pending_change:
                sql = f'SELECT ch_id, old_sh_id, old_sh.date_time, new_sh_id, new_sh.date_time, who_asked FROM change_schedule JOIN schedule AS old_sh ON change_schedule.old_sh_id = old_sh.sh_id JOIN schedule AS new_sh ON change_schedule.new_sh_id = new_sh.sh_id WHERE change_schedule.client_id = {data.user_id}'
                print(sql)
                cur.execute(sql)
                fetch_pending = cur.fetchall()
                sch_data = {}
                sch_data['pending'] = True
                sch_data['ch_id'] = fetch_pending[0][0]
                sch_data['old_sh_id'] = fetch_pending[0][1]
                sch_data['old_sh_date_time'] = format_time(time=fetch_pending[0][2], timezone=timezone, to_utc=False)
                sch_data['new_sh_id'] = fetch_pending[0][3]
                sch_data['new_sh_date_time'] = format_time(time=fetch_pending[0][4], timezone=timezone, to_utc=False)
                sch_data['who_asked'] = fetch_pending[0][5]
                sch_data['accepted'] = 0
            else:
                sql = f'SELECT sh_id, date_time, accepted FROM schedule WHERE client = {data.user_id}'
                print(sql)
                cur.execute(sql)
                fetch_normal = cur.fetchall()
                sch_data = {}
                sch_data['pending'] = False
                sch_data['ch_id'] = None
                sch_data['old_sh_id'] = fetch_normal[0][0]
                sch_data['old_sh_date_time'] = format_time(time=fetch_normal[0][1], timezone=timezone, to_utc=False)
                sch_data['new_sh_id'] = None
                sch_data['new_sh_date_time'] = None
                sch_data['who_asked'] = None
                sch_data['accepted'] = fetch_normal[0][2]

            sql = f'SELECT doc_name FROM doctors WHERE doc_id = {doc_id}'
            print(sql)
            cur.execute(sql)

            con.commit()
            cur.close()
            con.close()


            return {'status': True,
                    'client_id': data.user_id,
                    'name': name,
                    'user_phone': user_phone,
                    'user_age': user_age,
                    'user_photo': None,
                    'user_card': None,
                    'user_cashflow': None,
                    'sch_data': sch_data}
        else:
            return {'status': True,
                    'client_id': data.user_id,
                    'name': name,
                    'user_phone': user_phone,
                    'user_age': user_age,
                    'user_photo': None,
                    'user_card': None,
                    'user_cashflow': None,
                    'sch_data': None}

        con.commit()
        cur.close()
        con.close()
        return {'status': False}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass

        print({'status': False,
               'error': f'admin_get_client error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'admin_get_client error: {e}, {traceback.extract_stack()}'}


@app.post('/admin_get_therapist')
def admin_get_therapist(data: GetSomeoneData):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        # NULL iS PHOTO
        l = ', '.join([f'l_{i}' for i in range(0, 3)])
        s = ', '.join([f's_{i}' for i in range(0, 29)])
        e = ', '.join([f'e_{i}' for i in range(0, 5)])
        m = ', '.join([f'm_{i}' for i in range(0, 17)])
        sql = (f'SELECT doctors.doc_id, doc_name, doc_gender, doc_phone, doc_date_of_birth, doc_practice_start, '
               f'doc_additional_info, doc_client_age, doc_lgbtq, doc_therapy_type, email, user_photo, doc_avatar, doc_session_cost, approved, {l}, {s}, {e}, {m} '
               f'FROM doctors LEFT JOIN languages ON doctors.doc_id = languages.doc_id LEFT JOIN doc_symptoms ON doctors.doc_id = doc_symptoms.doc_id LEFT JOIN educations ON doctors.doc_id = educations.doc_id LEFT JOIN methods ON doctors.doc_id = methods.doc_id LEFT JOIN users ON doctors.doc_id = users.id WHERE doctors.doc_id = {data.user_id}')
        cur.execute(sql)
        fetch = cur.fetchall()
        fetch_cols = cur.description

        di = {}

        for i, item in enumerate(fetch[0]):
            di[fetch_cols[i][0]] = item

        print('di')
        print(di)

        sql_edu = f'SELECT year, university, faculty, degree FROM educations_main WHERE doc_id = {data.user_id}'
        cur.execute(sql_edu)
        fetch_edu = cur.fetchall()

        user_photo = fetch[0][11]
        doc_avatar = fetch[0][12]
        if user_photo:
            sql_photos = f'SELECT * FROM images WHERE img_id IN ({user_photo})'
            print(sql_photos)
            cur.execute(sql_photos)
            fetch_photos = cur.fetchall()
            print(fetch_photos)
            fetch_cols = cur.description
            print(fetch_cols)

            photos = [{'img_id': photo[0], 'data': photo[3] + ';' + photo[1].decode(), 'name': photo[2]} for photo in
                      fetch_photos]
            photo = {'avatar': [],
                     'document': []}

            for item in photos:
                if item['name'] == 'avatar':
                    item.pop('name', None)
                    photo['avatar'].append(item)
                else:
                    item.pop('name', None)
                    photo['document'].append(item)

        else:
            photos = {}
            photo = {}

        doc_name = fetch[0][1]
        doc_gender = fetch[0][2]
        doc_phone = fetch[0][3]
        doc_age = fetch[0][4]
        doc_practice_start = fetch[0][5]
        doc_additional_info = fetch[0][6]
        doc_client_age = fetch[0][7]
        doc_lgbtq = fetch[0][8]
        doc_therapy_type = fetch[0][9]
        doc_email = fetch[0][10]
        doc_session_cost = fetch[0][13]
        doc_photos = photos
        doc_avatar = doc_avatar
        doc_approved = fetch[0][14]

        # doc_photo = None
        doc_grade = None
        doc_card = None
        doc_cashflow = None
        doc_sessions = None

        l = [f'l_{i}' for i in range(0, 3)]
        s = [f's_{i}' for i in range(0, 29)]
        e = [f'e_{i}' for i in range(0, 5)]
        m = [f'm_{i}' for i in range(0, 17)]

        doc_languages = []
        doc_symptoms = []
        doc_additional_educations = []
        doc_methods = []
        for key in di.keys():
            if key in l:
                if di[key] == 1:
                    doc_languages.append(l.index(key))
            elif key in s:
                if di[key] == 1:
                    doc_symptoms.append(s.index(key))
            elif key in e:
                if di[key] == 1:
                    doc_additional_educations.append(e.index(key))
            elif key in m:
                if di[key] == 1:
                    doc_methods.append(m.index(key))

        doc_educations = []
        for row in fetch_edu:
            main_edu = {}
            main_edu['year'] = row[0]
            main_edu['university'] = row[1]
            main_edu['faculty'] = row[2]
            main_edu['degree'] = row[3]
            doc_educations.append(main_edu)

        out = {}
        out['doc_id'] = data.user_id
        out['doc_name'] = doc_name
        out['doc_gender'] = doc_gender
        out['doc_phone'] = doc_phone
        out['doc_date_of_birth'] = doc_age
        out['doc_email'] = doc_email
        out['doc_photo'] = photo
        out['doc_avatar'] = doc_avatar
        out['doc_card'] = doc_card
        out['doc_sessions_count'] = doc_sessions
        out['doc_session_cost'] = doc_grade
        out['doc_payments'] = doc_cashflow
        out['doc_language'] = doc_languages
        out['doc_practice_start'] = doc_practice_start
        out['doc_additional_info'] = doc_additional_info
        out['doc_method'] = doc_methods
        out['doc_client_age'] = doc_client_age
        out['doc_lgbtq'] = doc_lgbtq
        out['doc_therapy_type'] = doc_therapy_type
        out['doc_symptoms'] = doc_symptoms
        out['doc_edu'] = doc_educations
        out['doc_session_cost'] = doc_session_cost
        out['approved'] = doc_approved

        print(out)


        con.commit()
        cur.close()
        con.close()

        out['status'] = True

        return out

    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'admin_get_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'admin_get_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/admin_get_therapist_interview')
def admin_get_therapist_interview(data: GetSomeoneData):
    try:
        token = data.session_token

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql = f'SELECT users.id FROM users JOIN tokens ON users.id = tokens.user_id WHERE is_admin = 1 AND token = "{token}"'
        cur.execute(sql)
        if not cur.fetchall():
            raise Exception

        main_columns = ('doc_name, '
                        'doc_date_of_birth, '
                        'doc_gender, '
                        'doc_edu_additional, '
                        'doc_comunity, '
                        'doc_practice_start, '
                        'doc_online_experience, '
                        'doc_citizenship_other, '
                        'doc_ref, '
                        'doc_ref_other, '
                        'doc_customers_amount_current, '
                        'doc_therapy_length, '
                        'doc_personal_therapy, '
                        'doc_supervision, '
                        'doc_another_job, '
                        'doc_customers_slots_available, '
                        'doc_socials_links, '
                        'doc_citizenship, '
                        'doc_email, '
                        'doc_additional_info, '
                        'doc_question_1, '
                        'doc_question_2, '
                        'doc_contact, '
                        'doc_client_age, '
                        'doc_lgbtq, '
                        'doc_therapy_type, '
                        'doc_phone, '
                        'approved, '
                        'doc_session_cost, '
                        'doc_timezone, '
                        'doc_contact_other')
        l = [f'l_{i}' for i in range(0, 3)]
        s = [f's_{i}' for i in range(0, 29)]
        e = [f'e_{i}' for i in range(0, 5)]
        m = [f'm_{i}' for i in range(0, 17)]

        sql = (f'SELECT {main_columns}, {", ".join(l)}, {", ".join(s)}, {", ".join(e)}, {", ".join(m)} '
               f'FROM doctors LEFT JOIN languages ON doctors.doc_id = languages.doc_id '
               f'LEFT JOIN doc_symptoms ON doctors.doc_id = doc_symptoms.doc_id '
               f'LEFT JOIN educations ON doctors.doc_id = educations.doc_id '
               f'LEFT JOIN methods ON doctors.doc_id = methods.doc_id '
               f'LEFT JOIN users ON doctors.doc_id = users.id '
               f'WHERE doctors.doc_id = {data.user_id}')

        cur.execute(sql)
        fetch = cur.fetchall()
        fetch_cols = cur.description

        di = {}

        for i, item in enumerate(fetch[0]):
            di[fetch_cols[i][0]] = item

        sql_edu = f'SELECT year, university, faculty, degree FROM educations_main WHERE doc_id = {data.user_id}'
        cur.execute(sql_edu)
        fetch_edu = cur.fetchall()

        doc_languages = []
        doc_symptoms = []
        doc_additional_educations = []
        doc_methods = []

        for key in di.keys():
            if key in l:
                if di[key] == 1:
                    doc_languages.append(l.index(key))
            elif key in s:
                if di[key] == 1:
                    doc_symptoms.append(s.index(key))
            elif key in e:
                if di[key] == 1:
                    doc_additional_educations.append(e.index(key))
            elif key in m:
                if di[key] == 1:
                    doc_methods.append(m.index(key))

        doc_educations = []
        for row in fetch_edu:
            main_edu = {}
            main_edu['year'] = row[0]
            main_edu['university'] = row[1]
            main_edu['faculty'] = row[2]
            main_edu['degree'] = row[3]
            doc_educations.append(main_edu)

        cur.close()
        con.close()

        print(doc_symptoms)
        print(doc_languages)
        print(doc_methods)
        print(doc_educations)
        print(doc_additional_educations)

        print(di)

        out = {'status': True}

        for column in main_columns.split(', '):
            out[column] = di[column]
        out['doc_sympoms'] = doc_symptoms
        out['doc_languages'] = doc_languages
        out['doc_methods'] = doc_methods
        out['doc_educations'] = doc_educations
        out['doc_additional_educations'] = doc_additional_educations


        return out

    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'admin_get_therapist_interview error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'admin_get_therapist_interview error: {e}, {traceback.extract_stack()}'}


@app.post('/admin_update_therapist')
def admin_update_therapist(data: AdminUpdateDoc):
    try:
        con = mariadb.connect(**config)
        cur = con.cursor()

        token = data.session_token
        doc_id = data.doc_id
        sql_check = f"SELECT id FROM tokens JOIN users ON users.id = tokens.user_id WHERE token = '{token}' AND users.is_admin = 1"
        cur.execute(sql_check)
        token_check = cur.fetchall()
        # if not token_check:
        #     return {'status': False}
        doc_email = data.doc_email
        doc_name = data.doc_name
        doc_gender = data.doc_gender
        doc_phone = data.doc_phone
        doc_session_cost = data.doc_session_cost
        if data.doc_avatar == 0:
            doc_avatar = "NULL"
        else:
            doc_avatar = data.doc_avatar
        doc_language = data.doc_language
        doc_method = data.doc_method

        sql_email = f'UPDATE users SET email = "{doc_email}" WHERE id = {doc_id}'

        sql_main = (f'UPDATE doctors SET '
                    f'doc_name = "{doc_name}", '
                    f'doc_gender = {doc_gender}, '
                    f'doc_phone = "{doc_phone}", '
                    f'doc_email = "{doc_email}", '
                    f'doc_avatar = {doc_avatar}, '
                    f'doc_session_cost = {doc_session_cost} '
                    f'WHERE doc_id = {doc_id}')

        print(sql_main)

        l_c = [f'l_{i}' for i in range(0, 3)]
        l_v = [f'0' for i in range(0, 3)]

        m_c = [f'm_{i}' for i in range(0, 17)]
        m_v = [0 for i in range(0, 17)]

        for v in doc_language:
            l_v[v] = 1
        for v in doc_method:
            m_v[v] = 1

        l_sql = []
        m_sql = []

        for index, column in enumerate(l_c):
            l_sql.append(f'{column} = {l_v[index]}')

        for index, column in enumerate(m_c):
            m_sql.append(f'{column} = {m_v[index]}')

        l_sql = ', '.join(l_sql)
        m_sql = ', '.join(m_sql)

        sql_language = f'UPDATE languages SET {l_sql} WHERE doc_id = {doc_id}'
        sql_method = f'UPDATE methods SET {m_sql} WHERE doc_id = {doc_id}'

        cur.execute(sql_email)
        cur.execute(sql_main)
        cur.execute(sql_language)
        cur.execute(sql_method)

        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'admin_update_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'admin_update_therapist error: {e}, {traceback.extract_stack()}'}

@app.post('/doctor_appoint_client')
def doctor_appoint_client(data: DocAppoint):
    try:
        token = data.session_token
        user_id = data.user_id
        date_time = datetime.datetime.strptime(data.date_time, '%Y-%m-%d %H:%M')

        con = mariadb.connect(**config)
        cur = con.cursor()

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        doc_id = cur.fetchall()[0][0]

        sql_tz = f'SELECT doc_timezone FROM doctors WHERE doc_id = {doc_id}'
        cur.execute(sql_tz)
        timezone = cur.fetchall()[0][0]

        date_time = format_time(time=date_time, timezone=timezone, to_utc=True)

        sql_has_theraipst = f'SELECT has_therapist FROM clients WHERE client_id = {user_id}'
        cur.execute(sql_has_theraipst)

        check_id = cur.fetchall()[0][0]

        if check_id == doc_id:
            sql_deactivate = f'DELETE FROM schedule WHERE doctor_id = {doc_id} AND client = {user_id}' # TODO сделать отправку в архив
            cur.execute(sql_deactivate)
            sql_appoint = f'INSERT INTO schedule (doctor_id, date_time, client, accepted) VALUES ({doc_id}, "{date_time}", {user_id}, 1) ON DUPLICATE KEY UPDATE doctor_id = {doc_id}, date_time = " {date_time}", client = {user_id}, accepted = 1'
            cur.execute(sql_appoint)

        else:
            con.commit()
            cur.close()
            con.close()
            return {'status': False,
                    'error': f'doctor_appoint_client error: данные клиента не соответствуют даммым доктора'}


        con.commit()
        cur.close()
        con.close()

        return {'status': True}



    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'doctor_appoint_client error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'doctor_appoint_client error: {e}, {traceback.extract_stack()}'}


def card_validator(data: CardData):
    try:
        month = data.card_valid_to.split('-')[0]
        year = data.card_valid_to.split('-')[0]
        print('len(data.card_number) == 16', len(str(data.card_number)) == 16)
        print('type(int(data.card_number)) == int', type(data.card_number) == int)
        print('len(data.card_cvc) == 3', len(str(data.card_cvc)) == 3)
        print('len(month) == 2', len(month) == 2)
        print('len(year) == 2', len(year) == 2)
        print('1 <= month <= 12', 1 <= int(month) <= 12)
        if len(str(data.card_number)) == 16 and type(data.card_number) == int and len(str(data.card_cvc)) == 3 and len(month) == 2 and len(year) == 2 and 1 <= int(month) <= 12:
            return True
        else:
            return False
    except:
        return False


@app.post('/add_card')
def add_card(data: CardData):
    try:
        if not card_validator(data):
            return {'status': False}
        con = mariadb.connect(**config)
        cur = con.cursor()

        token = data.session_token

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        user_id = cur.fetchall()[0][0]
        if not user_id:
            return {'status': False}

        sql = f"INSERT INTO card_data (user_id, card_number, card_holder, card_cvc, card_valid_to) VALUES ({user_id}, {data.card_number}, '{data.card_holder}', {data.card_cvc}, '{data.card_valid_to}')"
        print(sql)
        cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'add_card error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'add_card error: {e}, {traceback.extract_stack()}'}


@app.post('/update_card')
def update_card(data: CardData):
    try:
        if not card_validator(data):
            print('not')
            return {'status': False}
        con = mariadb.connect(**config)
        cur = con.cursor()

        token = data.session_token

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        user_id = cur.fetchall()[0][0]
        if not user_id:
            return {'status': False}

        sql = f"UPDATE card_data SET card_number = {data.card_number}, card_holder = '{data.card_holder}', card_cvc = {data.card_cvc}, card_valid_to = '{data.card_valid_to}' WHERE user_id = {user_id}"
        cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'update_card error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'update_card error: {e}, {traceback.extract_stack()}'}


@app.post('/delete_card')
def delete_card(data: SingleToken):
    try:
        con = mariadb.connect(**config)
        cur = con.cursor()

        token = data.session_token

        sql_token = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_token)
        user_id = cur.fetchall()[0][0]
        if not user_id:
            return {'status': False}

        sql = f"DELETE FROM card_data WHERE user_id = {user_id}"
        cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'delete_card error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'delete_card error: {e}, {traceback.extract_stack()}'}


@app.post('/check_session')
def check_sessionn(data: SingleToken):
    try:
        t_0 = datetime.datetime.now()
        con = mariadb.connect(**config)
        cur = con.cursor()

        token = data.session_token

        sql_token = f'SELECT user_id, is_therapist FROM tokens JOIN users on tokens.user_id = users.id WHERE token = "{token}"'
        cur.execute(sql_token)
        user_data = cur.fetchall()
        user_id = user_data[0][0]
        is_therapist = user_data[0][1]
        if not user_id:
            return {'status': False}

        # sql = f'SELECT therapy_session, time FROM ongoing_sessions WHERE client_id = {user_id} OR doc_id = {user_id} ORDER BY time DESC'
        # cur.execute(sql)

        # sessions = cur.fetchall()
        sessions = False
        if not sessions:
            if is_therapist:
                sql = f'SELECT client, date_time FROM schedule WHERE client IS NOT NULL AND doctor_id = {user_id} AND accepted = 1'
                print(sql)
                cur.execute(sql)
                fetch = cur.fetchall()
                values = []
                for row in fetch:
                    values.append((str(uuid.uuid4()), user_id, row[0], str(row[1])))
                values = ', '.join([str(x) for x in values])
                print(values)
                try:
                    sql = f'INSERT INTO ongoing_sessions (therapy_session, doc_id, client_id, time) VALUES {values} ON DUPLICATE KEY UPDATE therapy_session_id = therapy_session_id'
                    print(sql)
                    cur.execute(sql)
                except:
                    pass
            else:
                sql = f'SELECT has_therapist FROM clients WHERE client_id = {user_id}'
                print(sql)
                cur.execute(sql)
                doc_id = cur.fetchall()[0][0]
                sql = f'SELECT date_time FROM schedule WHERE client = {user_id} AND doctor_id = {doc_id} AND accepted = 1'
                print(sql)
                cur.execute(sql)
                time = cur.fetchall()[0][0]
                try:
                    sql = f'INSERT INTO ongoing_sessions (therapy_session, doc_id, client_id, time) VALUES {str(uuid.uuid4()), doc_id, user_id, str(time)} ON DUPLICATE KEY UPDATE therapy_session_id = therapy_session_id'
                    print(sql)
                    cur.execute(sql)
                except:
                    pass
            con.commit()
            sql = f'SELECT therapy_session, time FROM ongoing_sessions WHERE client_id = {user_id} OR doc_id = {user_id} ORDER BY time DESC'
            cur.execute(sql)

            sessions = cur.fetchall()

        rooms = []
        for row in sessions:
            print(row)
            x = datetime.datetime.utcnow() - datetime.timedelta(hours=0, minutes=5)
            y = datetime.datetime.utcnow() + datetime.timedelta(hours=1, minutes=5)
            try:
                # if x < row[1] < y:
                rooms.append({'room': row[0], 'time': datetime.datetime.strftime(row[1], '%d-%m-%Y %H:%M')})
            except:
                pass
            print(rooms)

        # con.commit()
        cur.close()
        con.close()

        t_1 = datetime.datetime.now()
        print('TIME')
        print(t_1 - t_0)
        return {'status': True, 'rooms': rooms}

    except Exception as e:
        try:
            cur.close()
            con.close()
        except:
            pass
        print({'status': False,
               'error': f'check_session error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'check_session error: {e}, {traceback.extract_stack()}'}


# @app.post('/create_charge')
# def create_charge(data: ChargeSomeUser):
#     user_id = data.user_id
#     stripe_module.create_charge(description=f'charge for {user_id}')
#     return stripe_module.return_balance()
#
#
# @app.post('/get_charge')
# def get_charge():
#     stripe_module.capture_charge()
#     return stripe_module.return_balance()




@app.post('/db_handler')
def db_handler(data: DBHandler):
    # e6c8e073-5c78-4b5a-9600-2c2cad20c868 - send old schedules to archive
    # 11c4759b-a175-4451-b8a5-f879cf8afcb0
    # 7d3e6b2b-84a8-4abd-a1f1-1f5bfd07b4f8
    # b7617a99-9125-49de-a741-607279df76b2
    # ef471a8e-06ee-4f25-8381-8e5983c918f8
    # 18cbd8c9-430d-4ab1-ac3a-7f3285e9ce37
    # 3e2076a9-b1ac-43b1-8706-d45d5fca21e6
    # 1d73f702-3ba0-4b55-91a1-1fb5bda5fe1b
    # 8fc25a83-eab3-494b-b188-d4f86f986b0e
    # 95680ddd-3b1b-42fd-aa39-d661dac6e36d
    if data.code == 'e6c8e073-5c78-4b5a-9600-2c2cad20c868':
        sql = ('INSERT INTO archive_schedule (sh_id, doctor_id, date_time, client, accepted, pending_change) '
               'SELECT * FROM schedule '
               'WHERE date_time < NOW() '
               'AND sh_id NOT IN (SELECT new_sh_id FROM change_schedule) '
               'ON DUPLICATE KEY UPDATE archive_schedule.sh_id = schedule.sh_id;')


        # Session_data

    #     sql = f'SELECT sh_id, date_time, pending_change FROM schedule WHERE client = {data.user_id}'
    #     cur.execute(sql)
    #     fetch = cur.fetchall()
    #     if fetch:
    #         sh_id = fetch[0][0]
    #         date_time = fetch[0][1]
    #         pending_change = fetch[0][2]
    #
    #         if pending_change:
    #             sql = f'SELECT ch_id, old_sh_id, old_sh.date_time, new_sh_id, new_sh.date_time, who_asked FROM change_schedule JOIN schedule AS old_sh ON change_schedule.old_sh_id = old_sh.sh_id JOIN schedule AS new_sh ON change_schedule.new_sh_id = new_sh.sh_id WHERE change_schedule.client_id = {data.user_id}'
    #             print(sql)
    #             cur.execute(sql)
    #             fetch_pending = cur.fetchall()
    #             sch_data = {}
    #             sch_data['pending'] = True
    #             sch_data['ch_id'] = fetch_pending[0][0]
   #             sch_data['old_sh_id'] = fetch_pending[0][1]
    #             sch_data['old_sh_date_time'] = fetch_pending[0][2]
    #             sch_data['new_sh_id'] = fetch_pending[0][3]
    #             sch_data['new_sh_date_time'] = fetch_pending[0][4]
    #             sch_data['who_asked'] = fetch_pending[0][5]
    #             sch_data['accepted'] = 0
    #         else:
    #             sql = f'SELECT sh_id, date_time, accepted FROM schedule WHERE client = {data.user_id}'
    #             print(sql)
    #             cur.execute(sql)
    #             fetch_normal = cur.fetchall()
    #             sch_data = {}
    #             sch_data['pending'] = False
    #             sch_data['ch_id'] = None
    #             sch_data['old_sh_id'] = fetch_normal[0][0]
    #             sch_data['old_sh_date_time'] = fetch_normal[0][1]
    #             sch_data['new_sh_id'] = None
    #             sch_data['new_sh_date_time'] = None
    #             sch_data['who_asked'] = None
    #             sch_data['accepted'] = fetch_normal[0][2]
    #
    #         sql = f'SELECT doc_name FROM doctors WHERE doc_id = {doc_id}'
    #         print(sql)
    #         cur.execute(sql)
    #
    #         con.commit()
    #         cur.close()
    #         con.close()
    #
    #
    #         return {'status': True,
    #                 'client_id': data.user_id,
    #                 'name': name,
    #                 'user_phone': user_phone,
    #                 'user_age': user_age,
    #                 'user_photo': None,
    #                 'user_card': None,
    #                 'user_cashflow': None,
    #                 'sch_data': sch_data}
    #
    #     con.commit()
    #     cur.close()
    #     con.close()
    #     return {'status': False}
    # except Exception as e:
    #     print({'status': False,
    #            'error': f'admin_get_therapist error: {e}, {traceback.extract_stack()}'})
    #     return {'status': False,
    #             'error': f'admin_get_therapist error: {e}, {traceback.extract_stack()}'}
    #
