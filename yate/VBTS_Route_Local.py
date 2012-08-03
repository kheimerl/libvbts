#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys
import re
import time

class Route_Local:
	""" initialize the object """
	def __init__(self, to_be_handled):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_Route_Local.Route_Local")
		self.ym = YateMessenger.YateMessenger()
		self.to_be_handled = to_be_handled

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS Route Local event: empty")
		elif d == "incoming":
			self.app.Output("VBTS Route Local received: " +  self.app.name + " id: " + self.app.id)
			self.log.info("VBTS Route Local received: " +  self.app.name + " id: " + self.app.id)
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
			
			#ack regardless
			self.app.Acknowledge()
			
		elif d == "answer":
			self.app.Output("VBTS Route Local Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS Route Local Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS Route Local Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS Route Local event: " + self.app.type )
			
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
	vbts = Route_Local(to_be_handled)
	priority = int(sys.argv[1])
	pairs = []
	vbts.app.Output("VBTS Route Local on")
	vbts.main(priority, pairs)
