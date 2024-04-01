from flask import Flask

from alert.handlers import health, home


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_object("config.settings")

    app.config["SECRET_KEY"] = "supersecretunguessablekey"

    app.add_url_rule("/", "home", home, methods=["GET", "POST"])
    app.add_url_rule("/health", "health", health)

    return app
