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
    def __init__(self, user_data: User) -> None:
        self.id = user_data.id
        self.username = user_data.username
        self.passwd = user_data.passwd

    @staticmethod
    def query(user_name):
        user = User.query.filter(User.username == user_name).all()
        return UserLogin(user)
