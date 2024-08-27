# app/models.py
from flask_login import UserMixin
from .sql_class import run_query_get, run_query_post
from ..db_context import db

class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, id, username, password, is_authenticated=False):
        self.id = id
        self.username = username
        self.password = password
        self.is_authenticated = is_authenticated
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def get_user_by_id(cls, id):
        try:
            user = cls.query.filter_by(id=id).first()
            if user:
                return {'status': 'success', 'result': user}
            else:
                return {'status': 'error', 'message': f"User with id {id} not found."}
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
                new_user = cls(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return {'status': 'Success', 'result': new_user}
            else:
                return {'status': 'error', 'message': f"User with username {username} already exists."}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @classmethod
    def update_user(cls, id, property, value):
        try:
            user = User.get_user_by_id(id)
            if user['status']=='found':
                run_query_post("UPDATE Users SET [?] = '?'", (property, value))
                return {'status':'updated', 'result': User.get_user_by_id(id)['result']}
            else:
                return {'status':'not_found', 'message':f"User with {id} does not exists"}
        except Exception as e:
            return {'status':"error", 'message':str(e)}