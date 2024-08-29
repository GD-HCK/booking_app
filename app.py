import json
from flask import Flask
from flask_login import LoginManager
from .classes.user_class import User
from .routes.booking_controller import app as booking_controller
from .routes.authentication_controller import app as authentication_controller
from .routes.index_controller import app as index_controller
from .db_context import db
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app, template={
        "info": {
            "title": "My Flask API",
            "description": "An example API using Flask and Swagger",
            "version": "1.0.0"
        }
    })

    file_path='config.json'
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    
    sql_alchemy_conn_string = f'mssql+pyodbc://{config['connection_string']['username']}:{config['connection_string']['password']}@{config['connection_string']['server']}/{config['connection_string']['database']}?driver={config['connection_string']['driver'].replace(" ", "+")}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_alchemy_conn_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.secret_key = get_secret_key()
    app.config['SECRET_KEY'] = config['security']['secret_key']

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'authentication_controller.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.load_user_by_user_id(user_id)

    with app.app_context():
        db.create_all()

    app.register_blueprint(booking_controller)
    app.register_blueprint(authentication_controller)
    app.register_blueprint(index_controller)

    return app


if __name__ == '__main__':
    create_app().run()