import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
print os.environ['DATABASE_URL']


# for sqlite ,DATABASE_URL = 'sqlite:////tmp/test.db'
# for local postgres , = postgres:///jithin
# Remote  postgres://nu***:6a2**@ec2-23-23-227-188.compute-1.amazonaws.com:5432/d2s**
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


db = SQLAlchemy(app)


from app import views
'''
from flask.ext.mysql import MySQL

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = 'yet another secret key'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root123'
app.config['MYSQL_DATABASE_DB'] = 'VirtualUsers'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

'''
