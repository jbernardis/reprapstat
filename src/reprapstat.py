'''
Created on Sep 5, 2013

@author: ejefber
'''
import os.path
import sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

#import wx
import wx.lib.newevent
import thread

from reprapserver import RepRapServer
from connection import Connection
from snapshot import Snapshot
from settings import Settings

(UpdateEvent, EVT_STATUS_UPDATE) = wx.lib.newevent.NewEvent()


BASE_ID = 500
MAINTIMER = 1000

class UpdateThread:
	def __init__(self, win, rrs):
		self.win = win
		self.rrs = rrs
		self.status = None
		self.temps = None

	def Start(self):
		thread.start_new_thread(self.Run, ())

	def getStatus(self):
		return self.status
	
	def getTemps(self):
		return self.temps

	def Run(self):
		self.status = self.rrs.Status()
		self.temps = self.rrs.Temps()
		evt = UpdateEvent()
		wx.PostEvent(self.win, evt)	
	
class MainFrame(wx.Frame):
	def __init__(self, rrs, settings):
		self.rrs = rrs
		self.settings = settings
		
		self.count = 0
		font = wx.Font (12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.loadImages()
		
		wx.Frame.__init__(self, None, title="RepRap Status")
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(EVT_STATUS_UPDATE, self.continueUpdate)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.conn = []

		ribbon = wx.BoxSizer(wx.HORIZONTAL)	
		
		ribbon.AddSpacer((10, 10))
					
		self.bRefresh = wx.BitmapButton(self, wx.ID_ANY, self.imageRefresh, size=(48, 48))
		self.bRefresh.SetToolTipString("Refresh Data")
		self.Bind(wx.EVT_BUTTON, self.onRefresh, self.bRefresh)
		ribbon.Add(self.bRefresh, 1, wx.ALL, 10)
		
		ribbon.AddSpacer((20, 20))
		
		self.cbAuto = wx.CheckBox(self, wx.ID_ANY, "Auto Refresh every")
		self.cbAuto.SetValue(self.settings.autoRefresh)
		self.cbAuto.SetFont(font)
		self.Bind(wx.EVT_CHECKBOX, self.evtCheckBox, self.cbAuto)
		ribbon.Add(self.cbAuto, 3, wx.ALIGN_CENTER_VERTICAL)
		
		ribbon.AddSpacer((5,5))
		
		self.scIntv = wx.SpinCtrl(self, -1, "", size=(30, -1))
		self.scIntv.SetRange(1,300)
		self.scIntv.SetValue(self.settings.interval)
		self.Bind(wx.EVT_SPINCTRL, self.onSpin, self.scIntv)
		ribbon.Add(self.scIntv, 1, wx.ALIGN_CENTER_VERTICAL)
		
		ribbon.AddSpacer((5,5))
		
		t = wx.StaticText(self, wx.ID_ANY, "seconds")
		t.SetFont(font)
		ribbon.Add(t, 1, wx.ALIGN_CENTER_VERTICAL)
		
		ribbon.AddSpacer((5,5))
		
		self.bSnapshot = wx.BitmapButton(self, wx.ID_ANY, self.imageSnapshot, size=(48, 48))
		self.bSnapshot.SetToolTipString("Take a picture")
		self.Bind(wx.EVT_BUTTON, self.onSnapshot, self.bSnapshot)
		ribbon.Add(self.bSnapshot, 1, wx.ALL, 10)
		
		ribbon.AddSpacer((10, 10))
		
		self.sizer.Add(ribbon)
		
		self.SetSizer(self.sizer)
		self.Layout()
		self.Fit()
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)        
		self.timer.Start(MAINTIMER)
		self.Update()
		
	def loadImages(self):
		fp =  os.path.join(cmd_folder, "refresh.png")	
		self.imageRefresh = wx.Image(fp, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		mask = wx.Mask(self.imageRefresh, wx.BLUE)
		self.imageRefresh.SetMask(mask)
		
		fp =  os.path.join(cmd_folder, "snapshot.png")	
		self.imageSnapshot = wx.Image(fp, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		mask = wx.Mask(self.imageSnapshot, wx.BLUE)
		self.imageSnapshot.SetMask(mask)
		
	def onTimer(self, evt):
		if self.settings.autoRefresh:
			self.count += 1
			if self.count >= self.settings.interval:
				self.count = 0
				self.Update()

	def onClose(self, evt):
		self.settings.save()
		self.Destroy()
		
	def onRefresh(self, evt):
		self.Update()
		
	def evtCheckBox(self, evt):
		self.settings.autoRefresh = self.cbAuto.GetValue()
		if self.settings.autoRefresh:
			self.count = 0
			
	def onSpin(self, evt):
		self.settings.interval = self.scIntv.GetValue()
		
	def onSnapshot(self, evt):
		s = Snapshot(self, self.settings)
		if s.wasSuccessful():
			s.Show()
		else:
			dlg = wx.MessageDialog(self, "Error Taking Picture",
					'Camera Error', wx.OK | wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()
		
	def Update(self):
		self.bRefresh.Disable()
		self.thr = UpdateThread(self, self.rrs)
		self.thr.Start()
		
	def continueUpdate(self, evt):
		s = self.thr.getStatus()
		t = self.thr.getTemps()
		self.thr = None
		
		self.bRefresh.Enable()
		
		try:
			sNC = s['status::nconnections']
		except KeyError:
# 			print "Key error - closing application"
# 			self.onClose(None)
# 			return
			sNC = "0"
			
		try:
			nc = int(sNC)
		except:
			nc = 0
			
		title = "Reprep Status: %d connection" % nc
		if nc != 1:
			title += 's'
			
		self.SetTitle(title)
			
		for i in range(nc):
			if i >= len(self.conn):
				cn = Connection(self, i, t.keys())
				self.conn.append(cn)
				cn.Show()
# 				self.sizer.Add(cn)
# 				self.Layout()
# 				self.Fit()
			self.conn[i].Update(s, t)
			
		while len(self.conn) > nc:
			cn = self.conn[-1]
			del self.conn[-1]
# 			self.sizer.Remove(cn)
			cn.onClose(None)
# 			self.Layout()
# 			self.Fit()
	
class App(wx.App):
	def OnInit(self):
		settings = Settings(cmd_folder)
		rrs = RepRapServer(settings.ipAddress, settings.port)
		frame = MainFrame(rrs, settings)
		frame.Show()
		self.SetTopWindow(frame)
		return True

app = App(False)
app.MainLoop()


