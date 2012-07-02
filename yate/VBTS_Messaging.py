#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys

to_be_handled = [("sip.message", 50)]

class VBTS:
	""" initialize the object """
	def __init__(self):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_Messaging.VBTS")
		self.ym = YateMessenger.YateMessenger()

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS Messaging event: empty")
		elif d == "incoming":
			self.app.Output("VBTS Messaging received: " +  self.app.name + " id: " + self.app.id)
			self.log.info("VBTS Messaging received: " +  self.app.name + " id: " + self.app.id)
			res = self.ym.parse(self.app.params)
			self.log.info(str(res))
			self.app.handled = True			
			self.app.retval = "202"
			self.app.Acknowledge()
			
			self.ym.send_smqueue_sms(self.app, res["vbts_tp_dest_address"], "%s <sip:%s@%s>" % (res["caller"], res["caller"], res["address"]), res["vbts_text"])
		elif d == "answer":
			self.app.Output("VBTS Messaging Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS Messaging Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS Messaging Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS Messaging event: " + self.app.type )
			
	def uninstall(self):
		for (msg, pri) in to_be_handled:
			self.app.Uninstall(msg)

	def main(self):
		try:
			self.app.Output("VBTS Messaging Starting")

			for (msg, pri) in to_be_handled:
				self.app.Install(msg, pri)

			while True:
				self.app.flush()
		except:
			self.app.Output("Unexpected error:" + str(sys.exc_info()[0]))
			self.close()
					
	def close(self):
		self.uninstall()
		self.app.close()
		
if __name__ == '__main__':
	logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
	vbts = VBTS()
	vbts.main()
