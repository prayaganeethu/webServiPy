import sqlite3
import json

conn = sqlite3.connect("pythonExamDb.db")
cursor = conn.cursor()

def query_db(query, args=(), one=False):
    cursor.execute(query, args)
    # print("QUERY\n\n")
    # print(cursor.fetchall())
    # print("QUERY\n\n")
    # print(cursor.description)
    #data = cursor.fetchall()
    print("\n\n\ncursor\n\n\n")
    print("\n\n\ndesc\n\n\n",cursor.description[1])
    print('neetu')
    # fetch = cursor.fetchall()
    # r, val = [], []
    # for row in fetch:
    # 	print("Row\t", row)
    # 	for i, value in enumerate(row):
    # 		r.append((cursor.description[i][0], value))

    # 	val.append(dict(r))
    # 	r = []


    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    
    print("\n\n\nDict\n\n\n",r)
    conn.commit()
    #return (r[0] if r else None) if one else r
    # return (r[0] if r else None) if one else r
    return r

def add_question_pyExam(quest):
    cursor.execute("INSERT INTO pyQuestionsMCQ(Question,AnsOpt1,AnsOpt2,AnsOpt3,AnsOpt4,Answer,Score) VALUES(?,?,?,?,?,?,?)",quest)
    conn.commit()

def view_questions_pyExam():
    cursor.execute('SELECT * FROM pyQuestionsMCQ')
    return cursor.fetchall()

def show_Quest_pyExam():
    my_query = query_db("SELECT * FROM pyQuestionsMCQ ORDER BY RANDOM() LIMIT ?", (3,), one=True)
    print("my_query")
    print(my_query)
    return my_query
    #cursor.execute('SELECT * FROM pyQuestionsMCQ ORDER BY RANDOM() LIMIT 1')
    #return cursor.fetchone()

#def show_question_pyExam(qnum):
    #cursor.execute('SELECT * FROM pyQuestionsMCQ WHERE QNo > ? ORDER BY QNo LIMIT 1',(qnum,))
    #return cursor.fetchone()
