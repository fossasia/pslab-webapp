import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app,supports_credentials=True)

app.secret_key = 'yet another secret key'

#app.config.from_object(os.environ['APP_SETTINGS'])
#print (os.environ['DATABASE_URL'])


# for sqlite ,DATABASE_URL = 'sqlite:////tmp/test.db'
# for local postgres , = postgres:///jithin
# Remote  postgres://nu***:6a2**@ec2-23-23-227-188.compute-1.amazonaws.com:5432/d2s**
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


db = SQLAlchemy(app)

from app import views

