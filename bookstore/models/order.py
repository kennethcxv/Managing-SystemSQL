from . import db

class Order(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'))
    Quantity = db.Column(db.Integer)
