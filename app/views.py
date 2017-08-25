from app import app,SQLAlchemy,db
from app.db_handler import User,UserCode
from flask import Flask, render_template,request,json,session,redirect,jsonify,send_from_directory
from werkzeug import generate_password_hash, check_password_hash
import os

####  Get the list of available hardware methods ###
from app.hardwareHandler import functionList,np
from app.codeEvaluator import Evaluator

myEval = Evaluator(functionList)


@app.route('/signUp',methods=['POST'])
def signUp():
	"""Sign Up for Virtual Lab

	POST: Submit sign-up parameters. The following must be present:
	 inputName : The name of your account. does not need to be unique
	 inputEmail : e-mail ID used for login . must be unique.
	Returns HTTP 404 when data does not exist.
	"""
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
			return json.dumps({'status':True,'message':'User %s created successfully. e-mail:%s !'%(_name,_email)})
		except Exception as exc:
			reason = str(exc)
			return json.dumps({'status':False,'message':str(reason)})



@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    _username = request.form['inputEmail']
    _password = request.form['inputPassword']
    user = User.query.filter_by(email=_username).first() #retrieve the row based on e-mail
    if user is not None:
        if check_password_hash(user.pwHash,_password):
            session['user'] = [user.username,user.email]
            return json.dumps({'status':True})
        else:
            return json.dumps({'status':False,'message':'Wrong Email address or Password. hash mismatch'})
    else:
        return json.dumps({'status':False,'message':'Username not specified'})

@app.route('/logout',methods=['POST'])
def logout():
	try:
		print ('logging out',session.pop('user',None))
		return json.dumps({'status':True,'message':'Logged out'})
	except Exception as exc:
		reason = str(exc)
		return json.dumps({'status':False,'message':str(reason)})


@app.route('/getUserName')
def getUserName():
	if session.get('user'):
		return json.dumps({'username':session['user'][0]})
	else:
		return json.dumps({'error':'Not Logged In'})



@app.route('/addScript',methods=['POST'])
def addScript():
	try:
		if session.get('user'):
			_user = session.get('user')[1]
			_title = request.form['inputTitle']
			_description = request.form['inputDescription']

			newSnippet = UserCode(_user, _title,_description)
			try:
				db.session.add(newSnippet)
				db.session.commit()
				return json.dumps({'status':True})
			except Exception as exc:
				return json.dumps({'status':False,'message':str(exc)})

		else:
			return json.dumps({'status':False,'message':'Unauthorized access'})
	except Exception as e:
		return json.dumps({'status':False,'message':str(e)})


@app.route('/getScriptList')
def getScriptList():
	try:
		if session.get('user'):
			_user = session.get('user')[1]
			scripts = UserCode.query.filter_by(user=_user)
			scripts_dict = []
			for script in scripts:
				single_script = {
						'Id': script.id,
						'Filename': script.title,
						#'Code': script.code, #Can be enbled if the user demands all scripts and content.
						'Date': script.pub_date}
				scripts_dict.append(single_script)
			return json.dumps(scripts_dict)
		else:
			return json.dumps([])
	except Exception as e:
		print (str(e))
		return json.dumps([])


@app.route('/getScriptById',methods=['POST'])
def getCodeById():
	if session.get('user'):
		_id = request.form['id']
		_user = session.get('user')[1]
		try:
			script = UserCode.query.filter_by(user=_user,id=_id).first()
			return json.dumps({'status':True,'Id':script.id,'Code':script.code,'Filename':script.title,'Date':script.pub_date,'message':'got script %s'%script.title})
		except Exception as exc:
			return json.dumps({'data':None,'status':False,'message':str(exc)})
	else:
		return json.dumps({'data':None,'status':False,'message':'Unauthorized access'})




@app.route('/updateCode', methods=['POST'])
def updateCode():
  if session.get('user'):
    _user = session.get('user')[1]
    _title = request.form['inputTitle']
    _description = request.form['inputDescription']
    _code_id = request.form['codeId']
    try:
      script = UserCode.query.filter_by(user=_user,id=_code_id).first()
      script.title = _title
      script.code = _description
      db.session.commit()
      return json.dumps({'status':True,'message':'Updated!'})
    except Exception as exc:
      return json.dumps({'status':False,'message':str(exc)})
  else:
    return json.dumps({'status':False,'message':'Unauthorized access'})




