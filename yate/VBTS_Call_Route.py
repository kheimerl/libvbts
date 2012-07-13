#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys
import re
import time

class Call_Route:
	""" initialize the object """
	def __init__(self, to_be_handled):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_Call_Route.Call_Route")
		self.ym = YateMessenger.YateMessenger()
		self.to_be_handled = to_be_handled

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS Call Route event: empty")
		elif d == "incoming":
			self.app.Output("VBTS Call Route received: " +  self.app.name + " id: " + self.app.id)
			self.log.info("VBTS Call Route received: " +  self.app.name + " id: " + self.app.id)
			#get the destination name
			target = self.ym.SR_get("name", ("callerid", self.ym.get_param("called", self.app.params)))
			#and the caller's number
			caller_num = self.ym.SR_get("callerid", ("name", self.ym.get_param("callername", self.app.params)))
			if (target and caller_num):
				target_ip = self.ym.SR_get("ipaddr", ("name", target))
				target_port = self.ym.SR_get("port", ("name", target))
				self.app.retval = "sip/%s@%s:%s" % (target, target_ip, target_port)
				self.ym.add_param("caller", caller_num, self.app.params)
				self.ym.add_param("callername", caller_num, self.app.params)
				self.app.handled = True	
				self.app.Acknowledge()
			
		elif d == "answer":
			self.app.Output("VBTS Call Route Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS Call Route Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS Call Route Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS Call Route event: " + self.app.type )
			
	def uninstall(self):
		for (msg, pri) in self.to_be_handled:
			self.app.Uninstall(msg)

	def main(self, priority, regexs):
		self.regexs = regexs
		try:
			self.app.Output("VBTS Echo Starting")

			for msg in to_be_handled:
				self.app.Output("VBTS Echo_SMS Installing %s at %d" % (msg, priority))
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
	to_be_handled = ["call.route"]
	vbts = Call_Route(to_be_handled)
	priority = int(sys.argv[1])
	pairs = []
	vbts.app.Output("VBTS Call Routing on")
	vbts.main(priority, pairs)
