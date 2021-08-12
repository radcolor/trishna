import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, UnicodeText, Integer, String, Boolean

DB_URI = os.getenv("DB_URI")


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()


class Student(BASE):
    __tablename__ = "studetn"
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name


student1 = Student("001", "Joseph John")

SESSION.add(student1)
SESSION.commit()