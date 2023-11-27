from app.utils.db import db
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    passwd = db.Column(db.String(100))

    def __init__(self, username, passwd) -> None:
        self.username = username
        self.passwd = passwd
