# app/routes/authentication_controller.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..classes.user_class import *

# url_prefix='/authentication'
app = Blueprint('authentication_controller', __name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('booking_controller.index'))
                        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = User.get_user_by_username(username)
        if result['status'] == 'Success':
            if result and result.password == password:
                login_user(result)
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
        if result['status'] == 'Success':
            flash('User registered successfully')
        else:
            flash(result['message'])
        return redirect(url_for('authentication_controller.login'))
    return render_template('register.html')