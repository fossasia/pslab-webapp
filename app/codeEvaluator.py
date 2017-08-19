from __future__ import print_function

import sys,inspect

import numpy as np
from flask import json
from collections import OrderedDict



class Evaluator:
	def __init__(self,functionList):		
		self.generatedApp=[]
		self.hasPlot=False
		self.itemList=[]
		
		self.evalGlobals={}
		self.functionList = functionList
		self.evalGlobals = functionList.copy()
		self.evalGlobals['print_']=self.printer
		self.evalGlobals['print']=self.print
		self.evalGlobals['button']=self.button
		self.evalGlobals['label']=self.label
		self.evalGlobals['plot']=self.plot
		
	def toUnique(self,identifier): #Make any ID string unique. returns new string.
		suffix=0
		if identifier in self.itemList:
			suffix+=1
			return self.toUnique(identifier+str(suffix))
		self.itemList.append(identifier)
		return identifier
		
	def print(self,*args):
		'''
		For now, the print function is being overloaded in order to capture the console output.
		Future plans will store each line of execution as a json object. This approach will increase flexibility,
		and outputs more than just text, such as images and widgets can be created.
		'''
		name=self.toUnique("print")
		self.generatedApp.append({"type":"text","name":name,"value":[str(a) for a in args]})
		return name
	

	def printer(self,txt,name="print"):
		name=self.toUnique(name)
		self.generatedApp.append({"type":"span","name":name,"class":"row well","value":str(txt)})
		return name

	def label(self,txt,name="print",html_class=""):
		name=self.toUnique(name)
		self.generatedApp.append({"type":"label","name":name,"class":html_class,"value":str(txt)})
		return name

	def button(self,label,endpoint,displayType="display_number",**kwargs):
		name = kwargs.get("name","button-id")
		name=self.toUnique(name)
		
		targetName = kwargs.get("name","button-id-label") #Create a unique name for the target.
		targetName = self.toUnique(targetName)
		targetName = kwargs.get('target',targetName)   #OVerride this name if specified explicitly
		self.generatedApp.append({"type":"button", "name":name,"label":label,"fetched_value":"","action":{"type":"POST","endpoint":endpoint,"success":{"datapoint":'result',"type":displayType,"target":targetName}}})
		if 'target' not in kwargs:  #If a target was not specified, make a label.
			if displayType=="display_number":
				self.label('',targetName)
		return name
	
	#Plots
	def plot(self,x,y,**kwargs):
		name = kwargs.get('name','myPlot')
		self.generatedApp.append({"type":"plot","name":name,"data":[np.array([x,y]).T.tolist()]}) #jqplot requires [x,y] pairs . not separate datasets.
		return name

	def runCode(self,code):
		self.generatedApp=[]
		
		submitted = compile(code.encode(), '<string>', mode='exec')
		self.exec_scope = self.evalGlobals.copy()
		try:
			exec(submitted, self.exec_scope)
		except Exception as e:
			print(str(e))
			
		return self.getApp()


	def getApp(self):
		return self.generatedApp

	#### Extract Doc Strings ####
	def getDocs(self):
		flist = []
		for a in self.functionList.keys():
			if a[:2]=='__':continue
			doc = ''
			try:
				doc = inspect.getdoc(self.functionList[a])
				arglist = inspect.getargspec(self.functionList[a]).args
			except Exception as e:
				print(a,e)
				continue
			arglist.remove('self')
			flist.append({'doc_string':str(doc),'name':a,'args':arglist})
		return flist



		
