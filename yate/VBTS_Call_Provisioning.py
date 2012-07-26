#!/usr/bin/python
from libyate import Yate
from libvbts import YateMessenger
import logging
import sys
import re
import time
import random

def uniqid(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

class IVR:

	""" initialize the object """
	def __init__(self, to_be_handled):
		self.app = Yate()
		self.app.__Yatecall__ = self.yatecall
		self.log = logging.getLogger("libvbts.yate.playrec.IVR")
		self.ym = YateMessenger.YateMessenger()
		self.to_be_handled = to_be_handled
		self.state = "call"
		self.ourcallid = "playrec/" + uniqid(10)
		self.partycallid = ""
		self.dir = "/tmp"

	def setState(self, state):
		if (state == ""):
			return
		self.app.Output("setState('%s') state: %s" % (self.state, state))
		
		#if we get this, replay the prompt
		if (state == "prompt"):
			self.state = state
			m = Yate("chan.attach")
			m.params.append(["source", "wave/play//tmp/test.gsm"])
			m.Dispatch()
			m = Yate("chan.attach")
			m.params.append(["consumer", "wave/record/-"])
			m.params.append(["maxlen", 320000])
			m.params.append(["notify", self.callid])
			m.Dispatch()
			return

		if (state == self.state):
			return
		
		if (state == "record"):
			m = Yate("chan.attach")
			m.params.append(["source", "wave/play/-"])
			m.params.append(["consumer", "wave/record/" + self.dir + "/playrec.gsm"])
			m.params.append(["maxlen", 80000])
			m.params.append(["notify", self.ourcallid])
			m.Dispatch()
		elif (state == "play"):
			m = Yate("chan.attach")	
			m.params.append(["source","wave/play/" + self.dir + "/playrec.gsm"])
			m.params.append(["consumer", "wave/record/-"])
			m.params.append(["maxlen", 480000])
			m.params.append(["notify", self.ourcallid])
			m.Dispatch()
		elif (state == "goodbye"):
			m = Yate("chan.attach")	
			m.params.append(["source","tone/congestion"])
			m.params.append(["consumer", "wave/record/-"])
			m.params.append(["maxlen", 32000])
			m.params.append(["notify", self.ourcallid])
			m.Dispatch()
		#update state
		self.state = state

	def gotNotify(self, reason):
		self.app.Output("gotNotify() state: %s" % (self.state,))
		if (reason == "replace"):
			return
		elif (reason == "goodbye"):
			self.setState("")
		elif (reason == "prompt"):
			self.setState("goodbye")
		elif (reason == "record" or reason == "play"):
			self.setState("prompt")
		

	def gotDTMF(self, text):
		self.app.Output("gotDTMF('%s') state: %s" % (text, self.state));
		if (text == "1"):
			self.setState("record")
		elif (text == "2"):
			self.setState("play")
		elif (text == "3"):
			self.setState("")
		elif (text == "#"):
			self.setState("prompt")
			

	def yatecall(self, d):
		if d == "":
			self.app.Output("VBTS IVR event: empty")
		elif d == "incoming":
			self.app.Output("VBTS IVR Incoming: " +  self.app.name + " id: " + self.app.id)
			if (self.app.name == "call.execute"):
				self.partycallid = self.app.id
				self.ym.add_param("targetid", self.ourcallid, self.app.params)
				self.app.handled = True
				self.app.Acknowledge()

				m = Yate("call.answered")
				self.app.id = self.outcallid
				self.ym.add_param("targetid", self.partycallid, m.params)
				m.Dispatch()

				self.setState("prompt")
				return
			elif (self.app.name == "chan.notify"):
				if (self.ym.get_param("targetid", self.app.params) == self.ourcallid):
					self.gotNotify(self.ym.get_param("reason", self.app.params))
					self.app.handled = True
					self.app.Acknowledge()
				return
			elif (self.app.name == "chan.dtmf"):
				if (self.ym.get_param("targetid", self.app.params) == self.ourcallid):
					text =self.ym.get_param("text", self.app.params)
					for (t in text):
						self.gotDTMF(t)
					self.app.handled = True
					self.app.Acknowledge()

		elif d == "answer":
			self.app.Output("VBTS IVR Answered: " +  self.app.name + " id: " + self.app.id)
		elif d == "installed":
			self.app.Output("VBTS IVR Installed: " + self.app.name )
		elif d == "uninstalled":
			self.app.Output("VBTS IVR Uninstalled: " + self.app.name )
		else:
			self.app.Output("VBTS IVR event: " + self.app.type )
			
	def uninstall(self):
		for (msg, pri) in self.to_be_handled:
			self.app.Uninstall(msg)

	def main(self, priority, regexs):
		self.regexs = regexs
		try:
			self.app.Output("VBTS IVR Starting")

			for msg in to_be_handled:
				self.app.Output("VBTS IVR Installing %s at %d" % (msg, priority))
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
	to_be_handled = ["chan.dtmf", "chan.notify"]
	vbts = Call_Route(to_be_handled)
	priority = int(sys.argv[1])
	pairs = []
	vbts.app.Output("VBTS Call Routing on")
	vbts.main(priority, pairs)
