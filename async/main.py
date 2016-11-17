from dotenv import Dotenv
import json
import os
import requests
import server
import sqlite3 as sql
import sys

env = None

try:
    env = Dotenv("./.env")
    con = sql.connect("profile.db")
    c = con.cursor()
    table_create = """
create table if not exists profile(
id text primary key,
name text,
gender text,
dob text
);"""
    c.execute(table_create)
except IOError:
    env = os.environ
except sql.Error as e:
    print("Error encountered:{0}".format(e.args[0]))
    sys.exit(1)


def html_head():
    data = """
           <html>
           <head>
           </head>
           <body>
"""
    return data


def html_tail():
    data = """
           </body>
           </html>
"""
    return data


def build_routes():
    server.add_route("get", "/", home)
    server.add_route("get", "/callback", callback)
    server.add_route("get", "/update", update)
    server.add_route("post", "/profile_update", profile_update)
    server.add_route("get", "/profile", profile)


def home(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        return profile(request, response)
    with open("./views/index.html", "r") as f:
        data = f.read()
    return server.send_html_handler(request, response, data)


def callback(request, response):
    code = request["content"]["code"]
    json_header = {'content-type': 'application/json'}
    token_url = "https://{0}/oauth/token".format(env["AUTH0_DOMAIN"])
    token_payload = {
        'client_id': env['AUTH0_CLIENT_ID'],
        'client_secret': env['AUTH0_CLIENT_SECRET'],
        'redirect_uri': env['AUTH0_CALLBACK_URL'],
        'code': code,
        'grant_type': 'authorization_code'
    }
    token_info = requests.post(token_url, data=json.dumps(
        token_payload), headers=json_header).json()
    user_url = "https://{0}/userinfo?access_token={1}".format(
        env["AUTH0_DOMAIN"], token_info['access_token'])
    user_info = requests.get(user_url).json()
    user_id = user_info["identities"][0]["user_id"]
    content = {"user_id": user_id}
    server.add_session(request, content)
    get_query = "select count(*) from profile where id=(?)"
    c.execute(get_query, (user_id,))
    (no_rows,) = c.fetchone()
    if not no_rows:
        query = "insert into profile (id) values (?)"
        c.execute(query, (user_id,))
        con.commit()
    return profile(request, response)


def profile(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        data = html_head()
        get_query = "select count(*) from profile where id=(?)"
        c.execute(get_query, (session_data["user_id"],))
        (no_rows,) = c.fetchone()
        if no_rows:
            query = "select * from profile where id=(?)"
            c.execute(query, (session_data["user_id"],))
            res = c.fetchall()
            if res[0][1]:
                data += "<p>Name: {0}</p><br/>".format(res[0][1])
                data += "<p>Gender: {0}</p><br/>".format(res[0][2])
                data += "<p>Date of Birth: {0}</p><br/>".format(res[0][3])
                data += """<img src='./uploads/{0}.jpg' width='200px' height='200px'/>
                        <br/>""".format(session_data["user_id"])
                data += "<a href='/update'>Update details here</a>"
                data += html_tail()
                return server.send_html_handler(request, response, data)
        data += "Welcome to Profile app<br/>"
        data += "<a href='/update'>Update details here</a>"
        data += html_tail()
        return server.send_html_handler(request, response, data)
    return home(request, response)


def update(request, response):
    with open("./views/update.html", "r") as f:
        data = f.read()
    return server.send_html_handler(request, response, data)


def profile_update(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        name = request["content"]["name"]
        date_of_birth = request["content"]["dob"]
        gender = request["content"]["gender"]
        profile_pic = request["content"]["profile"]
        file_name = "./public/uploads/{0}.jpg".format(session_data["user_id"])
        with open(file_name, "wb") as f:
            f.write(profile_pic)
        query = "update profile set name=?, dob=?, gender=? where id=?"
        c.execute(query, (name, date_of_birth,
                          gender, session_data["user_id"]))
        con.commit()
        return profile(request, response)
    return server.err_404_handler(request, response)


def main():
    # port = int(input("PORT:"))
    build_routes()
    server.start_server("", port=8080)


if __name__ == "__main__":
    main()
