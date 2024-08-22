from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_jwt_extended import jwt_required
from app.models import Task, Session
from app.forms import TaskForm
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
import jwt

task_bp = Blueprint('task', __name__)

def decode_jwt(token):
    try:
        # Decode the token using the secret key from the current app configuration
        decoded_token = jwt.decode(token, key=current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return decoded_token['identity']
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

@task_bp.route('/add', methods=['GET', 'POST'])
@jwt_required()  # This ensures the route is protected and accessible only with a valid JWT token
def add():
    form = TaskForm()
    if form.validate_on_submit():
        token = request.cookies.get('access_token')
        if token:
            try:
                user_id = decode_jwt(token)  # Custom function to decode and verify the token
                task = Task(title=form.title.data, user_id=user_id)
                Session.add(task)
                Session.commit()
                flash('Task added successfully')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Task addition failed: {str(e)}')
        else:
            flash('Token is missing')
    return render_template('task.html', form=form)
