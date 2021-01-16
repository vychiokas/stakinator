from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    comments = relationship("Comment", backref='question')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    body = Column(String)