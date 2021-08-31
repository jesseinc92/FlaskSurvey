from flask import Flask, request, render_template
from surveys import satisfaction_survey

app = Flask(__name__)

responses = []

@app.route('/')
def survey_start():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', survey_title=title, survey_instructions=instructions)

@app.route('/question/<int:id>')
def survey_question(id):
    question = satisfaction_survey.questions[id].question
    next_id = id + 1
    return render_template('question.html', survey_question=question, action_id=next_id)