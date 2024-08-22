from flask import Flask, Blueprint, render_template, redirect, url_for, flash, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from app.models import User, Session
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

# This function will redirect the user to the login page
@auth_bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.Login'))

# This function and route is for the user to login 
@auth_bp.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    # If the form is submitted and validated, the user will be redirected to the task page
    if form.validate_on_submit(): 
        user = Session.query(User).filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:

            # Create the access and refresh tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = make_response(redirect(url_for('task.add')))
            response.set_cookie('access_token', access_token)
            return response  
            # return jsonify(access_token=access_token, refresh_token=refresh_token)
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# This function and route is for the user to register
@auth_bp.route('/register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()

    # If the form is submitted and validated, the user will be redirected to the login page
    if form.validate_on_submit():  
        user = User(username=form.username.data, password=form.password.data)
        Session.add(user)
        Session.commit()
        flash('User created successfully')
        return redirect(url_for('auth.Login'))
    else:
        Session.rollback()
        flash('User creation failed')
    return render_template('signup.html', form=form)

# This function and route is for the user to logout
@auth_bp.route('/logout', methods=['GET'])  
@jwt_required()
def Logout():
    response = jsonify(msg='Logged out successfully')
    response.delete_cookie('access_token')
    return response, 200
