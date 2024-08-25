# from . import *

# app = create_app()

# app/__init__.py
import json
from flask import Flask
from flask_login import LoginManager
from .classes.user_class import User
from .routes.booking_controller import app as booking_controller
from .routes.authentication_controller import app as authentication_controller
from .routes.index_controller import app as index_controller

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)

def get_secret_key():
    config = load_config()
    return config['security']['secret_key']

app = Flask(__name__)
app.secret_key = get_secret_key()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'authentication_controller.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_user(int(user_id))

app.register_blueprint(booking_controller, url_prefix='/bookings')
app.register_blueprint(authentication_controller, url_prefix='/authentication')
app.register_blueprint(index_controller)

# if __name__ == '__main__':
#     app.run(debug=True)