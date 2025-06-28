from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message="Username is required."),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required.")
    ])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message="Username is required."),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required.")
    ])
    submit = SubmitField('Register')

class TaskForm(FlaskForm):
    content = StringField('New Task', validators=[
        InputRequired(message="Task content is required.")
    ])
    submit = SubmitField('Add Task')
