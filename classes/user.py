# app/models.py
from flask_login import UserMixin
from classes.configuration import *
import pyodbc

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
    def get_user(cls, id):
        return [run_query_get(f"SELECT * FROM Users WHERE id = '{id}'")]