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
first_name text,
last_name text,
email text,
address text,
hometown text,
date_of_birth text,
date_of_joining text,
ph_no text
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
    server.add_route("get", "/dashboard", dashboard)
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
    ph_no = user_info["phone_number"]
    content = {"user_id": user_id}
    server.add_session(request, content)
    get_query = "select count(*) from profile where id=(?)"
    c.execute(get_query, (user_id,))
    (no_rows,) = c.fetchone()
    if not no_rows:
        query = "insert into profile (id, ph_no) values (?, ?)"
        c.execute(query, (user_id, ph_no,))
        con.commit()
    return profile(request, response)


def profile(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        data = html_head()
        get_query = "select count(*) from profile where id=(?)"
        if ("content" in request and "id" in request["content"] and
                session_data["user_id"] == "5820148e514cff820b882897"):
            u_id = request["content"]["id"]
        else:
            u_id = session_data["user_id"]
        c.execute(get_query, (u_id,))
        (no_rows,) = c.fetchone()
        if no_rows:
            query = "select * from profile where id=(?)"
            c.execute(query, (u_id,))
            res = c.fetchall()
            if res[0][1]:
                with open("./views/profile.html", "r") as f:
                    data = f.read()
                data = data.format(id=res[0][0], fname=res[0][1],
                                   lname=res[0][2], email=res[0][3],
                                   ph_no=res[0][8],
                                   address=res[0][4], hometown=res[0][5],
                                   date_of_birth=res[0][6],
                                   date_of_joining=res[0][7])
                return server.send_html_handler(request, response, data)
        return update(request, response)
    return home(request, response)


def update(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        with open("./views/update.html", "r") as f:
            data = f.read()
        return server.send_html_handler(request, response, data)
    return home(request, response)


def dashboard(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        data = ""
        c.execute("select * from profile")
        rows = c.fetchall()
        for row in rows:
            data += "Name: <a href='/profile?id={0}'>{1}{2}</a>".format(row[0],
                                                                        row[1],
                                                                        row[2])
            data += "<br/>"
        return server.send_html_handler(request, response, data)
    return home(request, response)


def profile_update(request, response):
    session_data = server.get_session(request)
    if session_data and "user_id" in session_data:
        first_name = request["content"]["fname"]
        last_name = request["content"]["lname"]
        email = request["content"]["email"]
        profile_pic = request["content"]["blob"]
        address = request["content"]["contactAddress"]
        hometown = request["content"]["hometown"]
        date_of_birth = request["content"]["dob"]
        date_of_joining = request["content"]["doj"]
        id_proof = request["content"]["idproof"]
        address_proof = request["content"]["adproof"]

        file_name = "./public/storage/profile_pic/{0}.jpg".format(session_data[
            "user_id"])
        with open(file_name, "wb") as f:
            f.write(profile_pic)
        file_name2 = "./public/storage/id_proof/{0}.pdf".format(
            session_data["user_id"])
        with open(file_name2, "wb") as f:
            f.write(id_proof)
        file_name3 = "./public/storage/address_proof/{0}.pdf".format(
            session_data["user_id"])
        with open(file_name3, "wb") as f:
            f.write(address_proof)
        query = """update profile set first_name = ?, last_name = ?, email =?,
                   address=?, hometown=?, date_of_birth=?, date_of_joining=?
                   where id=?"""
        c.execute(query, (first_name, last_name, email, address, hometown,
                          date_of_birth, date_of_joining,
                          session_data["user_id"]))
        con.commit()
        return profile(request, response)
    return server.err_404_handler(request, response)


def main():
    # port = int(input("PORT:"))
    build_routes()
    server.start_server("", port=8080)


if __name__ == "__main__":
    main()
