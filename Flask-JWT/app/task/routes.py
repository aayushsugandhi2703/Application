from flask import Flask, Blueprint, render_template, redirect, url_for, jsonify, make_response, session, flash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from app.models import User, Session, Task
from app.forms import TaskForm

task_bp = Blueprint('task', __name__)

@task_bp.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.Login'))
    
    form = TaskForm()
    if form.validate_on_submit():
            try:
                task = Task(title=form.title.data,user_id=session['user_id'])
                Session.add(task)
                Session.commit()
                flash('Task added successfully')
                return redirect(url_for('task.get_tasks'))
            except Exception as e:
                flash(f'Task addition failed: {str(e)}')
                Session.rollback()
    return render_template('task.html', form=form)

@task_bp.route('/display', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    
    # Rollback if there's any uncommitted session state (though it's not usually necessary here)
    Session.rollback()
    
    tasks = Session.query(Task).filter_by(user_id=user_id).all()
    tasks_json = [{'id': task.id, 'title': task.title} for task in tasks]
    
    return jsonify(tasks_json)

@task_bp.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    if 'user_id' in session:
        user_id = session['user_id']
    task = Session.query(Task).filter_by(user_id=user_id).filter_by(id=id).first()
    Session.delete(task)
    Session.commit()
    flash('Task deleted successfully')
    return redirect(url_for('task.get_tasks'))