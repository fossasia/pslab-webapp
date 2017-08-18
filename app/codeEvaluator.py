from __future__ import print_function

import sys,inspect

import numpy as np
from flask import json
from collections import OrderedDict



class Evaluator:
	def __init__(self,functionList):		
		self.generatedApp=[]
		self.widgets = 0
		self.hasPlot=False

		self.evalGlobals={}
		self.functionList = functionList
		self.evalGlobals = functionList.copy()
		self.evalGlobals['print_']=self.printer
		self.evalGlobals['print']=self.print
		self.evalGlobals['button']=self.button
		self.evalGlobals['label']=self.label
		self.evalGlobals['plot']=self.plot
		
	def print(self,*args):
		'''
		For now, the print function is being overloaded in order to capture the console output.
		Future plans will store each line of execution as a json object. This approach will increase flexibility,
		and outputs more than just text, such as images and widgets can be created.
		'''
		self.generatedApp.append({"type":"text","name":"print","value":str(args)})
	

	def printer(self,txt,name="print"):
		self.generatedApp.append({"type":"span","name":name,"class":"row well","value":str(txt)})

	def label(self,txt,name="print",html_class=""):
		self.generatedApp.append({"type":"label","name":name,"class":html_class,"value":str(txt)})

	def button(self,label,endpoint,displayType="display_number"):
		self.generatedApp.append({"type":"button", "name":"button-id%d"%self.widgets,"label":label,"fetched_value":"","action":{"type":"POST","endpoint":endpoint,"success":{"datapoint":'result',"type":displayType,"target":"button-id%d-label"%self.widgets}}})
		if displayType=="display_number":
			self.label('',"button-id%d-label"%self.widgets)
		self.widgets+=1
	
	#Plots
	def plot(self,x,y,**kwargs):
		self.generatedApp.append({"type":"plot","name":kwargs.get('name','myPlot'),"data":[np.array([x,y]).T.tolist()]}) #jqplot requires [x,y] pairs . not separate datasets.

	def runCode(self,code):
		self.generatedApp=[]
		self.widgets = 0
		
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



		
