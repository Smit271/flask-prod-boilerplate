# Standard Imports
from os import environ
# 3rd Party Imports
from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import inspect
from celery import Celery
from dotenv import load_dotenv
# Local Imports
from app.helpers.response_helpers import error_response
from app.config import config as app_config
from app.extension import db
from app.middleware.authentication import CustomMiddleware

celery = Celery(__name__)


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Get application environment
    APPLICATION_ENV = get_environment()

    # Initialize Flask app
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)

    # Configure app
    app.config.from_object(app_config[APPLICATION_ENV])

    # Check if the database URI is set correctly
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise ValueError(
            "SQLALCHEMY_DATABASE_URI is not set in the configuration.")

    # Configure CORS
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    # Configure Celery
    celery.config_from_object(app.config, force=True)
    celery.conf.update(result_backend=app.config.get(
        'RESULT_BACKEND', 'redis://localhost:6379/0'))

    # Initialize Flask extensions
    db.init_app(app)

    with app.app_context():
        # Create tables
        db.create_all()

        # List table names
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        print("Tables created:", table_names)

    # Register Blueprints
    from app.test_app.views import test_app as test_app_blueprint

    app.register_blueprint(test_app_blueprint, url_prefix='/api/v1/test-app')

    # Registering middlewares
    app.wsgi_app = CustomMiddleware(app.wsgi_app)

    # CUSTOM ERROR HANDLER FOR 404 NOTFOUND ERROR
    @app.errorhandler(404)
    def handle_base_error(error):
        return error_response("NOT FOUND", 404, {})

    # DEFAULT ERROR HANDLER FOR ALL UNHANDLED EXCEPTIONS
    @app.errorhandler(Exception)
    def default_exception_handler(error):
        """
        default_error_handler: If not the custom/base error raise error.
        Args:
            error (obj): Error object.
        """
        return error_response("Internal Server Error", error.status_code, error.to_dict())

    @app.before_request
    def before_request():
        # Middleware for before request to call.
        pass

    return app


def get_environment():
    """Fetch the application environment from environment variables."""
    return environ.get('APPLICATION_ENV', 'development')
