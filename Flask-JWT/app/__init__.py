from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurations
    from config import Config
    app.config.from_object(Config)

    # Initialize JWT with the app
    from flask_jwt_extended import JWTManager
    
    jwt = JWTManager(app)

    # Import and register blueprints
    from app.auth.routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix='/')

    return app
