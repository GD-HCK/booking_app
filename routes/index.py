# app.py
from flask import Blueprint, request, jsonify, render_template
app = Blueprint('index', __name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<num>')
def user(num):
    return render_template('hello.html', num=num)