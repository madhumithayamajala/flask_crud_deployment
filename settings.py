import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# app settings
app = Flask(__name__)
app.config["DEBUG"] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://madhuuser:madhuuser@madhuuser.cfsqyk4ui4co.ap-south-1.rds.amazonaws.com/madhuuser'

db = SQLAlchemy(app)

migrate = Migrate(app, db)
