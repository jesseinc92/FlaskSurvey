from flask import Flask, request, render_template, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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

    if id < len(satisfaction_survey.questions):
        return render_template('question.html',
            survey_question=q,
            responses=responses,
            choice1=question.choices[0],
            choice2=question.choices[1])
    elif id != len(responses)-1:
        flash("You're trying to answer the wrong question.")
        return redirect(url_for('survey_question', id=len(responses)))
    elif len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('thank_you'))


@app.route('/answer', methods=['POST'])
def add_answer():
    test = request.form['choice']
    responses.append(test)
    return redirect(url_for('survey_question', id=len(responses)))


@app.route('/thank-you')
def thank_you():
    return render_template('thanks.html')