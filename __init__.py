# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from classes.user import User

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with your secret key

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(int(user_id))

    with app.app_context():
        from .routes import booking_controller, authentication_controller
        app.register_blueprint(booking_controller.app)
        app.register_blueprint(authentication_controller.app)
        return app