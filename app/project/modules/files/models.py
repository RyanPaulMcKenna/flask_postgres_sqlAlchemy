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
    file_name = db.Column(db.String(128), nullable=False, unique=True)
    file_extension = db.Column(db.String(10), unique=True)
    file_data = db.Column(db.LargeBinary)

    def __init__(self,
                 file_name: str,
                 file_extension: str,
                 file_data: bytes):
        self.file_name = file_name
        self.file_extension = file_extension
        self.file_data = file_data

    def to_json(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_extension': self.file_extension,
        }
