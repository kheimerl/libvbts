#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys

to_be_handled = [("sip.message", 10)]

class VBTS:
	""" initialize the object """
	def __init__(self):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_Messaging.VBTS")
		self.ym = YateMessenger.YateMessenger()

	def yatecall(self, d):
		if d == "":
			self.app.Output("PYTHON event: empty")
		elif d == "incoming":
			self.app.Output("VBTS message received: " +  self.app.name + " id: " + self.app.id)
			self.log.info("VBTS message received: " +  self.app.name + " id: " + self.app.id)
			res = self.ym.parse(self.app.params)
			self.log.info(str(res))
			self.app.handled = True			
			self.app.retval = "202"
			self.app.Acknowledge()
			#sender_name = res["caller"]
			
			self.ym.send_smqueue_sms(self.app, res["vbts_tp_dest_address"], "%s <sip:%s@%s>" % (res["caller"], res["caller"], res["address"]), res["vbts_text"])
		elif d == "answer":
			self.app.Output("PYTHON Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("PYTHON Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("PYTHON Uninstalled: " + self.app.name )
		else:
			self.app.Output("PYTHON event: " + self.app.type )
			
	def uninstall(self):
		for (msg, pri) in to_be_handled:
			self.app.Uninstall(msg)

	def main(self):
		try:
			self.app.Output("VBTS Handler Starting")

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
