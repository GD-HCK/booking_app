# app/models.py
import pyodbc
from flask_login import UserMixin
from . import *

# Database connection string
conn_str = get_connection_string()

def run_query_get(query: str, *params) -> list:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    result = cursor.fetchall()
    conn.close()
    return result

def run_query_post(query: str, *params) -> int:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    conn.commit()
    conn.close()
    return 1

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def get_user_by_id(cls, id):
        try:
            users = [run_query_get(f"SELECT * FROM Users WHERE [id] = {id}")]
            if len(users) > 1:
                return {'status':"Error", 'message':f"Multiple users found with id {id}."}
            elif len(users) == 0:
                return {'status':"Error", 'message':f"User with id {id} not found."}
            else:
                return {'status':'Success', 'result': User.from_dict(users[0])}
        except Exception as e:
            return {'status':"Error", 'message':str(e)}
    
    @classmethod
    def get_user_by_username(cls, username):
        try:
            users = [run_query_get(f"SELECT * FROM Users WHERE [username] = '{username}'")]
            if len(users) > 1:
                return {'status':"Error", 'message':f"Multiple users found for {username}."}
            elif len(users) == 0:
                return {'status':"Error", 'message':f"User for {username} not found."}
            else:
                return {'status':'Success', 'result': User.from_dict(users[0])}
        except Exception as e:
            return {'status':"Error", 'message':str(e)}
    

    @classmethod
    def create_new_user(cls, username, password):
        try:
            user = User.get_user_by_username(username)
            if not user:
                run_query_post('''
                    INSERT INTO Users (username, password)
                    VALUES (?, ?)
                ''', (username, password))
                return {'status':'Success', 'result': User.get_user_by_username(username)}
            else:
                return {'status':'Error', 'message':f"User {username} already exists"}
        except Exception as e:
            return {'status':"Error", 'message':str(e)}