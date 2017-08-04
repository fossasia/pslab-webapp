from datetime import datetime
from app import db

class User(db.Model):
	__tablename__ = 'userList'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique=True)
	username = db.Column(db.String(50))
	pwHash = db.Column(db.String(120))

	def __init__(self, email, username,pwHash):
		self.email = email
		self.username = username
		self.pwHash = pwHash

	def __repr__(self):
		return '<User %r>' % self.username


class UserCode(db.Model):
	__tablename__ = 'userCode'
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(80))
	title = db.Column(db.String(100), unique=True)
	code = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)

	def __init__(self, user, title,code,pub_date=None):
		self.user = user
		self.title = title
		self.code = code
		if pub_date is None:
		    pub_date = datetime.utcnow()
		self.pub_date = pub_date

	def __repr__(self):
		return '<UserCode %r>' % self.email



db.create_all()
