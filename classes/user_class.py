# app/models.py
from flask_login import UserMixin
from .sql_class import *
from . import *

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.is_authenticated = False
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def get_user_by_id(cls, id):
        try:
            users = run_query_get(f"SELECT * FROM Users WHERE [id] = {id}")
            if len(users) > 1:
                return {'status':"error", 'message':f"Multiple users found with id {id}."}
            elif len(users) == 0:
                return {'status':"error", 'message':f"User with id {id} not found."}
            else:
                return {'status':'Success', 'result': User.from_dict(users[0]['dictionary'])}
        except Exception as e:
            return {'status':"error", 'message':str(e)}
    
    @classmethod
    def get_user_by_username(cls, username):
        try:
            users = run_query_get(f"SELECT * FROM Users WHERE [username] = '{username}'")
            if len(users) > 1:
                return {'status':"multiple_users_found", 'message':f"Multiple users found for {username}."}
            elif len(users) == 0:
                return {'status':"not_found", 'message':f"User for {username} not found."}
            else:
                return {'status':'found', 'result': User.from_dict(users[0]['dictionary'])}
        except Exception as e:
            return {'status':"error", 'message':str(e)}
    
    @classmethod
    def create_new_user(cls, username, password):
        try:
            user = User.get_user_by_username(username)
            if user['status']=='not_found':
                run_query_post('''
                    INSERT INTO Users (username, password)
                    VALUES (?, ?)
                ''', (username, password))
                return {'status':'created', 'result': User.get_user_by_username(username)['result']}
            else:
                return {'status':'found', 'message':f"User {username} already exists"}
        except Exception as e:
            return {'status':"error", 'message':str(e)}
    
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