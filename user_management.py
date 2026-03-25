import sqlite3 as sql
import time
import random
from werkzeug.security import generate_password_hash, check_password_hash


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    hashed_password = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashed_password, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    con.row_factory = sql.Row
    user = con.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user == None:
        con.close()
        print("no username match")
        return None
    else:
        if check_password_hash(user["password"], password):

            # Plain text log of visitor count as requested by Unsecure PWA management
            with open("visitor_log.txt", "r") as file:
                number = int(file.read().strip())
                number += 1
            with open("visitor_log.txt", "w") as file:
                file.write(str(number))
            print("login ok")
            con.close()
            return user
        else:
            print("password fail")
            return None


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
