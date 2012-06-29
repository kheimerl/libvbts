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

	def send_sms(self, to_addy, to_num, fromm, body):
		self.log.info("Sending: " + to_addy + " " + to_num + " " + fromm + " " + body)
		self.app.Yate("xsip.generate")
		self.app.retval="true"
		self.app.params = []
		self.app.params.append(["method","MESSAGE"])
		self.app.params.append(["uri", to_addy])
		self.app.params.append(["sip_from", fromm])
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
	y = YateSMSSender()

	def usage(y):
		y.output ("Script for sending direct MESSAGEs in yate")
		y.output ("-h | --help Show this message")
		y.output ("-t | --to_addy= The SIP address to send to")
		y.output ("-n | --to_number= The number stored in the 3GPP message")
		y.output ("-f | --from= The from SIP field")
		y.output ("-b | --body= The body text")
		y.close()

	to_addy = "sip:smsc@127.0.0.1:5060"
	to_num = "101"
	fromm = "IMSI460010018073482 <sip:IMSI460010018073482@127.0.0.1>"
	body = "Test"

	opts, args = getopt.getopt(sys.argv[1:], 
				   "b:f:t:n:h", ["help", "body=", "from=", "to_addy=", "to_number="])
	for o,a in opts:
		if o in ("-b", "--body="):
			body = a
		elif o in ("-f", "--from="):
			fromm = a
		elif o in ("-t", "--to_addy="):
			to_addy = a
		elif o in ("-n", "--to_number="):
			to_num = a
		else:
			usage(y)
	
	y.send_sms(to_addy, to_num,
		   fromm, body)
	y.close()