@app.route('/deleteScript',methods=['POST'])
def deleteScript():
  if session.get('user'):
    _user = session.get('user')[1]
    _id = request.form['scriptId']
    try:
      UserCode.query.filter_by(user=_user,id=_id).delete()
      print ('deleted',_id)
      db.session.commit()
      return json.dumps({'status':True,'message':'Deleted!'})
    except Exception as exc:
      print(exc)
      return json.dumps({'status':False,'message':str(exc)})
  else:
    return json.dumps({'status':False,'message':'Unauthorized access'})


@app.route('/getCommonScripts')
def getCommonScripts():
	try:
		if session.get('user'):
			_user = session.get('user')[1]
			scripts = [{'Filename':a} for a in os.listdir('./app/scripts') if a[-3:]=='.py']
			return json.dumps(scripts)
		else:
			return json.dumps([])
	except Exception as e:
		print (str(e))
		return json.dumps([])


@app.route('/getScriptByFilename',methods=['POST'])
def getScriptByFilename():
	if session.get('user'):
		try:
			Filename = request.form['Filename']
			with open ('./app/scripts/'+Filename, "r") as myfile:
				data=myfile.read()
			return json.dumps({'status':True,'Filename':Filename,'Code':data})
		except Exception as exc:
			return json.dumps({'status':False,'message':str(exc),'Code':None})
	else:
		return json.dumps({'status':False,'message':'Unauthorized access','Code':None})


@app.route('/runScriptByFilename',methods=['POST'])
def runScriptByFilename():
	if session.get('user'):
		try:
			Filename = request.form['Filename']
			with open ('./app/scripts/'+Filename, "r") as myfile:
				data=myfile.read()
			res = myEval.runCode(script.code)
			return json.dumps({'status':True,'Filename':Filename,'result':res})
		except Exception as exc:
			return json.dumps({'result':None,'status':False,'message':str(exc)})
	else:
		return json.dumps({'result':None,'status':False,'message':'Unauthorized access'})





@app.route('/getFunctionList')
def getFunctionList():
	"""returns a comprehensive list of functions, their arguments and their docstrings
	{'status':true/false, 'doc_list':doc_list}
	doc_list = [{args:list of arguments, name:name of the function , doc_string : inline docstring if any},{function 2},...]
	"""
	if session.get('user'):
		return json.dumps({'status':False,'doc_list':myEval.getDocs()})
	else:
		return json.dumps({'status':False,'doc_list':[]})



@app.route('/evalFunctionString',methods=['POST'])
def evalFunctionString():
    if session.get('user'):
        _stringify=False
        try:
            _user = session.get('user')[1]
            _fn = request.form['function']
            _stringify = request.form.get('stringify',False)
            res = eval(_fn,functionList)
        except Exception as e:
            res = str(e)
        #dump string if requested. Otherwise json array
        if _stringify:
            return json.dumps({'status':True,'result':str(res),'stringified':True})
        else:
            #Try to simply convert the results to json
            try:
                return json.dumps({'status':True,'result':res,'stringified':False})
            # If that didn't work, it's due to the result containing numpy arrays.
            except Exception as e:
                #try to convert the numpy arrays to json using the .toList() function
                try:
                    return json.dumps({'status':True,'result':np.array(res).tolist(),'stringified':False})
                #And if nothing works, return the string
                except Exception as e:
                    print( 'string return',str(e))
                    return json.dumps({'status':True,'result':str(res),'stringified':True})
    else:
        return json.dumps({'status':False,'result':'unauthorized access','message':'Unauthorized access'})



@app.route('/runScriptById',methods=['POST'])
def runScriptById():
	if session.get('user'):
		_id = request.form['id']
		_user = session.get('user')[1]
		try:
			script = UserCode.query.filter_by(user=_user,id=_id).first()
			res = myEval.runCode(script.code)
			return json.dumps({'status':True,'Id':script.id,'result':res,'Filename':script.title,'Date':script.pub_date})
		except Exception as exc:
			return json.dumps({'status':False,'result':str(exc)})
	else:
		return json.dumps({'status':False,'result':'unauthorized access','message':'Unauthorized access'})


