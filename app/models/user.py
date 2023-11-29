from app.utils.db import db
from flask_login import UserMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    passwd = db.Column(db.String(100))

    def __init__(self, username, passwd) -> None:
        self.username = username
        self.passwd = passwd


class UserLogin(UserMixin):
    def __init__(self, id, username, passwd) -> None:
        self.id = id
        self.username = username
        self.passwd = passwd

    @staticmethod
    def query(user_name):
        user: User = User.query.get(user_name)
        print(user.id)
        return UserLogin(user.id, user.username, user.passwd)
