from app import db, login
from flask_login import UserMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Reminder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return "<Reminder '{}'>".format(self.text[:20])
  
