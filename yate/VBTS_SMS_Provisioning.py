#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys
import time

def Usage():
	ret = "VBTS Provisioning ERROR: Please provide a priority\n"
	ret += "CMD PRIORITY"
	return ret

def Output(app, log, msg):
	vbts.app.Output(msg)
	vbts.log.error(msg)

def Error(app, log):
	msg = Usage()
	Output(msg)
	exit(1)

class VBTS_Provisioning:
	""" initialize the object """
	def __init__(self, to_be_handled):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_SMS_Provisioning.VBTS_Provisioning")
		self.ym = YateMessenger.YateMessenger()
		self.to_be_handled = to_be_handled

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS Provisioning event: empty")
		elif d == "incoming":
			res = self.ym.parse(self.app.params)
			Output(self.app, self.log, "VBTS Provisioning received: " +  self.app.name + " id: " + self.app.id)
			
			sender_name = res["caller"]
			#look up their number to set to return
			sender_num = self.ym.SR_get("callerid", ("name", sender_name))
			#they're in the system, pass on it
			if (sender_num):
				self.app.Acknowledge()
			#otherwise redirect to provisioning script
			else:
				self.app.handled = True			
				self.app.retval = "202"
				self.app.Acknowledge()
				#originate a new call
				self.ym.originate(self.app, res["caller"], "101", "external/nodata/VBTS_Call_Provisioning.py", 
						  ipaddr=res["ip_host"], port=res["ip_port"])

		elif d == "answer":
			self.app.Output("VBTS Provisioning Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS Provisioning Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS Provisioning Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS Provisioning event: " + self.app.type )
			
	def uninstall(self):
		for (msg, pri) in self.to_be_handled:
			self.app.Uninstall(msg)

	def main(self, priority):
		try:
			self.app.Output("VBTS Provisioning Starting")

			for msg in to_be_handled:
				self.app.Output("VBTS Provisioning_SMS Installing %s at %d" % (msg, priority))
				self.log.info("Installing %s at %d" % (msg, priority))
				self.app.Install(msg, priority)

			while True:
				self.app.flush()
				time.sleep(0.1)
		except:
			self.app.Output("Unexpected error:" + str(sys.exc_info()[0]))
			self.close()
					
	def close(self):
		self.uninstall()
		self.app.close()

if __name__ == '__main__':
	logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
	to_be_handled = ["sip.message"]
	vbts = VBTS_Provisioning(to_be_handled)
	if (len(sys.argv) < 2):
		Error(vbts.app, vbts.log)
	priority = int(sys.argv[1])
	vbts.main(priority)
