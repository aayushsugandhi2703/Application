from flask import Flask, Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models import Task, Session
from app.forms import TaskForm

task_bp = Blueprint('task', __name__)

@task_bp.route('/add', methods=['GET'])
# This function will redirect the user to the task page only if the user is logged in
@jwt_required()
def add():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data)
        Session.add(task)
        Session.commit()
        flash('Task added successfully')
        return redirect(url_for('task.add'))
    else:
        Session.rollback()
        flash('Task addition failed')
    return render_template('task.html', form=form)