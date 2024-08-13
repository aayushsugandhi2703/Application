from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from app.auth.models import UserModel

# Create engine and session for task database
task_engine = create_engine('sqlite:///taskdb.db')
Base = declarative_base()
TaskSession = sessionmaker(bind=task_engine)

class TaskModel(UserMixin, Base):
    __tablename__ = 'TASK'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey('USER.id'), nullable=False)

    user = relationship('UserModel', back_populates='tasks')

# Create all tables in task database
Base.metadata.create_all(task_engine)

# Create a session instance
task_session = TaskSession()
