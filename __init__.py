# app/__init__.py
import json
from flask import Flask
from flask_login import LoginManager
from classes.user_class import User

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

def get_secret_key():
    config = load_config()
    return config['security']['secret_key']

def create_app():
    app = Flask(__name__)
    app.secret_key = get_secret_key()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(int(user_id))

    with app.app_context():
        from .routes import booking_controller, authentication_controller, index_controller
        app.register_blueprint(booking_controller.app)
        app.register_blueprint(authentication_controller.app)
        app.register_blueprint(index_controller.app)
        return app