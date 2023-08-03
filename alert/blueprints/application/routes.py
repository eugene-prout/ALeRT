from flask import Blueprint, render_template


application = Blueprint("user", __name__)


@application.route("/")
def home():
    return render_template("application/home.html")


@application.route("/health")
def health():
    return {"status": "healthy"}, 200
