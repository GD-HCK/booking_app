# app/models.py
from flask_login import UserMixin
from .sql_class import run_query_get, run_query_post
from ..db_context import db
import uuid

class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, username, password, is_authenticated=False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.is_authenticated = is_authenticated
    
    def get_id(self):
        return self.user_id
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def get_user_by_user_id(cls, user_id):
        try:
            user = cls.query.filter_by(user_id=user_id).first()
            if user:
                return {'status': 'success', 'result': user}
            else:
                return {'status': 'error', 'message': f"User with user_id {user_id} not found."}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @classmethod
    def load_user_by_user_id(cls, user_id):
        try:
            user = cls.query.filter_by(user_id=user_id).first()
            if user:
                return user
            else:
                return User(None,None,None,False)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    
    @classmethod
    def get_user_by_username(cls, username):
        try:
            user = cls.query.filter_by(username=username).first()
            if user:
                return {'status': 'found', 'result': user}
            else:
                return {'status': 'not_found', 'message': f"User for {username} not found."}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    
    @classmethod
    def create_new_user(cls, username, password):
        try:
            user = cls.get_user_by_username(username)
            if user['status'] == 'not_found':
                new_user = cls(user_id=str(uuid.uuid4()), username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return {'status': 'created', 'result': new_user}
            else:
                return {'status': 'error', 'message': f"User with username {username} already exists."}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @classmethod
    def update_user(cls, user_id, property, value):
        try:
            user = User.get_user_by_user_id(user_id)
            if user['status']=='found':
                run_query_post("UPDATE Users SET [?] = '?'", (property, value))
                return {'status':'updated', 'result': User.get_user_by_user_id(user_id)['result']}
            else:
                return {'status':'not_found', 'message':f"User with {user_id} does not exists"}
        except Exception as e:
            return {'status':"error", 'message':str(e)}