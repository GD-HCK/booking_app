# app.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
app = Blueprint('index_controller', __name__)

@app.route('/')
@login_required
def index():
    return render_template('index.html')