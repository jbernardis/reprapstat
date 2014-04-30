'''
Created on Sep 5, 2013

@author: ejefber
'''

import wx
import urllib, urllib2
import  cStringIO
import xml.parsers.expat
import os

if os.path.sep == '/':
	quote = urllib.quote
	unquote = urllib.unquote_plus
else:
	quote = lambda x: urllib.quote(x.replace(os.path.sep, '/'))
	unquote = lambda x: os.path.normpath(urllib.unquote_plus(x))

class Snapshot(wx.Frame):
	def __init__(self, parent, settings):
		self.failed = False
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Snapshot", (-1, -1), (-1, -1), wx.DEFAULT_FRAME_STYLE)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		url = 'http://%s:%s/picture' % (settings.ipAddress, settings.port)

		try:
			f = urllib.urlopen(url)
			picXml = f.read()
			f.close()
		except:
			self.failed  = True
			return
		
		p = xml.parsers.expat.ParserCreate()

		p.StartElementHandler = self._startElement
		p.EndElementHandler = self._endElement
		p.CharacterDataHandler = self._charData
		
		self.inUrl = False
		self.urlPic = ""

		p.Parse(picXml)
		if self.urlPic == "":
			self.failed = True
			return
		
		self.SetTitle("snapshot - %s" % self.urlPic)
	
		fullurl = "http://%s/images/%s" % (quote(settings.ipAddress), self.urlPic)
		try:
			pic = urllib2.urlopen(fullurl)
			data = pic.read()
			pic.close()
			stream = cStringIO.StringIO(data)
	
			jpg = wx.BitmapFromImage( wx.ImageFromStream( stream ))
	
			wx.StaticBitmap(self, wx.ID_ANY, jpg, (-1, -1), (jpg.GetWidth(), jpg.GetHeight()))
		
			self.Fit()
			
		except:
			self.failed = True
			
		
	def wasSuccessful(self):
		return (not self.failed)

	def _startElement(self, name, attrs):
		if name == 'file':
			self.urlPic = ""
			self.inUrl = True
	
	def _endElement(self, name):
		if name == 'file':
			self.inUrl = False
	
	def _charData(self, data):
		if self.inUrl:
			self.urlPic += data
			
	def onClose(self, evt):
		self.Destroy()
		
