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


db.create_all()
