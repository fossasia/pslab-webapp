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
		
	def toUnique(self,identifier,suffix=0): #Make any ID string unique. returns new string.
		newId = identifier+str(suffix) if suffix else identifier
		if newId in self.itemList:
			return self.toUnique(identifier,suffix+1)
		return newId
		
	def print(self,*args):
		'''
		For now, the print function is being overloaded in order to capture the console output.
		Future plans will store each line of execution as a json object. This approach will increase flexibility,
		and outputs more than just text, such as images and widgets can be created.
		'''
		name=self.toUnique("print")
		self.generatedApp.append({"type":"text","name":name,"value":[str(a) for a in args]})
		self.itemList.append(name)
		return name
	

	def printer(self,txt,name="print"):
		name=self.toUnique(name)
		self.generatedApp.append({"type":"span","name":name,"class":"row well","value":str(txt)})
		self.itemList.append(name)
		return name

	def label(self,txt,name="print",html_class=""):
		name=self.toUnique(name)
		self.generatedApp.append({"type":"label","name":name,"class":html_class,"value":str(txt)})
		self.itemList.append(name)
		return name

	def button(self,label,endpoint,displayType="display_number",**kwargs):
		name = kwargs.get("name","button-id")
		name=self.toUnique(name)
		self.itemList.append(name)
		
		targetName = kwargs.get('target',name+'-label')
		if 'target' not in kwargs:  #If a target was not specified, make up a name
			targetName = self.toUnique(name+'-label')

		successOpts={"datapoint":'result',"type":displayType,"target":targetName}
		if displayType=='update-plot': # specify the stacking of data
			successOpts['stacking']='xy'
		self.generatedApp.append({"type":"button", "name":name,"label":label,"fetched_value":"","action":{"type":"POST","endpoint":endpoint,"success":successOpts}})
		if 'target' not in kwargs:  #If a target was not specified, make a label.
			if displayType in ["display_number","display"]:
				print('making a target')
				self.label('',targetName)
		return name
	
	#Plots
	def plot(self,x,y,**kwargs):
		name = kwargs.get('name','myPlot')
		self.generatedApp.append({"type":"plot","name":name,"data":[np.array([x,y]).T.tolist()]}) #jqplot requires [x,y] pairs . not separate datasets.
		self.itemList.append(name)
		return name

	def runCode(self,code):
		self.generatedApp=[]
		self.itemList=[]
		
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



		
