from flask import Flask, render_template
app = Flask(__name__)
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
