from flask import Blueprint, render_template

from alert.forms import EditGrammarForm

application = Blueprint("user", __name__)


@application.route("/")
def home():
    form = EditGrammarForm()
    return render_template("application/home.html",form=form)


@application.route("/health")
def health():
    return {"status": "healthy"}, 200
