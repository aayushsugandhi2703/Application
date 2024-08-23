from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

engine = create_engine('sqlite:///database.db')

Base = declarative_base()

# Define the User database model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True ,nullable=False)
    password = Column(String(100), nullable=False)
    task = relationship('Task', back_populates='user',cascade='all, delete-orphan')

# Define the Task database model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='task')

session = sessionmaker(bind=engine)

Session = session()

Base.metadata.create_all(engine)
