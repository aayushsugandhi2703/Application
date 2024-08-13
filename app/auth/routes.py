from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import UserForm
from app.auth.models import UserModel, user_session  
from app.task.models import TaskModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('task_bp.index'))
    form = UserForm()
    if form.validate_on_submit():
        user = user_session.query(UserModel).filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('task_bp.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        existing_user = user_session.query(UserModel).filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken, please choose another')
            return redirect(url_for('auth.register'))
        
        user = UserModel(username=form.username.data, password=form.password.data)
        user_session.add(user)
        user_session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
