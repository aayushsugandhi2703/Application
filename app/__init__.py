from flask import Flask
from flask_login import LoginManager
from app.auth.routes import auth_bp
from app.task.routes import task_bp
from app.auth.models import UserModel, user_session  # Ensure user_session is imported
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You need to login to access this page'
    login_manager.init_app(app)

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return user_session.query(UserModel).filter_by(id=user_id).first()

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)  # Ensure this matches the blueprint name

    return app
