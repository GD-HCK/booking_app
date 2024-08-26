import json
from flask import Flask
from flask_login import LoginManager
from .classes.user_class import User
from .routes.booking_controller import app as booking_controller
from .routes.authentication_controller import app as authentication_controller
from .routes.index_controller import app as index_controller
from .db_context import db 

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()

def get_connection_string():
    return (
        f"DRIVER={config['connection_string']['driver']};"
        f"SERVER={config['connection_string']['server']};"
        f"DATABASE={config['connection_string']['database']};"
        f"UID={config['connection_string']['username']};"
        f"PWD={config['connection_string']['password']}"
    )

def get_sqlalchemy_connection_string():
    return f'mssql+pyodbc://{config['connection_string']['username']}:{config['connection_string']['password']}@{config['connection_string']['server']}/{config['connection_string']['database']}?driver={config['connection_string']['driver'].replace(" ", "+")}'

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

def get_secret_key():
    config = load_config()
    return config['security']['secret_key']

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.secret_key = get_secret_key()
    app.config['SECRET_KEY'] = get_secret_key()

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'authentication_controller.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_by_id(int(user_id))

    with app.app_context():
        db.create_all()

    app.register_blueprint(booking_controller)
    app.register_blueprint(authentication_controller)
    app.register_blueprint(index_controller)

    return app


if __name__ == '__main__':
    create_app().run()