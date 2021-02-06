from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine

metadata = MetaData()
Base = declarative_base()
db_string = "postgres+psycopg2://postgres:example@172.17.0.1:5433/mytestdb2"

engine = create_engine(db_string, echo=True)

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

Base.metadata.create_all(engine)
session = Session(engine)
session.add(Question(body="asdf"))
session.commit()
session.close()