import urllib.parse
import db
import server

def add_a_question(request,response):
#     data = """
# <form action='/add-a-question' method='post'>
#     Question:<br>
#     <input type='text' name="quest" size=50 required><br>
#     Option 1:<br>
#     <input type='text' name="opt1"><br>
#     Option 2:<br>
#     <input type='text' name="opt2"><br>
#     Option 3:<br>
#     <input type='text' name="opt3"><br>
#     Option 4:<br>
#     <input type='text' name="opt4"><br>
#     Answer(Enter the option number):<br>
#     <input type='number' name="ans"><br>
#     Score:<br>
#     <input type='number' name="score"><br>
#     <button type='submit'>Add</button>
# </form>
# <a href='/admin'>Back</a>
# """
    with open("./public/html/pyAddQuestion.html", "r") as file_descriptor:
        res = file_descriptor.read()
    return server.send_html_handler(request, response, res)

def listForm(dictQ):
    l = []
    l.append(urllib.parse.unquote_plus(str(dictQ['quest'])))
    l.append(urllib.parse.unquote_plus(str(dictQ['opt1'])))
    l.append(urllib.parse.unquote_plus(str(dictQ['opt2'])))
    l.append(urllib.parse.unquote_plus(str(dictQ['opt3'])))
    l.append(urllib.parse.unquote_plus(str(dictQ['opt4'])))
    l.append(dictQ['ans'])
    l.append(dictQ['score'])
    return l


def add_a_question_post(request,response):
    que = listForm(request['content'])
    print(request['content'])
    print(request)
    db.add_question_pyExam(que)
    data = """
<form action='/add-a-question' method='post'>
    Question:<br>
    <input type='text' name="quest"><br>
    Option 1:<br>
    <input type='text' name="opt1"><br>
    Option 2:<br>
    <input type='text' name="opt2"><br>
    Option 3:<br>
    <input type='text' name="opt3"><br>
    Option 4:<br>
    <input type='text' name="opt4"><br>
    Answer(Enter the option number):<br>
    <input type='number' name="ans"><br>
    Score:<br>
    <input type='number' name="score"><br>
    <button type='submit'>Add</button>
</form>
<a href='/admin'>Back</a>
"""
    return server.send_html_handler(request, response, data)

def formatQuestions(dataItem):
    #print("format")
    #print(dataItem)
    formattedQ = """<li>Question:<br>
    """+dataItem[1]+"""<br><br>Options:<br>
    1."""+dataItem[2]+"""<br>
    2."""+dataItem[3]+"""<br>
    3."""+dataItem[4]+"""<br>
    4."""+dataItem[5]+"""<br><br>
    Answer: Option """+str(dataItem[6])+"""<br>
    Score:"""+str(dataItem[7])+"""<br><br></li>"""
    #print("format")
    return formattedQ

def view_questions(request, response):
    data = db.view_questions_pyExam()
    print(data)
    list2 = list(map(formatQuestions, data))
    finalList = ''.join(list2)
    with open("./public/html/pyViewQuestions.html", "r") as file_descriptor:
            res = file_descriptor.read()
    result = res.format(finalList)
#     htmlCode = """<html>
# <head>
#     <title>Nemo</title>
#     <style type="text/css">
#         body {
#         color: darkblue;
#         background-color: lightgrey
#         }
#     </style>
# </head>
# <body>
#     <ol>%s</ol>
#     <a href='/admin'>Back</a>
# </body>
# </html>""" %(finalList)
    return server.send_html_handler(request, response, result)
