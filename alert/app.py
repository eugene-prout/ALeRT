from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

from alert.blueprints.application.routes import application


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)
    
    app.config.from_object("config.settings")

    bootstrap.init_app(app)

    app.register_blueprint(application)

    

    return app
