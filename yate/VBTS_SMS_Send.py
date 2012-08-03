#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import base64
import logging
import sys

class YateSMSSender:
	""" initialize the object """
	def __init__(self):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_Send_SMS.YateSMSSender")
		self.ym = YateMessenger.YateMessenger()

	def yatecall(self, d):
		self.app.Output("YateSMSSender Event: " + self.app.type )

	def send_sms(self, to_addy, to_num, fromm, body, plain):
		self.log.info("Sending: " + to_addy + " " + to_num + " " + fromm + " " + body)
		self.app.Yate("xsip.generate")
		self.app.retval="true"
		self.app.params = []
		self.app.params.append(["method","MESSAGE"])
		self.app.params.append(["uri", to_addy])
		self.app.params.append(["sip_from", fromm])
		if (plain):
			self.app.params.append(["xsip_type", "text/plain"])
			self.app.params.append(["xsip_body", body])
		else:
			self.app.params.append(["xsip_type", "application/vnd.3gpp.sms"])
			self.app.params.append(["xsip_body_encoding", "base64"]) 
			self.app.params.append(["xsip_body", base64.b64encode(self.ym.generate(str(to_num), body))])
		self.app.Dispatch() 
		     
	def output(self, string):
		self.app.Output(string)

	def close(self):
		self.app.close()
		
if __name__ == '__main__':
	import getopt
	logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
	logging.getLogger("libvbts.yate.VBTS_Send_SMS.__main__")
	y = YateSMSSender()

	def usage(y):
		y.output ("Script for sending direct MESSAGEs in yate")
		y.output ("VBTS_Send_SMS.py TO_NAME|TO_NUM|FROM_NAME|BODY|[plain]")
		y.close()

	args = ["sip:smsc@127.0.0.1:5060", 
		"101", 
		"IMSI460010018073482 <sip:IMSI460010018073482@127.0.0.1>",
		"Test",
		False]

	if (len(sys.argv) > 1):
		if ("help" in sys.argv[1]):
			usage(y)
			exit(1)
		new_args = sys.argv[1].split("|")
		for i in range(len(new_args)):
			new_args[i] = new_args[i].strip() 
			if (i == 4):
				args[i] = (new_args[i] == "plain")
			elif (new_args[i] != ""):
				args[i] = new_args[i]
	
	y.send_sms(args[0],args[1],args[2],args[3], args[4])
	y.close()
