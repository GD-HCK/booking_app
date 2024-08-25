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
    def get_user(cls, property, value):
        try:
            if type(value) is int:
                user = [run_query_get(f"SELECT * FROM Users WHERE id = {value}")]
            if type(value) is str:
                user = [run_query_get(f"SELECT * FROM Users WHERE [{property}] = '{value}'")]
            if len(user) > 1:
                return {'status':"Error", 'message':"Multiple users found."}
            elif len(user) > 0:
                return {'status':"Error", 'message':"User not found."}
            else:
                return {'status':'Success', 'result': User.from_dict(user[0][0])}
        except Exception as e:
            return {'status':"Error", 'message':str(e)}
    
    @classmethod
    def create_new_user(cls, username, password):
        try:
            run_query_post('''
                INSERT INTO Users (username, password)
                VALUES (?, ?)
            ''', (username, password))
            return 1
        except Exception as e:
            return {'status':"Error", 'message':str(e)}