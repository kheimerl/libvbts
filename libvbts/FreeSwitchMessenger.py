#Copyright 2012 Kurtis Heimerl <kheimerl@cs.berkeley.edu>. All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are
#permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this list of
#      conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this list
#      of conditions and the following disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY Kurtis Heimerl ''AS IS'' AND ANY EXPRESS OR IMPLIED
#WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Kurtis Heimerl OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those of the
#authors and should not be interpreted as representing official policies, either expressed
#or implied, of Kurtis Heimerl.

import logging
import Messenger
from freeswitch import *

#handles yate specific messaging
class FreeSwitchMessenger(Messenger.Messenger):

    def __init__(self):
        Messenger.Messenger.__init__(self)
        self.log = logging.getLogger("libvbts.FreeSwitchMessenger.FreeSwitchMessenger")

    def parse(self, msg):
        return Messenger.Messenger.parse(self, msg)

    def send_openbts_sms(self, msg, to, fromm, body, empty=False):
        for b in self.chunk_sms(body):
            self.__send_openbts_sms(msg, to, fromm, b, empty)

    def send_smqueue_sms(self, msg, to, fromm, body, empty=False):
        for b in self.chunk_sms(body):
            self.__send_smqueue_sms(msg, to, fromm, b, empty)

    def __send_openbts_sms(self, msg, to, fromm, body, empty=False):
        IMSI = to[0]
        ipaddr = to[1]
        port = to[2]
        body = self.gen_sms_deliver(to, fromm, body, empty).upper()
        consoleLog('info', 'Message body is: \'' + str(body) + '\'\n')

        event = Event("CUSTOM", "SMS::SEND_MESSAGE")
        event.addHeader("proto", "sip")
        event.addHeader("dest_proto", "sip")
        event.addHeader("from", fromm)
        event.addHeader("from_full", "sip:" + fromm + "@" + getGlobalVariable("domain"))
        event.addHeader("to", str(getGlobalVariable("smqueue_profile") + "/sip:" + str(IMSI) + "@" + ipaddr + ":" + str(port)))
        event.addHeader("subject", "SIMPLE_MESSAGE")
        event.addHeader("type", "application/vnd.3gpp.sms")
        event.addHeader("hint", "the hint")
        event.addHeader("replying", "false")
        event.addBody(body)

        event.fire()

    def __send_smqueue_sms(self, msg, to, fromm, body, empty=False):
        event = Event("CUSTOM", "SMS::SEND_MESSAGE")
        event.addHeader("proto", "sip");
        event.addHeader("dest_proto", "sip");
        event.addHeader("from", fromm)
        event.addHeader("from_full", "sip:" + fromm + "@" + getGlobalVariable("domain"))
        event.addHeader("to", str(getGlobalVariable("smqueue_profile") + "/sip:smsc@" + self.smqueue_get("SIP.myIP") + ":" + self.smqueue_get("SIP.myPort")))
        event.addHeader("subject", "SIMPLE_MESSAGE")
        event.addHeader("type", "application/vnd.3gpp.sms");
        event.addHeader("hint", "the hint");
        event.addHeader("replying", "false");
        event.addBody(self.gen_sms_submit(to, body, empty));

        event.fire()

if __name__ == '__main__':
    pass


def chat(message, args):
    args = args.split('|')
    if (len(args) < 3):
        consoleLog('err', 'Missing Args\n')
        exit(1)
    to = args[0]
    fromm = args[1]
    text = args[2]
    if ((not to or to == '') or
        (not fromm or fromm == '')):
        consoleLog('err', 'Malformed Args\n')
        exit(1)

    #messenger
    m = FreeSwitchMessenger()
    m.send_openbts_sms("", to, fromm, text)

def fsapi(session, stream, env, args):
    #chat doesn't use message anyhow
    chat(None, args)
