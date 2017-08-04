import inspect,random
import numpy as np

# A dummy class that will pretend to be a minimal PSLab . we shall use this for testing purposes during development as well as deployment.
class dummy(object):
	def __init__(self):
		self.x=np.linspace(0,8*np.pi,200)
		self.r = random.random()
	def capture1(self,chan,samples,tg):
		'''
		Example doc for capture command. returns a sine wave (x,y)
		'''
		self.x=np.linspace(0,8*np.pi,samples)
		return self.x,np.sin(self.x+np.pi*random.random()/10)
	def capture2(self,samples,tg):
		self.x=np.linspace(0,8*np.pi,samples)
		return self.x,np.sin(self.x+np.pi*random.random()/10),np.sin(self.x+np.pi*random.random()/10)

	def get_voltage(self,chan):
		'''
		get a random value
		'''
		return self.r+random.random()
	def set_pv1(self,val):
		return val+self.r


# Try to import and create an instance of sciencelab, otherwise create an instance of the dummy class
try:
	from PSL import sciencelab
	I = sciencelab.connect(verbose=True)
	I.set_sine2(1000)
except Exception as e:
	print ('using dummy class',str(e))
	I = dummy()

# Use the inspect module to prepare a list of methods available in the class. 
#This is quite flexible, and in theory this framework should easily adapt to serve any hardware with a python communication library
functionList = {}
for a in dir(I):
	attr = getattr(I, a)
	if inspect.ismethod(attr) and a!='__init__':
		functionList[a] = attr

