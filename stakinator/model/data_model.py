from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Serializer():
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Question(Base, Serializer):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    tags = Column(String)
    user_id = Column(Integer)

    # user = relationship("User", back_populates="question")
    answers = relationship("Answer")
    

class Answer(Base, Serializer):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    user_id = Column(Integer)
    body = Column(String)


class User(Base, Serializer):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    display_name = Column(String)

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}



    # def serialize(self):
    #     {"User":{
    #         "id": 
    #     }}
    
