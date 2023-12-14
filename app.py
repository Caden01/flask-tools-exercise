from flask import Flask, flash, render_template,  redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def home() :
    return render_template("home.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey() :
    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def show_question(question_id) :

    if responses is None :
        return redirect("/")

    if len(responses) == len(survey.questions) :
        return redirect("/complete")

    if len(responses) != question_id :
        flash("You can't skip ahead.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[question_id]
    return render_template("question.html", question_num=question_id, question=question)


@app.route("/answer", methods=["POST"])
def handle_answers() :

    choice = request.form["answer"]

    responses.append(choice)

    if len(responses) == len(survey.questions) :
        return redirect("/complete")
    else :
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def show_complete():
    return render_template("show_complete.html")
