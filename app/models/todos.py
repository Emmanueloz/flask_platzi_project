from app.utils.db import db


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(100))

    def __init__(self, id_user, description) -> None:
        self.id_user = id_user
        self.description = description
