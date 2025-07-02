from flask import Blueprint, render_template, request, redirect, flash, session, current_app
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cur = current_app.mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    if result and check_password_hash(result[0], password):
        session['user'] = username
        return redirect('/dashboard')
    else:
        flash('Invalid login')
        return redirect('/')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
