import json
import pyodbc
from flask import Flask
from flask_login import LoginManager
from .classes.user_class import User
from .routes.booking_controller import app as booking_controller
from .routes.authentication_controller import app as authentication_controller
from .routes.index_controller import app as index_controller
from flask_sqlalchemy import SQLAlchemy

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

conn_str = get_connection_string()

def run_query_get(query: str, *params) -> list:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    results = cursor.fetchall()
    result_list = []
    for result in results:
        dictionary = dict(zip([column[0] for column in cursor.description], result))
        values = result
        result_list.append({'dictionary': dictionary, 'values': values})
    conn.close()
    return result_list

def run_query_post(query: str, *params) -> int:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    conn.commit()
    conn.close()
    return 1

app = Flask(__name__)
app.secret_key = get_secret_key()

app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dbcontext = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'authentication_controller.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(int(user_id))

with app.app_context():
    dbcontext.create_all()
    app.register_blueprint(booking_controller, url_prefix='/bookings')
    app.register_blueprint(authentication_controller, url_prefix='/authentication')
    app.register_blueprint(index_controller)