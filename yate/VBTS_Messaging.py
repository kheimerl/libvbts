#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger

to_be_handled = [("sip.message", 10)]

class VBTS:
	""" initialize the object """
	def __init__(self):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall

	def yatecall(self, d):
		if d == "":
			self.app.Output("PYTHON event: empty")
		elif d == "incoming":
			self.app.Output("PYTHON message: " +  self.app.name + " id: " + self.app.id)
			self.app.handled = True
			self.app.Output(str(self.app.params))
			res = self.ym.parse(self.app.params)
			self.app.Output(str(res))
			self.app.retval = "202"
			self.app.Acknowledge()
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
		self.app.Yate("VBTSMessaging.start")
		self.app.retval = "true"
		self.app.params = []
		self.app.Dispatch()

		self.ym = YateMessenger.YateMessenger()

		self.app.Output("VBTS Handler Starting")

		for (msg, pri) in to_be_handled:
			self.app.Install(msg, pri)


		while True:
			self.app.flush()
	def close(self):
		self.uninstall()
		self.app.close()
		
if __name__ == '__main__':
	vbts = VBTS()
	vbts.main()
