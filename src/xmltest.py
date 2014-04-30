'''
Created on Jun 12, 2013

@author: ejefber
'''
import xml.parsers.expat

class Node:
	def __init__(self, name):
		self.name = name
		self.value = None
		self.properties = {}
		
	def getName(self):
		return self.name
	
	def getPropertyCount(self):
		return len(self.properties)
	
	def getProperty(self, name):
		if name not in self.properties.keys():
			return None
		else:
			return self.properties[name]
		
	def getProperties(self):
		return self.properties
		
	def setProperty(self, name, value):
		if name in self.properties.keys():
			ov = self.properties[name]
			try:
				self.properties[name].append(value)
			except:
				self.properties[name] = [ ov, value ]
		else:
			self.properties[name] = value
			
	def getValue(self):
		return self.value

	def setValue(self, value):
		
		self.value = value.strip()
		if self.value == '':
			self.value = None

# 3 handler functions
class MyClass:
	def __init__(self):
		self.root = None
		self.stack = []
		
	def start_element(self, name, attrs):
		newNode = Node(name)
		if self.root == None:
			self.root = newNode
		else:
			parent = self.stack[-1]
			parent.setProperty(name, newNode)
			
		self.stack.append(newNode)
		
	def end_element(self, name):
		if len(self.stack) == 0:
			print "Empty Stack"
			return None
		
		del self.stack[-1]
		
	def char_data(self, data):
		if len(self.stack) == 0:
			print "Empty Stack"
			return None
		
		p = self.stack[-1]
		p.setValue(data)
		
	def getRoot(self):
		return self.root

	def start(self, text):
		p = xml.parsers.expat.ParserCreate()

		p.StartElementHandler = self.start_element
		p.EndElementHandler = self.end_element
		p.CharacterDataHandler = self.char_data

		p.Parse(text,  1)
		
def traverse(nd, nest):
	print " " * nest, nd.getName()
	if nd.getValue() is not None:
		print " " * nest, "  Value: ", nd.getValue()
		
	plist = nd.getProperties()
	for k in plist.keys():
		try:
			for pl in plist[k]:
				traverse(pl, nest+1)
		except:
			traverse(plist[k], nest+1)	
		
		
		
if __name__ == '__main__':
	p = MyClass()
	
	text = open('maven.txt').read()		

	p.start(text)
	
	r = p.getRoot()
	
	traverse(r, 0)