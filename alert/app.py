from flask import Flask

from alert.blueprints.application.routes import application


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_object("config.settings")

    app.register_blueprint(application)

    return app
