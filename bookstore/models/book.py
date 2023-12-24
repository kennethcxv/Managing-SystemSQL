from . import db

class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255))
    Author = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Stock = db.Column(db.Integer)
    OutOfPrint = db.Column(db.Boolean)
