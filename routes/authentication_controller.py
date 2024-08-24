# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from classes.user import User

app = Blueprint('authentication_controller', __name__, url_prefix='/auth')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('booking_controller.index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add user registration logic here
        flash('User registered successfully')
        return redirect(url_for('auth.login'))
    return render_template('register.html')