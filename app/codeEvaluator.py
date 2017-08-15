from __future__ import print_function

import sys,inspect

import numpy as np
from flask import json
from collections import OrderedDict



class Evaluator:
	def __init__(self,functionList):		
		self.generatedApp=[]
		self.hasPlot=False

		self.evalGlobals={}
		self.functionList = functionList
		self.evalGlobals = functionList.copy()
		self.evalGlobals['print_']=self.printer
		self.evalGlobals['print']=self.print
		
	def print(self,*args):
		'''
		For now, the print function is being overloaded in order to capture the console output.
		Future plans will store each line of execution as a json object. This approach will increase flexibility,
		and outputs more than just text, such as images and widgets can be created.
		'''
		self.generatedApp.append({"name":"print","type":"text","value":str(args)})
	
	def printer(self,txt):
		self.generatedApp.append({"name":"print","type":"span","class":"row well","value":str(txt)})

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



		
