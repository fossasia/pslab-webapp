#from cStringIO import StringIO
from io import BytesIO
import sys

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
		
	
	def printer(self,txt):
		self.html+='''<div id="print-statement" class="row well well-sm">%s</div>'''%txt

	def runCode(self,code):
		old_stdout = sys.stdout
		sys.stdout = results = BytesIO()
		
		submitted = compile(str(code), '<string>', mode='exec')
		self.exec_scope = self.evalGlobals.copy()
		try:
			exec(submitted, self.exec_scope)
		except Exception as e:
			print(str(e))
			return str(e)
			
		sys.stdout = old_stdout

		self.html += '''
		<hr><div id="resText" style="width:100%;">{value}</div>
		'''.format(value =results.getvalue().replace(' ','&nbsp;').replace('\n','<br>'))

		#print eval(code,globals(),self.evalGlobals)
		return self.get_html()


	def get_html(self):
		return self.html
		
