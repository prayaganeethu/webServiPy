import server
import admin
import user

def build_routes():
    server.add_route('get', '/admin', adminPage)
    server.add_route('get','/user',userPage)
    server.add_route('get', '/login', login)
    server.add_route('get', '/add-a-question', admin.add_a_question)
    server.add_route('post','/add-a-question', admin.add_a_question_post)
    server.add_route('get', '/view-questions', admin.view_questions)
    server.add_route('get', '/testPython', user.showQuestion)
    server.add_route('post', '/testPython', user.showQuestionPost)
    #server.add_route('post','/next-question',user.showNextQuestion)

def userPage(request, response):
    htmlCode = """<html>
<head>
    <title>Python Proficiency Test</title>
    <style type="text/css">
        body {
        color: darkblue;
        background-color: lightgrey
        }
    </style>
</head>
<body>
    <h1>Python Exam</h1>
    <p>Click Enter to start</p>
    <a href='/testPython'>Enter</a>
</body>
</html>"""
    return server.send_html_handler(request,response, htmlCode)

def adminPage(request, response):
    with open("./public/html/pyAdmin.html", "rb") as file_descriptor:
            res = file_descriptor.read()
    return server.send_html_handler(request,response,res)
#     data = """
# <a href='/add-a-question'>Add Question</a>
# <a href='/view-questions'>View Question</a>
# """
    return server.send_html_handler(request,response,data)


def login(request, response):
    with open("./public/html/pyExamLogin.html", "rb") as file_descriptor:
            res = file_descriptor.read()
    return server.send_html_handler(request,response, res)

if __name__ == "__main__":
    build_routes()
    server.start_server("0.0.0.0", 5558)
