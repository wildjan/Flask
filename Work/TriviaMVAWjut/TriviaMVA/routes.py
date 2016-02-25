from flask import Flask, url_for, request, render_template
from app import app
import redis

# connect to redis data store
r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

# server/
@app.route('/')
def hello():

    createLink = "<a href='" + url_for('create') + "'>Create a question</a>"
    print(createLink)
    return """<html>
                <head>
                    <title>Hello world!</title>
                    <body>
                        """ + createLink + """
                    </body>
                </head>
            </html>"""

# server/create
@app.route('/create', methods=['GET', 'POST']) 
def create():
    if request.method == 'GET':
        # send the user the form
        return render_template('CreateQuestion.html')
    elif request.method == 'POST':
        # read form data and save it
        title = request.form['title']
        question = request.form['question']
        answer = request.form['answer']

        print(title, question, answer)
        # store data in data store
        # Key name will be whatever title they typed in : Question
        # e.g. music:question countries:question
        # e.g. music:answer countries:answer

        r.set(title + ':question', question)
        r.set(title + ':answer', answer)

        return render_template('CreatedQuestion.html',question=question)
    else:
        return '<h2>Invalid request</h2>'

# server/question/<title>
@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        question = r.get(title + ':question')
        return render_template('AnswerQuestion.html', question = question)
    elif request.method == 'POST':
        submittedAnswer = request.form['submittedAnswer']
        answer = r.get(title + ':answer')
        
        if submittedAnswer == answer:
            return render_template('Correct.html')
        else:
           return render_template('Incorrect.html', answer = answer, submittedAnswer = submittedAnswer)
        