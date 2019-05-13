import os,sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flasgger import Swagger

print('Version: ',sys.version)


app = Flask(__name__)

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": 'PSLab-Remote',
    "specs": [
        {
            "version": "0.0.1",
            "title": "PSLab Remote Access",
            "description": "PSLab remote access framework",
            "endpoint": "v1_spec",
            "route": "/v1/spec",
        }
    ]
}

Swagger(app)

CORS(app,supports_credentials=True)

app.secret_key = 'yet another secret key'

app.config.from_object('config')


# for sqlite ,DATABASE_URL = 'sqlite:////tmp/test.db'
# for local postgres , = postgres:///jithin
# Remote  postgres://nu***:6a2**@ec2-23-23-227-188.compute-1.amazonaws.com:5432/d2s**
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


db = SQLAlchemy(app)

db.create_all()

# from app import views

