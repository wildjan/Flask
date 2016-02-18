from flask import Flask, url_for, request, render_template
from app import app

# server/
@app.route('/')
def hello():
    createLink = "<a href'" + url_for('create') + "'>Create a question</a>"
    return """<html>
                <head>
                    <title>Hello world</title>
                    <body>
                        """ + createLink + """
                    </body>
                </head>
            </html>"""

# server/create
@app.route('/create') 
def create():
    if request.method == 'GET':
        # send the user the form
        return render_template('CreateQuestion.html')
    elif request.method == 'POST':
        # read form data and save it
        title = request.form('title')
        answer = request.form('answer')
        question = request.form('question')

        # store data in data store

        return render_template('CreatedQuestion.html', question = question)
    else:
        return '<h2>Invalid request</h2>'

# server/question/<title>
@app.route('/question/<title>')
def question(title):
    return '<h2>' + title + '</h2>' 