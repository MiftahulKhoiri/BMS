 
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

login_manager = LoginManager()

def create_app(config_object="core.config.Config"):
    from core.config import Config

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # Init login system
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Database engine
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    app.db_engine = engine
    app.db_session_factory = SessionLocal

    # Register Blueprint
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    # Create tables
    from app.services.db_service import create_tables
    create_tables(engine)

    return app