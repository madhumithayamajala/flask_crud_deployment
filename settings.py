import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# app settings
app = Flask(__name__)
app.config["DEBUG"] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://madhuuser:madhuuser@madhudb1.cbig68kc8ube.ap-south-1.rds.amazonaws.com/madhudb'

db = SQLAlchemy(app)

migrate = Migrate(app, db)
