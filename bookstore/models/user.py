from . import db

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Password = db.Column(db.String(255))
    Name = db.Column(db.String(255))
    Email = db.Column(db.String(255), unique=True)
    UserType = db.Column(db.Enum('Admin', 'Customer'), default='Customer')
