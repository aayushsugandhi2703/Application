from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from app.task.models import TaskModel

# Create engine and session for user database
user_engine = create_engine('sqlite:///userdb.db')
Base = declarative_base()
UserSession = sessionmaker(bind=user_engine)

class UserModel(UserMixin, Base):
    __tablename__ = 'USER'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    tasks = relationship('TaskModel', back_populates='user')

# Create all tables in user database
Base.metadata.create_all(user_engine)

# Create a session instance
user_session = UserSession()
