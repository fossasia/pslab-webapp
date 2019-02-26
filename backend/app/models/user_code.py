from datetime import datetime
from app import db

class UserCode(db.Model):
	__tablename__ = 'userCode'
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(80))
	title = db.Column(db.String(100))
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