from sqlalchemy import Column, UnicodeText
from sqlalchemy.sql.elements import Null
from TrishnaBot.modules.sql.__init__ import SESSION, BASE


class RSS(BASE):
    __tablename__ = "rss_records"
    name = Column(UnicodeText, primary_key=True)
    value = Column(UnicodeText, nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value


RSS.__table__.create(checkfirst=True)


def RSSRECORDS(name, value):
    record = RSS(name, value)
    SESSION.add(record)
    SESSION.commit()


def get_name(value):
    for instance in SESSION.query(RSS).filter_by(value=value):
        return instance.name


def get_value(name):
    for instance in SESSION.query(RSS).filter_by(name=name):
        return instance.value


def update_value(name, new_value):
    record = SESSION.query(RSS).filter_by(name=name).first()
    if record is None:
        # Initialize the record if not found
        RSSRECORDS(name, new_value)
    else:
        # Update the values from the record if found
        record.value = new_value
    SESSION.commit()