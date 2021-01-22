from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    tags = Column(String)
    user_id = Column(Integer)

    # user = relationship("User", back_populates="question")
    answers = relationship("Answer")
    

class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    user_id = Column(Integer)
    body = Column(String)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    display_name = Column(String)
    
