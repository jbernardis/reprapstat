'''
Created on Sep 5, 2013

@author: ejefber
'''

import wx
from thermometer import Thermometer

LABEL_FILE = "File:"
LABEL_START_TIME = "Start Time:"
LABEL_EXPECTED_DURATION = "Expected Duration:"
LABEL_ORIGINAL_ETA = "Original ETA:"
LABEL_ELAPSED = "Elapsed Time:"
LABEL_REMAINING = "Remaining Time:"
LABEL_REVISED_ETA = "Revised ETA:"
LABEL_CURRENT_HEIGHT = "Current Height:"
LABEL_LAYER = "Layer:"
LABEL_G_CODE = "G Code:"

class Connection(wx.Frame):
	def __init__(self, parent, cx, htrs):
		self.cx = cx
		self.htrs = htrs
		title = "Connection %d" % (cx+1)
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, (-1, -1), (-1, -1), wx.DEFAULT_FRAME_STYLE & ~(wx.CLOSE_BOX))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		sizer = wx.BoxSizer(wx.VERTICAL)

		sizerLeft = wx.BoxSizer(wx.VERTICAL)
		sizerRight = wx.BoxSizer(wx.VERTICAL)
		
		grid = wx.GridBagSizer()
		bfont = wx.Font (12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		font = wx.Font (12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
	
		
		row = 1
		t = wx.StaticText(self, wx.ID_ANY, "Printer:", size=(160,-1))
		t.SetFont(bfont)
		grid.Add(t, (row,0))
		
		self.tPrtr = wx.StaticText(self, wx.ID_ANY, "", size=(200, -1));
		self.tPrtr.SetFont(font)
		grid.Add(self.tPrtr, (row,1))
		
		t = wx.StaticText(self, wx.ID_ANY, "Port:")
		t.SetFont(bfont)
		grid.Add(t, (row+1,0))
		
		self.tPort = wx.StaticText(self, wx.ID_ANY, "");
		self.tPort.SetFont(font)
		grid.Add(self.tPort, (row+1,1))
		
		t = wx.StaticText(self, wx.ID_ANY, "Status:")
		t.SetFont(bfont)
		grid.Add(t, (row+2,0))
		
		self.tStat = wx.StaticText(self, wx.ID_ANY, "");
		self.tStat.SetFont(font)
		grid.Add(self.tStat, (row+2,1))
		
		sizerLeft.Add(grid)
		sizerLeft.AddSpacer((20, 20))
		
		self.lFile = wx.StaticText(self, wx.ID_ANY, "")
		self.lFile.SetFont(bfont)
		sizerLeft.Add(self.lFile)
		
		self.tFile = wx.StaticText(self, wx.ID_ANY, "");
		self.tFile.SetFont(font)
		sizerLeft.Add(self.tFile)

		sizerLeft.AddSpacer((20, 20))
		
		grid = wx.GridBagSizer()
		row = 0
		
		self.lStartTime = wx.StaticText(self, wx.ID_ANY, "", size=(160,-1))
		self.lStartTime.SetFont(bfont)
		grid.Add(self.lStartTime, (row,0))
		
		self.tStartTime = wx.StaticText(self, wx.ID_ANY, "", size=(200, -1));
		self.tStartTime.SetFont(font)
		grid.Add(self.tStartTime, (row,1))
		
		self.lExpDur = wx.StaticText(self, wx.ID_ANY, "")
		self.lExpDur.SetFont(bfont)
		grid.Add(self.lExpDur, (row+1,0))
		
		self.tExpDur = wx.StaticText(self, wx.ID_ANY, "");
		self.tExpDur.SetFont(font)
		grid.Add(self.tExpDur, (row+1,1))
		
		self.lOrigETA = wx.StaticText(self, wx.ID_ANY, "")
		self.lOrigETA.SetFont(bfont)
		grid.Add(self.lOrigETA, (row+2,0))
		
		self.tOrigETA = wx.StaticText(self, wx.ID_ANY, "");
		self.tOrigETA.SetFont(font)
		grid.Add(self.tOrigETA, (row+2,1))
		
		grid.AddSpacer((10, 10), (row+3, 0))
		row += 4
		
		
		self.lElapsed = wx.StaticText(self, wx.ID_ANY, "")
		self.lElapsed.SetFont(bfont)
		grid.Add(self.lElapsed, (row,0))
		
		self.tElapsed = wx.StaticText(self, wx.ID_ANY, "");
		self.tElapsed.SetFont(font)
		grid.Add(self.tElapsed, (row,1))
		
		self.lRemaining = wx.StaticText(self, wx.ID_ANY, "")
		self.lRemaining.SetFont(bfont)
		grid.Add(self.lRemaining, (row+1,0))
		
		self.tRemaining = wx.StaticText(self, wx.ID_ANY, "");
		self.tRemaining.SetFont(font)
		grid.Add(self.tRemaining, (row+1,1))
		
		self.lNewETA = wx.StaticText(self, wx.ID_ANY, "")
		self.lNewETA.SetFont(bfont)
		grid.Add(self.lNewETA, (row+2,0))
		
		self.tNewETA = wx.StaticText(self, wx.ID_ANY, "");
		self.tNewETA.SetFont(font)
		grid.Add(self.tNewETA, (row+2,1))
		
		grid.AddSpacer((20, 20), (row+3, 0))
		row += 4
		
		self.lHeight = wx.StaticText(self, wx.ID_ANY, "")
		self.lHeight.SetFont(bfont)
		grid.Add(self.lHeight, (row,0))
		
		self.tHeight = wx.StaticText(self, wx.ID_ANY, "");
		self.tHeight.SetFont(font)
		grid.Add(self.tHeight, (row,1))
		
		self.lLayer = wx.StaticText(self, wx.ID_ANY, "")
		self.lLayer.SetFont(bfont)
		grid.Add(self.lLayer, (row+1,0))
		
		self.tLayer = wx.StaticText(self, wx.ID_ANY, "");
		self.tLayer.SetFont(font)
		grid.Add(self.tLayer, (row+1,1))
		
		self.lGCode = wx.StaticText(self, wx.ID_ANY, "G Code")
		self.lGCode.SetFont(bfont)
		grid.Add(self.lGCode, (row+2,0))
		
		self.tGCode = wx.StaticText(self, wx.ID_ANY, "");
		self.tGCode.SetFont(font)
		grid.Add(self.tGCode, (row+2,1))
			
		sizerLeft.Add(grid)
		
		sizerH = wx.BoxSizer(wx.HORIZONTAL)
		sizerH.AddSpacer((20, 20))
		sizerH.Add(sizerLeft)

		sizerRight.AddSpacer((20, 20))

		self.therm = {}				
		self.therm['Bed']= Thermometer(self, "Print Bed")
		sizerRight.Add(self.therm['Bed'])
		sizerRight.AddSpacer((10, 10))

		k = "temps::connection.%d::temps::temps::HE0" % (self.cx+1)
		if k in self.htrs:
			self.therm['HE0'] = Thermometer(self, "Hot End 0")
			sizerRight.Add(self.therm['HE0'])
			sizerRight.AddSpacer((10, 10))

		k = "temps::connection.%d::temps::temps::HE1" % (self.cx+1)
		if k in self.htrs:
			self.therm['HE1'] = Thermometer(self, "Hot End 1")
			sizerRight.Add(self.therm['HE1'])
			sizerRight.AddSpacer((10, 10))

		sizerRight.AddSpacer((10, 10))
		
		sizerH.Add(sizerRight, 1, wx.EXPAND)
		sizerH.AddSpacer((20,20))
		
		sizer.Add(sizerH)
		
		self.SetSizer(sizer)
		self.Layout()
		self.Fit()

	def onClose(self, evt):
		self.Destroy()
		
	def Update(self, stat, temp):
		kpfx = ('status::connection.%d' % (self.cx+1)) + '::'
		self.tPrtr.SetLabel(stat[kpfx+'printer'])
		self.tPort.SetLabel(stat[kpfx+'port'])
		status = stat[kpfx+'status']
		self.tStat.SetLabel(status)
		
		if status == "printing":
			kpfx += "printstat::"
			self.lFile.SetLabel(LABEL_FILE)
			self.tFile.SetLabel(stat[kpfx+"filename"])
			self.lStartTime.SetLabel(LABEL_START_TIME)
			self.tStartTime.SetLabel(stat[kpfx+"times::starttime"])
			self.lExpDur.SetLabel(LABEL_EXPECTED_DURATION)
			self.tExpDur.SetLabel(stat[kpfx+"times::expectedduration"])
			self.lOrigETA.SetLabel(LABEL_ORIGINAL_ETA)
			self.tOrigETA.SetLabel(stat[kpfx+"times::origeta"])
			self.lElapsed.SetLabel(LABEL_ELAPSED)
			self.tElapsed.SetLabel(stat[kpfx+"times::elapsed"])
			self.lRemaining.SetLabel(LABEL_REMAINING)
			self.tRemaining.SetLabel(stat[kpfx+"times::remaining"])
			self.lNewETA.SetLabel(LABEL_REVISED_ETA)
			self.tNewETA.SetLabel(stat[kpfx+"times::neweta"])
			self.lHeight.SetLabel(LABEL_CURRENT_HEIGHT)
			self.tHeight.SetLabel(stat[kpfx+"currentheight"])
			self.lLayer.SetLabel(LABEL_LAYER)
			self.tLayer.SetLabel("%s / %s" % (stat[kpfx+"currentlayer"], stat[kpfx+"layers"]))
			self.lGCode.SetLabel(LABEL_G_CODE)
			self.tGCode.SetLabel("%s / %s (%s)" % (stat[kpfx+"gcode::position"], stat[kpfx+"gcode::linecount"], stat[kpfx+"percent"]))
		else:
			self.lFile.SetLabel("")
			self.tFile.SetLabel("")
			self.lStartTime.SetLabel("")
			self.tStartTime.SetLabel("")
			self.lExpDur.SetLabel("")
			self.tExpDur.SetLabel("")
			self.lOrigETA.SetLabel("")
			self.tOrigETA.SetLabel("")
			self.lHeight.SetLabel("")
			self.tHeight.SetLabel("")
			self.lLayer.SetLabel("")
			self.tLayer.SetLabel("")
			self.lGCode.SetLabel("")
			self.tGCode.SetLabel("")
			self.lElapsed.SetLabel("")
			self.tElapsed.SetLabel("")
			self.lRemaining.SetLabel("")
			self.tRemaining.SetLabel("")
			self.lNewETA.SetLabel("")
			self.tNewETA.SetLabel("")
			
		for th in ['Bed', 'HE0', 'HE1']:
			k = "temps::connection.%d::temps::temps::%s" % (self.cx+1, th)
			if k in temp.keys():
				try:
					v = float(temp[k])
				except:
					v = 0.0
					
				self.therm[th].setTemp(v)
				
			k = "temps::connection.%d::temps::targets::%s" % (self.cx+1, th)
			if k in temp.keys():
				try:
					v = float(temp[k])
				except:
					v = 0.0
					
				self.therm[th].setTarget(v)

