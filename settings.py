from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

# app settings
app = Flask(__name__)
app.config["DEBUG"] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://madhuuser:madhupassword@madhudb.cfsqyk4ui4co.ap-south-1.rds.amazonaws.com/madhudb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///madhu2.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()
