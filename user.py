import server
import db
import json

score=0

# def makeTemplate(q,qno,opt1,opt2,opt3,opt4):
#     # r = []
#     # r.append(qno)
#     with open("./public/html/pyExam.html", "r") as file_descriptor:
#             res = file_descriptor.read()
#     result = res.format(q,opt1,opt2,opt3,opt4)
#     # r.append(result)
#     return result

# def makeQuestionBlocks(questObj):
#     # print(questObj)
#     q = questObj[0]["Question"]
#     qno = questObj[0]["QNo"]
#     opt1 = questObj[0]["AnsOpt1"]
#     opt2 = questObj[0]["AnsOpt2"]
#     opt3 = questObj[0]["AnsOpt3"]
#     opt4 = questObj[0]["AnsOpt4"]
#     return makeTemplate(q,qno,opt1,opt2,opt3,opt4)

def showQuestionPost(request, response):
    # request['content']['Opt']
    data = db.show_Quest_pyExam()
    # htmlcode = makeQuestionBlocks(data)
    # htmlcode = val[1]
    return server.send_html_handler(request, response, data)



def showQuestion(request, response):
    # print("\n\n\nrequest",request['content'])
    data = db.show_Quest_pyExam()
    # htmlcode = makeQuestionBlocks(data)
    # json_data = json.dumps(dict(data))
    # json_data = json.dumps(data)
    # print(json_data)
    # json_obj = json.loads(json_data)
    # global score
    # data1 = json.loads(json_data)
    # htmlcode = """<html>
    # <head>
    # <title>Python Proficiency Test</title>
    # </head>
    # <body>
    #     %s<br>
    #     <br>
    #     <form action="/testPython" method="POST">
    #         <input type="radio" name="Opt" value=1 checked>%s<br>
    #         <input type="radio" name="Opt" value=2>%s<br>
    #         <input type="radio" name="Opt" value=3>%s<br>
    #         <input type="radio" name="Opt" value=4>%s<br>
    #         <br>
    #         <button type='submit'>Submit</button>
    #     </form>
    # </body>
    # </html>""" %(data['Question'],data['AnsOpt1'],data['AnsOpt2'],data['AnsOpt3'],data['AnsOpt4'])
    return server.send_json_handler(request, response, data)

#def showNextQuestion(request,response):
    #global qnum
    #qnum+=1
    #data = db.show_question_pyExam(qnum)
    #htmlcode = """<html>
    #<head>
    #<title>Python Proficiency Test</title>
    #</head>
    #<body>
        #%s<br>
        #<br>
        #<form action="/next-question" method="POST">
            #<input type="radio" name="Opt" value=1 checked>%s<br>
            #<input type="radio" name="Opt" value=2>%s<br>
            #<input type="radio" name="Opt" value=3>%s<br>
            #<input type="radio" name="Opt" value=4>%s<br>
            #<br>
            #<button type='submit'>Submit</button>
        #</form>
    #</body>
    #</html>""" %(data[1],data[2],data[3],data[4],data[5])
    #return server.send_html_handler(request, response, htmlcode)
