import datetime
import logging

import jwt
from flask import current_app
from project.extensions import bcrypt, db

log = logging.getLogger(__name__)

class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

class Files(db.Model,TimestampMixin):

    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    extension = db.Column(db.String(10), unique=True)
    data = db.Column(db.LargeBinary)

    def __init__(self,
                 name: str,
                 extension: str,
                 data: bytes):
        self.name = name
        self.extension = extension
        self.data = data

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'extension': self.extension,
        }
