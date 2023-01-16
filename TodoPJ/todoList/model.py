from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default= func.now())
    duedate = db.Column(db.DateTime(timezone=True), default= func.now())
    #duein = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    notes = db.relationship("Note")


    def __init__(self, email, password, user_name):
        self.email = email
        self.password= password
        self.user_name = user_name
        


