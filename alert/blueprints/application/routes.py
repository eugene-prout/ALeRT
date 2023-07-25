from flask import Blueprint, render_template
from flask_babel import _


application = Blueprint("user", __name__)


@application.route("/")
@application.route("/home")
def home():
    return render_template("application/home.html")


@application.route("/health")
def health():
    return {"status": "healthy"}, 200
