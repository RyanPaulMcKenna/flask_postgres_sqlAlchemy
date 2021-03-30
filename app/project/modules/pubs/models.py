import datetime
import logging
from project.extensions import db

log = logging.getLogger(__name__)

class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

class Pubs(db.Model,TimestampMixin):

    __tablename__ = "pubs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    author = db.Column(db.String(128), db.ForeignKey('users.username'))
    text = db.Column(db.Text(), nullable=False)


    def __init__(self,
                 name: str,
                 text: str,
                 author: str):
        self.name = name
        self.text = text
        self.author = author

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'text': self.text
        }
