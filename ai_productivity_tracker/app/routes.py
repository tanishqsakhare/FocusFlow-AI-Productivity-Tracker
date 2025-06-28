import random
from flask import Blueprint, render_template, redirect, url_for, flash
from .models import User, Task
from .forms import LoginForm, RegisterForm, TaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db, login_manager

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(f"Login attempt for username: {form.username.data}")
        if user:
            print(f"User found: {user.username}")
            print(f"Stored hashed password: {user.password}")
            print(f"Password entered: {form.password.data}")
            if check_password_hash(user.password, form.password.data):
                print("Password check passed")
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                print("Password check failed")
        else:
            print("User not found")
        flash("Invalid login.")
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(content=form.content.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.timestamp.desc()).all()

    # AI motivational quotes
    quotes = [
        "You are capable of amazing things!",
        "Stay focused — your future self will thank you.",
        "Every small step counts. Keep moving!",
        "Discipline is choosing between what you want now and what you want most.",
        "Progress, not perfection!"
    ]
    motivation = random.choice(quotes)

    return render_template('dashboard.html', form=form, tasks=tasks, motivation=motivation)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/pomodoro')
@login_required
def pomodoro():
    return render_template('pomodoro.html')

@main.route('/toggle_task/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('main.dashboard'))
