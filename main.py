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
import traceback # for debug
from fastapi import FastAPI, applications, Request, HTTPException
from pydantic import ValidationError
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
                         UserTherapist,
                         UserTherapistReview,
                         SingleToken,
                         ApproveTime,
                         SelectTime,
                         ReSelectTime,
                         GetSomeoneData,
                         CancelTherapy,
                         DocRegister,
                         DocScheldure,
                         ApproveTherapistToken,
                         AdminReport,
                         DocUpdate)
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


@app.post("/generate_password")
def gen_password(data: UserLoginGen):
    # TODO оправлять фалсе если пользователя нет
    try:
        email = data.user_email
        password = ''.join([random.choice(string.ascii_letters) + random.choice(string.digits) for i in range(0, 4)])
        sql = f'UPDATE users SET password = "{password}" WHERE email = "{email}";'
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

        print({"status": True,
               "password": password})

        return {"status": True,
                "password": password}
    except Exception as e:
        print({'status': False,
                'error': f'/login error: {e} {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'/login error: {e} {traceback.extract_stack()}'}




# DEBUG DELETE THIS FUNC
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

    print({"email": email,
            "password": password})

    return {"email": email,
            "password": password}


@app.post("/logout")
def logout(data: SingleToken):
    """
    Logout user/therapist/admin
    """
    token = data.session_token
    sql = f"DELETE FROM tokens WHERE token = '{token}'"
    con = mariadb.connect(**config)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

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
                # cur.execute(f'DELETE FROM tokens WHERE user_id = "{user_id}"')
                cur.execute(f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}');")
                con.commit()
                cur.close()
                con.close()
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
        return {'status': False,
                'error': f'/login error: {e} {traceback.extract_stack()}'}


@app.post("/register")
def register(data:UserCreate):
    # TODO добавить токен
    try:
        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{data.user_email}';")
        f = cur.fetchall()
        if f == []:
            cur.execute(f"INSERT INTO users (email, password) VALUES ('{data.user_email}', '{data.password}') RETURNING id;")
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
            con.commit()
            cur.close()
            con.close()
            return {'status': True,
                    'token': f'{token}'}
        else:
            cur.close()
            con.close()
            return {'status': False,
                    'error': 'registration error, user exists'}
    except Exception as e:
        return {'status': False,
                'error': f'/register error: {e} {traceback.extract_stack()}'}


@app.post("/get_client_data")
def return_client_data(data: SingleToken):
    try:
        token = data.session_token

        data_cols = 'clients.client_id, name, user_age, user_experience, user_type, user_therapist_gender, user_time, user_specific_date_time, user_price, user_phone, email, has_therapist, user_timezone, user_photo'
        language_list = [f'l_{i}' for i in range(0,3)]
        language_cols = ', '.join(language_list)
        symptoms_list = [f's_{i}' for i in range(0,28)]
        symptoms_cols = ', '.join(symptoms_list)

        sql_1 = (f'SELECT {data_cols}, {language_cols}, {symptoms_cols} '
                 f'FROM clients '
                 f'JOIN tokens ON clients.client_id = tokens.user_id '
                 f'JOIN client_languages ON clients.client_id = client_languages.client_id '
                 f'JOIN client_symptoms ON clients.client_id = client_symptoms.client_id '
                 f'JOIN users ON clients.client_id = users.id '
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
        cur.execute(sql_1)
        desc = cur.description
        fetch_0 = cur.fetchall()
        print('fetch_0')
        print(fetch_0)
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
        else:
            out['client_id'] = fetch_0[0][0]
            out['name'] = fetch_0[0][1]
            out['email'] = fetch_0[0][13]
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

        out['user_photo'] = ""
        out['user_symptoms'] = user_symptoms
        out['user_languages'] = user_languages

        if out["has_therapist"]:
            sql = f"SELECT doc_name, date_time, pending_change, sh_id, accepted FROM schedule JOIN doctors ON schedule.doctor_id = doctors.doc_id WHERE doctor_id = {out['has_therapist']} AND client = {fetch_0[0][0]} AND pending_change IN (0, 1)"
            cur.execute(sql)
            fetch = cur.fetchall()
            pending = fetch[0][2]
            accepted = fetch[0][4]
            new_time = ''
            if pending:
                old_sh_id = fetch[0][3]
                sql_1 = f"SELECT new_sh_id, who_asked FROM change_schedule WHERE old_sh_id = {old_sh_id}"
                cur.execute(sql_1)
                fetch_1 = cur.fetchall()
                new_sh_id = fetch_1[0][0]
                pending = fetch_1[0][1]
                sql_1 = f"SELECT date_time FROM schedule WHERE sh_id = {new_sh_id}"
                cur.execute(sql_1)
                fetch_1 = cur.fetchall()
                new_time = fetch_1[0][0]
            print(fetch)
            out["has_therapist"] = {'doc_id': out['has_therapist'], 'doc_name': fetch[0][0], 'sch_time': fetch[0][1], 'pending': pending, 'new_sch_time': new_time, 'accepted': accepted}

        con.commit()
        cur.close()
        con.close()

        return out
    except Exception as e:
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
        sql_1_vals = f'"{data.user_age}", {data.user_experience}, {data.user_type}, {data.user_therapist_gender}, "{data.user_time}", "{data.user_specific_date_time}", {data.user_price}, "{data.user_phone}", "{data.user_photo}", {data.user_timezone}'
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

        sql_3_cols = [f's_{i}' for i in range(0, 28)]
        sql_3_vals = ["0" for i in range(0, 28)]
        if data.user_symptoms:
            for index in data.user_symptoms:
                sql_3_vals[index] = "1"
        update_data = []
        for i in range(0, len(sql_3_cols)):
            update_data.append(f'{sql_3_cols[i]} = {sql_3_vals[i]}')
        update_data = ', '.join(update_data)
        sql_3 = f"INSERT INTO client_symptoms (client_id, {', '.join(sql_3_cols)}) VALUES ({client_id}, {', '.join(sql_3_vals)}) ON DUPLICATE KEY UPDATE {update_data}"
        cur.execute(sql_3)

        con.commit()
        cur.close()
        con.close()
        return {'status': True}

    except Exception as e:
        print({'status': False,
                'error': f'update_client error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'update_client error: {e}, {traceback.extract_stack()}'}


@app.post("/user_therapist_cancel_review")
def update_user_main(data: UserTherapistReview):
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
        con.commit()
        cur.close()
        con.close()

        return {'status': True}

    except Exception as e:
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

        sql_0 = f"UPDATE users SET email = '{email}' WHERE id = {client_id}"
        sql_1 = f"UPDATE clients SET name = '{name}', user_timezone = {user_timezone} WHERE client_id = {client_id}"

        languages = [0, 0, 0]
        for i in user_languages:
            languages[i] = 1

        sql_2 = f"UPDATE client_languages SET l_0 = {languages[0]}, l_1 = {languages[1]}, l_2 = {languages[2]} WHERE client_id = {client_id}"

        cur.execute(sql_0)
        cur.execute(sql_1)
        cur.execute(sql_2)

        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
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

        return {'status': True}
    except Exception as e:
        print({'status': False,
                'error': f'/update_user_request error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'/update_user_request error: {e}, {traceback.extract_stack()}'}



@app.post("/get_therapist_list")
def get_therapist_list(data: SingleToken):
    # TODO ДОПИЛИТЬ ФИЛЬТРЫ ПО ЯЗЫКУ И ПОЛУ
    try:
        token = data.session_token
        symptoms = [f's_{i}' for i in range(0, 28)]
        sql_0 = f'SELECT {", ".join(symptoms)} FROM client_symptoms JOIN tokens ON client_symptoms.client_id = tokens.user_id WHERE token = "{token}"'

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql_0)
        client_symptoms = cur.fetchall()

        sql_1 = f'SELECT doc_id, {", ".join(symptoms)} from doc_symptoms'
        cur.execute(sql_1)
        docs = cur.fetchall()

        print(client_symptoms)
        print(docs)

        valid_docs = []
        print(client_symptoms)
        for doc_info in docs:
            print(doc_info)
            if client_symptoms[0] <= doc_info[1:]:
                valid_docs.append(str(doc_info[0]))

        sql_2 = f'SELECT doc_id, doc_name, doc_additional_info FROM doctors WHERE doc_id IN ({", ".join(valid_docs)})'
        print(sql_2)
        cur.execute(sql_2)
        out_docs = cur.fetchall()

        sql_3 = f'SELECT doc_id, year, university, faculty, degree FROM educations_main WHERE doc_id IN ({", ".join(valid_docs)})'
        cur.execute(sql_3)
        out_edu = cur.fetchall()
        print(out_edu)

        edu_dict = {}
        for doc_id in valid_docs:
            edu_dict[int(doc_id)] = []

        for row in out_edu:
            print(row)
            doc_id = row[0]
            year = row[1]
            university = row[2]
            faculty = row[3]
            degree = row[4]
            edu_dict[int(doc_id)].append({'year': year, 'university': university, 'faculty': faculty, 'degree': degree})

        print(edu_dict)

        sql_4 = f'SELECT doctor_id, sh_id, date_time FROM schedule WHERE client IS NULL and doctor_id IN ({", ".join(valid_docs)})'
        cur.execute(sql_4)
        out_sch = cur.fetchall()
        # print(out_sch)

        sh_dict = {}
        for doc_id in valid_docs:
            sh_dict[int(doc_id)] = []

        for row in out_sch:
            doc_id = row[0]
            sh_id = row[1]
            date_time = row[2]
            # print(doc_id, sh_id, date_time)
            sh_dict[int(doc_id)].append({'sh_id': sh_id, 'time': date_time})

        # print(sh_dict)

        out_docs = [{"doc_id": row[0], "doc_name": row[1], "doc_additional_info": row[2], "doc_edu": edu_dict[row[0]], "doc_schedule": sh_dict[row[0]]} for row in out_docs]
        cur.close()
        con.close()

        out = {"status": True,
               "list_of_doctors": out_docs}
        return out
    except Exception as e:
        print({'status': False,
                'error': f'list_therapist for client error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'list_therapist for client error: {e}, {traceback.extract_stack()}'}




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
        columns = 'doc_id, doc_name, doc_date_of_birth, doc_gender, doc_edu, doc_method_other, doc_comunity, doc_practice_start, doc_online_experience, doc_customers_amount_current, doc_therapy_length, doc_personal_therapy, doc_supervision, doc_another_job, doc_customers_slots_available, doc_socials_links, doc_citizenship, doc_citizenship_other, doc_ref, doc_ref_other, doc_phone, doc_email, doc_additional_info, doc_question_1, doc_question_2, doc_contact, user_photo'

        # save photos
        img_data = []
        # for item in data.user_photo:
        #     img_data.append(str((item['data'], item['name'], item['type'])))

        if img_data:
            sql = f'INSERT INTO images (data, name, type) VALUES {", ".join(img_data)} RETURNING img_id;'
            cur.execute(sql)
            f = cur.fetchall()
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


        items = [data.doc_name, data.doc_date_of_birth, data.doc_gender, data.doc_edu, data.doc_method_other, data.doc_comunity, data.doc_practice_start, data.doc_online_experience, data.doc_customers_amount_current, data.doc_therapy_length, data.doc_personal_therapy, data.doc_supervision, data.doc_another_job, data.doc_customers_slots_available, data.doc_socials_links, data.doc_citizenship, data.doc_citizenship_other, data.doc_ref, data.doc_ref_other, data.doc_phone, data.doc_email, data.doc_additional_info, data.doc_question_1, data.doc_question_2, data.doc_contact, data.user_photo]
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
        con.commit()
        cur.close()
        con.close()

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
               f'm_10, '  # 36 10
               f'm_11, '  # 36 11
               f'm_12, '  # 36 12
               f'm_13, '  # 36 13
               f'm_14, '  # 36 14
               f'm_15, '  # 36 15
               f'l_0, '  # 37  16
               f'l_1, '  # 38  17
               f'l_2, '  # 39  18
               f'e_0, '  # 40  19
               f'e_1, '  # 41  20
               f'e_2, '  # 42  21
               f'e_3, '  # 43  22
               f'e_4 '  # 44  23
               f'FROM doctors '
               f'JOIN tokens ON doctors.doc_id = tokens.user_id '
               f'JOIN methods ON doctors.doc_id = methods.doc_id '
               f'JOIN languages ON doctors.doc_id = languages.doc_id '
               f'JOIN educations ON doctors.doc_id = educations.doc_id '
               f'WHERE token = "{token}"')

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        d = cur.description
        print('______________________________')
        for i, x in enumerate(d):
            print(f'{i} / {x[0]} / {f[0][i]}')
        print('______________________________')
        con.commit()
        cur.close()
        con.close()

        doc_id, doc_photos_ids = f[0][0], f[0][26]
        print(f[0])
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
               'user_photo': fph}
        print(out)
        return out
    except ValidationError as e:
        print({'status': False,
                'error': f'register_therapist error: validation error, {e}, {traceback.extract_stack()}, ЭТО ЗНАЧИТ С ФРОНТА ПРИШЛО ЧТО-ТО НЕ ТО!'})
        return {'status': False,
                'error': f'register_therapist error: validation error, {e}, {traceback.extract_stack()}, ЭТО ЗНАЧИТ С ФРОНТА ПРИШЛО ЧТО-ТО НЕ ТО!'}
    except Exception as e:
        print({'status': False,
                'error': f'register_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'register_therapist error: {e}, {traceback.extract_stack()}'}



@app.post('/get_doc_data')
def get_doc_data(data: SingleToken):

    try:
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
               f'user_photo, '  # 26
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
               f'doc_therapy_type '  # 82
               f'FROM doctors '
               f'JOIN tokens ON doctors.doc_id = tokens.user_id '
               f'JOIN languages ON doctors.doc_id = languages.doc_id '
               f'JOIN methods ON doctors.doc_id = methods.doc_id '
               f'JOIN educations ON doctors.doc_id = educations.doc_id '
               f'JOIN doc_symptoms ON doctors.doc_id = doc_symptoms.doc_id '
               f'WHERE token = "{token}"')

        con = mariadb.connect(**config)
        cur = con.cursor()
        cur.execute(sql)
        f = cur.fetchall()
        d = cur.description
        print('______________________________')
        for i, x in enumerate(d):
            print(f'{i} / {x[0]} / {f[0][i]}')
        print('______________________________')
        con.commit()
        cur.close()
        con.close()

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

            fph = [{'data': ph[0], 'name': ph[1], 'type': ph[2]} for ph in fph]
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
               'doc_symptoms': doc_symptoms_out,
               'user_photo': fph}
        print(out)
        return out
    except Exception as e:
        print({'status': False,
                'error': f'get_doc_data error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'get_doc_data error: {e}, {traceback.extract_stack()}'}

@app.post('/doctor_schedule')
def doctor_schedule(data: DocScheldure):
    try:
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
            print({'status': False,
                    'error': """doctor_schedule error: user not auth-ed"""})
            return {'status': False,
                    'error': """doctor_schedule error: user not auth-ed"""}
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
            print({'status': True, 'schedule': out, 'timezone': timezone})
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
        print({'status': True, 'schedule': out, 'timezone': timezone})
        return {'status': True, 'schedule': out, 'timezone': timezone}
    except Exception as e:
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
            print(975)
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
            print({'status': True})
            return {'status': True}
    except Exception as e:
        print({'status': False,
                'error': f'update_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'update_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/get_available_slots')
def get_available_slots(data: SingleToken):
    try:
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

    sql_1 = f'UPDATE schedule SET client = {client_id} WHERE sh_id = {sh_id} AND doctor_id = {doc_id} AND client IS NULL'
    print(sql_1)
    cur.execute(sql_1)
    sql_2 = f'SELECT date_time FROM schedule WHERE client = {client_id} AND sh_id = {sh_id} AND doctor_id = {doc_id}'
    cur.execute(sql_2)
    try:
        date_time = cur.fetchall()[0][0]
    except:
        date_time = None

    if date_time:
        sql_3 = f'UPDATE clients SET has_therapist = {doc_id} WHERE client_id = {client_id}'
        cur.execute(sql_3)
        con.commit()
    else:
        return {"status": False}
    cur.close()
    con.close()

    return {"status": True,
            "time": date_time}

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
            sql_0 = f'UPDATE schedule SET accepted = 1, pending_change = 0 WHERE sh_id = {sh_id} AND doctor_id = {doc_id}'
            print(sql_0)
            cur.execute(sql_0)
            sql_1 = f'SELECT client FROM schedule WHERE sh_id = "{sh_id}"'
            cur.execute(sql_1)
            fetch_1 = cur.fetchall()
            client_id = fetch_1[0][0]
            sql_2 = f'UPDATE clients SET first_time = 0 WHERE client_id = {client_id}'

            if data.ch_id:
                sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {data.ch_id}'
                cur.execute(sql)
                fetch = cur.fetchall()
                old_sh_id = fetch[0][0]
                sql = f'UPDATE schedule SET client = NULL WHERE sh_id = {old_sh_id}'
                cur.execute(sql)
                sql = f'DELETE FROM change_schedule WHERE ch_id = {data.ch_id}'
                cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        return {'status': True}
    except Exception as e:
        print({'status': False, 'error': f'approve_time_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False, 'error': f'approve_time_therapist error: {e}, {traceback.extract_stack()}'}




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
        send_email_func(to_addr='admin@speakyourmind.help',
                        sender=report_email,
                        noreply=True,
                        author=report_email,
                        subject=data.report_subject + f': {str(datetime.datetime.now().ctime())}',
                        content=f'REPORT FROM {report_name} ({report_email}):\n' + data.report_text)
        return {"status": True}
    except Exception as e:
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
            print({'status': True})
            return {'status': True}
        print({'status': False,
                'error': 'approve_therapist error: no such admin, or admin not logged in'})
        return {'status': False,
                'error': 'approve_therapist error: no such admin, or admin not logged in'}
    except Exception as e:
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
            sql = 'SELECT doc_id, doc_name, doc_gender, email, registred_date FROM users JOIN doctors ON doc_id = users.id'
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
                            'registred_date': row[4]})
            print({'status': True,
                    'list': out})
            return {'status': True,
                    'list': out}
    except Exception as e:
        print({'status': False,
                'error': f'list_therapist error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'list_therapist error: {e}, {traceback.extract_stack()}'}


@app.post('/list_clients')
def list_clients(data: SingleToken):
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
            sql = 'SELECT client_id, name, email, registred_date FROM users JOIN doctors ON doc_id = users.id'
            con = mariadb.connect(**config)
            cur = con.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            con.commit()
            cur.close()
            for row in res:
                out.append({'client_id': row[0],
                            'name': row[1],
                            'email': row[2],
                            'registred_date': row[3]})
            print({'status': True,
                    'list': out})
            return {'status': True,
                    'list': out}
        else:
            return {'status': False}
    except Exception as e:
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

        sql_1 = f'SELECT has_therapist FROM clients WHERE client_id = {client_id}'
        cur.execute(sql_1)
        doc_id = cur.fetchall()[0][0]

        sql_2 = f'UPDATE schedule SET pending_change = 1 WHERE sh_id = {old_sh_id}'
        cur.execute(sql_2)

        sql_3 = f'UPDATE schedule SET client = {client_id}, pending_change = 2 WHERE sh_id = {sh_id} AND doctor_id = {doc_id} AND client IS NULL'
        cur.execute(sql_3)

        sql_4 = f'INSERT INTO change_schedule (client_id, doc_id, old_sh_id, new_sh_id, who_asked) VALUES ({client_id}, {doc_id}, {old_sh_id}, {sh_id}, 2)'
        cur.execute(sql_4)

        if data.ch_id:
            sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {data.ch_id}'
            cur.execute(sql)
            fetch = cur.fetchall()
            old_sh_id = fetch[0][0]
            sql = f'UPDATE schedule SET client = NULL WHERE sh_id = {old_sh_id}'
            cur.execute(sql)
            sql = f'DELETE FROM change_schedule WHERE ch_id = {data.ch_id}'
            cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        return {"status": True}
    except Exception as e:
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

        sql_0 = f'SELECT user_id FROM tokens WHERE token = "{token}"'
        cur.execute(sql_0)
        doc_id = cur.fetchall()[0][0]

        sql_1 = f'SELECT client FROM schedule WHERE sh_id = {old_sh_id}'
        cur.execute(sql_1)
        client_id = cur.fetchall()[0][0]

        sql_2 = f'UPDATE schedule SET pending_change = 1 WHERE sh_id = {old_sh_id}'
        cur.execute(sql_2)

        sql_3 = f'UPDATE schedule SET client = {client_id}, pending_change = 2 WHERE sh_id = {sh_id} AND doctor_id = {doc_id} AND client IS NULL'
        cur.execute(sql_3)

        sql_4 = f'INSERT INTO change_schedule (client_id, doc_id, old_sh_id, new_sh_id, who_asked) VALUES ({client_id}, {doc_id}, {old_sh_id}, {sh_id}, 1)'
        cur.execute(sql_4)

        if data.ch_id:
            sql = f'SELECT old_sh_id FROM change_schedule WHERE ch_id = {data.ch_id}'
            cur.execute(sql)
            fetch = cur.fetchall()
            old_sh_id = fetch[0][0]
            sql = f'UPDATE schedule SET client = NULL WHERE sh_id = {old_sh_id}'
            cur.execute(sql)
            sql = f'DELETE FROM change_schedule WHERE ch_id = {data.ch_id}'
            cur.execute(sql)

        con.commit()
        cur.close()
        con.close()

        return {"status": True}
    except Exception as e:
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
        normal_sessions_list = []
        for row in fetch_0:
            out_normal = {}
            out_normal['client_id'] = row[0]
            out_normal['name'] = row[1]
            out_normal['sh_id'] = row[2]
            out_normal['time'] = row[3]
            out_normal['accepted'] = row[4]
            normal_sessions_list.append(out_normal)

        pending_sessions_list = []
        sql_1 = f'SELECT ch_id, ch.client_id, name, old_sh_id, new_sh_id, old_sh.date_time, new_sh.date_time FROM testdb.change_schedule ch JOIN schedule old_sh ON ch.old_sh_id = old_sh.sh_id JOIN schedule new_sh ON ch.new_sh_id = new_sh.sh_id JOIN clients ON ch.client_id = clients.client_id WHERE ch.doc_id = {doc_id} ORDER BY ch_id DESC;'
        cur.execute(sql_1)
        fetch_1 = cur.fetchall()
        for row in fetch_1:
            out_pending = {}
            out_pending['ch_id'] = row[0]
            out_pending['client_id'] = row[1]
            out_pending['name'] = row[2]
            out_pending['old_sh_id'] = row[3]
            out_pending['new_sh_id'] = row[4]
            out_pending['old_time'] = row[5]
            out_pending['new_time'] = row[6]

            pending_sessions_list.append(out_pending)

        con.commit()
        cur.close()
        con.close()

        return {'status': True,
                'normal_sessions_list': normal_sessions_list,
                'pending_sessions_list': pending_sessions_list}
    except Exception as e:
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
        client_id = fetch[0][0]
        doc_id = fetch[0][1]

        if doc_id:
            sql_1 = f'SELECT sh_id, date_time, client, accepted FROM schedule WHERE client IS NULL OR client = {client_id} AND doctor_id = {doc_id}'
            cur.execute(sql_1)
            fetch = cur.fetchall()
            # print(fetch)
            sh_out = []
            for row in fetch:
                # print(row)
                sh_row = {}
                sh_row['sh_id'] = row[0]
                sh_row['date_time'] = row[1]
                sh_row['client'] = row[2] if row[2] else None
                sh_row['accepted'] = row[3] if row[3] else None
                sh_out.append(sh_row)
            return {'status': True,
                    'doctor_id': doc_id,
                    'schedule': sh_out}

        else:
            return {'status': False, 'error': 'Client have no therapist'}
    except Exception as e:
        print({'status': False,
               'error': f'get_clients_therapist_schedule error: {e}, {traceback.extract_stack()}'})
        return {'status': False,
                'error': f'get_clients_therapist_schedule error: {e}, {traceback.extract_stack()}'}



@app.post('/get_user_data')
def get_user_data(data: GetSomeoneData):
    token = data.session_token

    con = mariadb.connect(**config)
    cur = con.cursor()

    sql = f'SELECT user_id, is_therapist FROM tokens WHERE token = "{token}"'
    cur.execute(sql)

    fetch = cur.fetchall()
    is_therapist = fetch[0][1]

    if is_therapist:
        doc_id = fetch[0][0]

    sql = f'SELECT name, age, NULL FROM clients JOIN schedule ON clients.client_id = schedule.client WHERE client = {data.user_id} AND doctor_id = {doc_id} ORDER by sh_id DESC'