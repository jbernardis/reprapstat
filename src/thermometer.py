'''
Created on Apr 15, 2013

@author: Jeff
'''
import wx

tempThreshold = 0.75

class Thermometer(wx.Window): 
	def __init__(self, parent, name=""):
		self.parent = parent
		self.currentSelection = 0
		self.name = name
		self.current = None
		self.target = None
		self.label = None
		
		wx.Window.__init__(self, parent, wx.ID_ANY, size=(-1, -1), style=wx.SIMPLE_BORDER)
		
		self.dc = wx.WindowDC(self)
		self.font = wx.Font (24, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		self.dc.SetFont(self.font)
		szDig = self.dc.GetTextExtent("000.00")
		
		slash = " / "
		szSlash = self.dc.GetTextExtent(slash)
		
		totalWidth = szDig[0] + szDig[0] + szSlash[0]
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		rSizer = wx.BoxSizer()
		
		f = wx.Font (24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		self.dc.SetFont(f)
		s2 = self.dc.GetTextExtent(name)
		totalHeight = szDig[1] + s2[1]
		
		self.SetSize((totalWidth, totalHeight))
		
		print s2, szSlash, szDig

		t = wx.StaticText(self, wx.ID_ANY, name)		
		t.SetFont(f)
		margin = int((totalWidth - s2[0])/2.0)
		rSizer.Add(t, 1, wx.LEFT, margin)
		
		sizer.Add(rSizer)

		rSizer = wx.BoxSizer()
		
		self.temp = wx.StaticText(self, wx.ID_ANY, size=szDig)
		self.temp.SetFont(self.font)
		self.temp.SetBackgroundColour(wx.BLACK)
		self.temp.SetForegroundColour(wx.WHITE)

		self.tgt = wx.StaticText(self, wx.ID_ANY, size=szDig)
		self.tgt.SetFont(self.font)
		self.tgt.SetBackgroundColour(wx.BLACK)
		self.tgt.SetForegroundColour(wx.WHITE)

		t = wx.StaticText(self, wx.ID_ANY, slash, size=szSlash)
		t.SetFont(self.font)
		t.SetBackgroundColour(wx.BLACK)
		t.SetForegroundColour(wx.WHITE)
		
		self.setTarget(self.target)
		
		rSizer.Add(self.temp)
		rSizer.Add(t)
		rSizer.Add(self.tgt)
		
		sizer.Add(rSizer)
		
		self.SetSizer(sizer)
#		sizer.Layout()
		
	def setTarget(self, newTarget):
		self.target = newTarget
		if newTarget is None:
			self.tgt.SetLabel("      ")
		else:
			s = "%6.2f" % newTarget
			self.tgt.SetLabel(s)
			self.setTemp(self.current)
	
	def setTemp(self, newTemp):
		self.current = newTemp
		if newTemp is None:
			self.temp.SetLabel("      ")
		else:
			if self.target is None:
				c = wx.WHITE
			elif self.target < 0.1:
				c = wx.WHITE
			elif newTemp < (self.target-tempThreshold):
				c = wx.BLUE
			elif newTemp > (self.target+tempThreshold):
				c = wx.RED
			else:
				c = wx.GREEN
			self.temp.SetForegroundColour(c)
			s = "%6.2f" % newTemp
			self.temp.SetLabel(s)
		
