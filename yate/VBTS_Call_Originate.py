#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import base64
import logging
import sys

class YateOriginator:
	""" initialize the object """
	def __init__(self):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.VBTS_Originate_Call.YateOriginator")
		self.ym = YateMessenger.YateMessenger()

	def yatecall(self, d):
		self.app.Output("YateSMSSender Event: " + self.app.type )

	def originate(self, name, ret, dest):
		self.ym.originate(self.app, name, ret, dest)
		     
	def close(self):
		self.app.close()
		
if __name__ == '__main__':
	import getopt
	logging.basicConfig(filename="/var/log/VBTS.log", level="DEBUG")
	log = logging.getLogger("libvbts.yate.VBTS_Originate_Call.__main__")
	y = YateOriginator()
	res = sys.argv[1].split('|')
	if (len(res) != 3):
		log.info("Originate: Malformed Args")
		y.app.Output("libvbts.yate.VBTS_Originate_Call: Malformed Args")
		y.close()
		exit(1)
	y.originate(res[0],res[1],res[2])
	y.close()
