from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists (create if missing)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        # Optional: print or log this if needed
        print(f"Error creating instance folder: {e}")

    # Load config from instance/config.py
    app.config.from_pyfile('config.py')

    # Fix relative SQLite path to absolute path inside instance folder
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    if uri.startswith('sqlite:///') and not os.path.isabs(uri[10:]):
        db_path = os.path.join(app.instance_path, uri[10:])
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
