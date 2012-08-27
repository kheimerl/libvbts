#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys
import time

class VBTS:
	""" initialize the object """
	def __init__(self, to_be_handled):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.to_be_handled = to_be_handled
		self.log = logging.getLogger("libvbts.yate.VBTS_SMS_Route.VBTS")
		self.ym = YateMessenger.YateMessenger()

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS SMS_Route event: empty")
		elif d == "incoming":
			res = self.ym.parse(self.app.params)
			for (tag, re) in self.regexs:
				if (not res.has_key(tag) or not re.match(res[tag])):
					self.app.Output("VBTS SMS_Route %s did not match" % (tag,))
					return
			self.app.Output("VBTS SMS_Route received: " +  self.app.name + " id: " + self.app.id)
			self.log.info("VBTS SMS_Route received: " +  self.app.name + " id: " + self.app.id)
			self.app.handled = True	
			self.app.retval = "202"
			self.app.Acknowledge()
			
			self.ym.send_smqueue_sms(self.app, res["vbts_tp_dest_address"], "%s <sip:%s@%s>" % (res["caller"], res["caller"], res["address"]), res["vbts_text"])
		elif d == "answer":
			self.app.Output("VBTS SMS_Route Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS SMS_Route Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS SMS_Route Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS SMS_Route event: " + self.app.type )
			
	def uninstall(self):
		for (msg, pri) in self.to_be_handled:
			self.app.Uninstall(msg)

	def main(self, priority, regexs):
		self.regexs = regexs
		try:
			self.app.Output("VBTS SMS_Route Starting")
			for msg in to_be_handled:
				self.app.Output("VBTS SMS_Route Installing %s at %d" % (msg, priority))
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
	#this is mostly boilterplate arg parsing. I'll probably wrap it into ym
	logging.basicConfig(filename="/var/log/VBTS.log", level="DEBUG")
	to_be_handled = ["sip.message"]
	vbts = VBTS(to_be_handled)
	if (len(sys.argv) < 2):
		Error(vbts.app, vbts.log)
	args = sys.argv[1].split("|")
	#if it's not odd length...
	if (len(args) % 2 == 0 or args[0] == ""):
		Error(vbts.app, vbts.log)
	priority = int(args[0])
	args = args[1:]
	pairs = []
	for i in range(len(args)/2):
		i *= 2
		pairs.append((args[i], re.compile(args[i+1])))
	vbts.app.Output("VBTS SMS_Route filtering: " + str(pairs))
	vbts.main(priority, pairs)

