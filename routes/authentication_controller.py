# app/routes/authentication_controller.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..classes.user_class import *

# url_prefix='/authentication'
app = Blueprint('authentication_controller', __name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This is an example endpoint that returns a User object'
    ---
    tags:
        - Greetings
    description: Returns a friendly greeting.
    responses:
        200:
            description: A successful response
            examples:
                application/json: "Hello, World!"
    """
    # if current_user['status'] == 'success':
    #         if current_user['result'].is_authenticated:
    #             return redirect(url_for('booking_controller.index'))
    if current_user.is_authenticated:
            return redirect(url_for('booking_controller.index'))
                        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = User.get_user_by_username(username)
        if result['status'] == 'found':
            if result and result['result'].password == password:
                login_user(result['result'])
                User.update_user(result['result'].user_id, 'is_authenticated', True)
                return redirect(url_for('booking_controller.index'))
            flash('Invalid username or password')
        else:
            flash(result['message'])
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication_controller.login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('booking_controller.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = User.create_new_user(username, password)
        if result['status'] == 'created':
            flash('User registered successfully')
        else:
            flash(result['message'])
        return redirect(url_for('authentication_controller.login'))
    return render_template('register.html')