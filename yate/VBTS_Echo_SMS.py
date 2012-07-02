#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys

to_be_handled = [("sip.message", 10)]

NUMBER = "100"

class VBTS_Echo:
	""" initialize the object """
	def __init__(self):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_SMS_Echo.VBTS_Echo")
		self.ym = YateMessenger.YateMessenger()

	def yatecall(self, d):
		if d == "":
			self.app.Output("PYTHON event: empty")
		elif d == "incoming":
			res = self.ym.parse(self.app.params)
			#not us, pass on
			if (res["vbts_tp_dest_address"] != NUMBER):
				return
			self.app.Output("VBTS ECHO received: " +  self.app.name + " id: " + self.app.id)
			self.log.info("VBTS ECHO received: " +  self.app.name + " id: " + self.app.id)
			self.app.handled = True			
			self.app.retval = "202"
			self.app.Acknowledge()

			sender_name = res["caller"]
			#look up their number to set to return
			sender_num = self.ym.SR_get("callerid", ("name", sender_name))
			self.ym.send_openbts_sms(self.app, sender_name, "<sip:%s@127.0.0.1>" % (sender_num,), res["vbts_text"])
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
			self.app.Output("VBTS Echo Starting")

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
	vbts = VBTS_Echo()
	vbts.main()
