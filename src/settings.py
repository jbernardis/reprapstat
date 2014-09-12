import ConfigParser
import os

INIFILE = "reprapstat.ini"

def parseBoolean(val, defaultVal):
	lval = val.lower();
	
	if lval == 'true' or lval == 't' or lval == 'yes' or lval == 'y':
		return True
	
	if lval == 'false' or lval == 'f' or lval == 'no' or lval == 'n':
		return False
	
	return defaultVal

class Settings:
	def __init__(self, folder):
		self.inifile = os.path.join(folder, INIFILE)
		
		self.ipAddress = "192.168.1.211"
		self.port = "8989"
		self.interval = 60
		self.autoRefresh = True
		self.section = "reprapstat"	
		
		self.cfg = ConfigParser.ConfigParser()
		if not self.cfg.read(self.inifile):
			print("Settings file %s does not exist.  Using default values" % INIFILE)
			return

		if self.cfg.has_section(self.section):
			for opt, value in self.cfg.items(self.section):
				if opt == 'ip':
					self.ipAddress = value
				elif opt == 'autorefresh':
					self.autoRefresh = parseBoolean(value, True)
				elif opt == 'port':
					self.port = value
				elif opt == 'interval':
					try:
						self.interval = int(value)
					except:
						print "Unable to parse value for interval - defaulting to 60"
						self.interval = 60
				else:
					print("Unknown %s option: %s - ignoring" % (self.section, opt))
		else:
			print("Missing %s section - assuming defaults" % self.section)
				
	def save(self):
		try:
			self.cfg.add_section(self.section)
		except ConfigParser.DuplicateSectionError:
			pass
		
		self.cfg.set(self.section, "ip", str(self.ipAddress))
		self.cfg.set(self.section, "port", str(self.port))
		self.cfg.set(self.section, "interval", str(self.interval))
		self.cfg.set(self.section, "autorefresh", str(self.autoRefresh))
		
		try:		
			cfp = open(self.inifile, 'wb')
		except:
			print "Unable to open settings file %s for writing" % self.inifile
			return
		self.cfg.write(cfp)
		cfp.close()

