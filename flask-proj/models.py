from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Menu(db.model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer)
    name = db.Column(db.String(32))
    price = db.Column(db.Integer)