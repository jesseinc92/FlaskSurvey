from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def survey_start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', survey_title=title, survey_instructions=instructions)

@app.route('/question/<int:id>')
def survey_question(id):
    question = satisfaction_survey.questions[id]
    q = question.question
    id += 1
    return render_template('question.html',
        survey_question=q,
        responses=responses,
        choice1=question.choices[0],
        choice2=question.choices[1])

@app.route('/answer', methods=['POST'])
def add_answer():
    test = request.form['choice']
    responses.append(test)
    return redirect(url_for('survey_question', id=len(responses)))