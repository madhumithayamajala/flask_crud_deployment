from settings import db
from sqlalchemy.orm import validates
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    # email = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(500))
    mobile_number = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, 'Invalid email address'
        return email

    def __str__(self):
        return self.first_name + self.email + str(self.mobile_number)
