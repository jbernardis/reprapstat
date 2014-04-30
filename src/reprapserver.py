
import urllib
import string
import xml.parsers.expat

class RepRapError(Exception):
	pass

class RepRapServer:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		
	def Status(self):
		url = 'http://%s:%s/status' % (self.ip, self.port)

		try:
			f = urllib.urlopen(url)
			statxml = f.read()
			f.close()
	
		except:
			return {}

		self.lStack = []
		self.xkeys = {}
		self.status = {}
	
		p = xml.parsers.expat.ParserCreate()

		p.StartElementHandler = self._startElement
		p.EndElementHandler = self._endElement
		p.CharacterDataHandler = self._charStatusData

		p.Parse(statxml)
		return self.status
	
	def Temps(self):
		url = 'http://%s:%s/temps' % (self.ip, self.port)

		try:
			f = urllib.urlopen(url)
			tempxml = f.read()
			f.close()
	
		except:
			return {}

		self.lStack = []
		self.xkeys = {}
		self.temps = {}
	
		p = xml.parsers.expat.ParserCreate()

		p.StartElementHandler = self._startElement
		p.EndElementHandler = self._endElement
		p.CharacterDataHandler = self._charTempData

		p.Parse(tempxml)
		return self.temps

	def _startElement(self, name, attrs):
		self.lStack.append(name)
	
	def _endElement(self, name):
		if len(self.lStack) == 0:
			raise RepRapError("ERROR: Stack unexpectedly empty")
		
		del self.lStack[-1]
	
	def _charStatusData(self, data):
		if len(self.lStack) == 0:
			raise RepRapError("ERROR: Stack unexpectedly empty")

		label = string.join(self.lStack, '::')
		self.status[label] = data
		
		for kx in range(len(self.lStack)-1):
			self.addXKey(string.join(self.lStack[0:kx+1], "::"), self.lStack[kx+1])
	
	def _charTempData(self, data):
		if len(self.lStack) == 0:
			raise RepRapError("ERROR: Stack unexpectedly empty")

		label = string.join(self.lStack, '::')
		self.temps[label] = data
		
		for kx in range(len(self.lStack)-1):
			self.addXKey(string.join(self.lStack[0:kx+1], "::"), self.lStack[kx+1])
			
	def addXKey(self, value, key):
		if value not in self.xkeys.keys():
			self.xkeys[value] = [key]
		elif key not in self.xkeys[value]:
			self.xkeys[value].append(key)
			

