from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import TaskForm
from app.task.models import TaskModel, task_session  # Use task_session

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/display', methods=['GET', 'POST'])
@login_required
def index():
    tasks = task_session.query(TaskModel).filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

@task_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TaskForm()
    if form.validate_on_submit():
        task = TaskModel(title=form.title.data, description=form.description.data, user_id=current_user.id)
        task_session.add(task)
        task_session.commit()
        flash('Task added successfully')
        return redirect(url_for('task_bp.index'))
    return render_template('add_task.html', form=form)

@task_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    task = task_session.query(TaskModel).filter_by(id=id).first()
    if task:
        task_session.delete(task)
        task_session.commit()
        flash('Task deleted successfully')
    return redirect(url_for('task_bp.index'))
