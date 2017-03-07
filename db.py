import sqlite3

conn = sqlite3.connect("myDb.db")
cursor = conn.cursor()

def add_question_pyExam(quest):
    #print(type(quest))
    cursor.execute("INSERT INTO Sam VALUES (?)",[(quest)])
    #view_questions_pyExam()
    conn.commit()
    #conn.close()

def view_questions_pyExam():
    cursor.execute('SELECT Name FROM Sam')
    return cursor.fetchall()
