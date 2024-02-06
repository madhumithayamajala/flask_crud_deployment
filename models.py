from settings import db
from sqlalchemy import Column, Integer, Text
from datetime import datetime
#

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60))
    password = db.Column(db.String(500))
    mobile_number = db.Column(db.String(300))

    def __str__(self):
        return self.name + self.email + str(self.mobile_number)
