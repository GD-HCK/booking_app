# app.py
from flask import Blueprint, request, jsonify, render_template
app = Blueprint('index_controller', __name__)

@app.route('/')
def index():
    return render_template('index.html')