import server
import db
import urllib.parse


def build_routes():
    server.add_route('get', '/admin', admin)
    server.add_route('get', '/login', login)
    server.add_route('get', '/add-a-question', add_a_question)
    server.add_route('post','/add-a-question', add_a_question_post)
    server.add_route('get', '/view-questions', view_questions)

def add_a_question(request,response):
    data = """
<form action='/add-a-question' method='post'>
<input type='text' name="quest" />
<button type='submit'>Add</button>
</form>
<a href='/admin'>Back</a>
"""
    return server.send_html_handler(request, response, data)

def question_parse(que):
    queChar = que.split("+")
    print(queChar)
    queStr = ""
    for i in queChar:
        queStr+=" "+i
    print(queStr)
    return queStr


def add_a_question_post(request,response):
    que = urllib.parse.unquote_plus(str(request['content']['quest']))
    print(request['content']['quest'])
    print(request)
    db.add_question_pyExam(str(que))
    data = """
<form action='/add-a-question' method='post'>
<input type='text' name="quest" />
<button type='submit'>Add</button>
</form>
<a href='/admin'>Back</a>
"""
    return server.send_html_handler(request, response, data)

def generateList(dataItem):
    return """
<li>""" + str(dataItem[0]) + """
</li>
"""


def view_questions(request, response):
    data = db.view_questions_pyExam()
    list2 = list(map(generateList, data))
    finalList = ''.join(list2)
    htmlCode = """<html><head><title>Nemo</title><style type="text/css">
body {
color: darkblue;
background-color: lightgrey
}
</style>
</head>
<body>
<ol>%s</ol></body></html>""" %(finalList)
    return server.send_html_handler(request, response, htmlCode)


def admin(request, response):
    data = """
<a href='/add-a-question'>Add Question</a>
<a href='/view-questions'>View Question</a>
"""
    return server.send_html_handler(request,response, data)


def login(request, response):
    data = """
<a href='/admin'>submit</a>
"""
    return server.send_html_handler(request, response, data)


if __name__ == "__main__":
    build_routes()
    server.start_server("localhost", 5555)
