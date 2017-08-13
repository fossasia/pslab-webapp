from __future__ import print_function

import sys,inspect

import numpy as np
from flask import json
from collections import OrderedDict



class Evaluator:
	def __init__(self,functionList):		
		self.html = ''
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
		self.html += str(*args).replace(' ','&nbsp;').replace('\n','<br>')
		self.html+='<br>'
	
	def printer(self,txt):
		self.html+='''<div id="print-statement" class="row well well-sm">%s</div>'''%txt

	def runCode(self,code):
		self.html = """ <hr><div id="resText" style="width:100%;"> """
		
		submitted = compile(code.encode(), '<string>', mode='exec')
		self.exec_scope = self.evalGlobals.copy()
		try:
			exec(submitted, self.exec_scope)
		except Exception as e:
			print(str(e))
			
		self.html += "</div>"
		return self.get_html()


	def get_html(self):
		return self.html

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



		
