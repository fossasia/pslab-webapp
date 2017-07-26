from app import app,SQLAlchemy,db
from app.db_handler import User
from flask import Flask, render_template,request,json,session,redirect,jsonify
from werkzeug import generate_password_hash, check_password_hash
import os


@app.route('/')
@app.route('/index')
@app.route('/main')
def index():
	'''
	Home Page link
	'''
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	'''
	Sign-up Page link
	'''
	return render_template('signup.html')



@app.route('/signUp',methods=['POST'])
def signUp():
	# read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	# validate the received values
	if _name and _email and _password:
		_hashed_password = generate_password_hash(_password)
		newUser = User(_email, _name,_hashed_password)
		try:
			db.session.add(newUser)
			db.session.commit()
			return json.dumps({'message':'User %s created successfully. e-mail:%s !'%(_name,_email)})
		except Exception as exc:
			reason = str(exc)
			print ("Message: " , reason)
			return json.dumps({'error':str(reason)})



@app.route('/showSignIn')
@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
	_username = request.form['inputEmail']
	_password = request.form['inputPassword']
	user = User.query.filter_by(email=_username).first() #retrieve the row based on e-mail
	if user is not None:
		if check_password_hash(user.pwHash,_password):
			session['user'] = [user.username,user.email]
			return redirect('/userHome')
		else:
			return render_template('error.html',error = 'Wrong Email address or Password. hash mismatch')
	else:
		return render_template('error.html',error = 'Wrong Email address or Password. no len')



@app.route('/userHome')
def userHome():
	if session.get('user'):
		#print (session['user'])
		return render_template('userHome.html',username = session['user'][0])
	else:
		return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/showAddScript')
def showAddScript():
	if session.get('user'):
		#print (session['user'])
		return render_template('addScript.html',author = session['user'][0])
	else:
		return render_template('error.html',error = 'Unauthorized Access')    



"""
#Pending migration to postgres



import inspect,random
import numpy as np
# A dummy class that will pretend to be a minimal PSLab . we shall use this for testing purposes.
class dummy(object):
	def __init__(self):
		self.x=np.linspace(0,8*np.pi,200)
		self.r = random.random()
	def capture1(self,chan,samples,tg):
		'''
		Example doc for capture command. returns a sine wave
		'''
		self.x=np.linspace(0,8*np.pi,samples)
		return self.x,np.sin(self.x+np.pi*random.random()/10)
	def capture2(self,samples,tg):
		self.x=np.linspace(0,8*np.pi,samples)
		return self.x,np.sin(self.x+np.pi*random.random()/10),np.sin(self.x+np.pi*random.random()/10)

	def get_voltage(self,chan):
		'''
		bloo blahs
		a454
		*&^ "23"
		'''
		return self.r+random.random()
	def set_pv1(self,val):
		return val+self.r


try:
	from PSL import sciencelab
	I = sciencelab.connect(verbose=True)
	I.set_sine2(1000)
except Exception as e:
	print ('using dummy class',str(e))
	I = dummy()

# Use the inspect module to prepare a list of methods available in the class. This is quite flexible, and in theory this framework should easily adapt to serve any hardware with a python communication library
functionList = {}
for a in dir(I):
	attr = getattr(I, a)
	if inspect.ismethod(attr) and a!='__init__':
		functionList[a] = attr



"""
