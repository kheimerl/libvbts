#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys
import re
import time

class VBTS_Echo:
	""" initialize the object """
	def __init__(self, to_be_handled):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_SMS_Echo.VBTS_Echo")
		self.ym = YateMessenger.YateMessenger()
		self.to_be_handled = to_be_handled

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS ECHO event: empty")
		elif d == "incoming":

			#ensure it's an IMSI
			if (not self.ym.is_imsi(self.ym.get_param("caller", self.app.params))):
				self.app.Acknowledge()
				return

			res = self.ym.parse(self.app.params)
			for (tag, re) in self.regexs:
				if (not res.has_key(tag) or not re.match(res[tag])):
					self.app.Output("VBTS ECHO %s did not match" % (tag,))
					self.app.Acknowledge()
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
			self.app.Output("VBTS ECHO Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS ECHO Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS ECHO Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS ECHO event: " + self.app.type )
			
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

def Usage():
	ret = "VBTS ECHO ERROR: Please provide a priority and a regex to match against\n"
	ret += "CMD PRIORITY [FIELD REGEX]?"
	return ret

def Error(app, log):
	err = Usage()
	vbts.app.Output(err)
	vbts.log.error(err)
	exit(2)

if __name__ == '__main__':
	logging.basicConfig(filename="/var/log/VBTS.log", level="DEBUG")
	to_be_handled = ["sip.message"]
	vbts = VBTS_Echo(to_be_handled)
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
	vbts.app.Output("VBTS Echo_SMS filtering: " + str(pairs))
	vbts.main(priority, pairs)
