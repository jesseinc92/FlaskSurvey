from flask import Flask, request, render_template, redirect, flash, session
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


@app.route('/start', methods=['POST'])
def session_start():
    session['responses'] = []
    responses = []

    return redirect('/question/0')


@app.route('/question/<int:qid>')
def survey_question(qid):
    if session['responses'] is None:
        return redirect('/')

    if qid != len(session['responses']):
        flash("You're trying to answer the wrong question.")
        return redirect(f'/question/{len(session["responses"])}')

    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect('/thank_you')

    question = satisfaction_survey.questions[qid]
    q = question.question
    qid += 1
    return render_template('question.html',
        survey_question=q,
        responses=responses,
        choice1=question.choices[0],
        choice2=question.choices[1])


@app.route('/answer', methods=['POST'])
def add_answer():
    test = request.form['choice']
    responses.append(test)
    session['responses'] = responses

    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect('/thank_you')

    else:
        return redirect(f'/question/{len(session["responses"])}')


@app.route('/thank_you')
def thank_you():
    return render_template('thanks.html')