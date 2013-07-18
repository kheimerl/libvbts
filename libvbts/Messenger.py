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
import sys
import SMS_Parse
import SMS_Deliver
import SMS_Submit
import Configuration
import SubscriberRegistry
import os
import re
import time
import xmlrpclib

SMS_LENGTH = 160

class Messenger:

    def __init__(self, openbtsConf="/etc/OpenBTS/OpenBTS.db",
                 smqueueConf="/etc/OpenBTS/smqueue.db",
                 sipauthserveConf="/etc/OpenBTS/sipauthserve.db"):
        reload(SubscriberRegistry)
        self.log = logging.getLogger("libvbts.VBTSMessenger.Messenger")
        self.openbts_conf = Configuration.getConfig(openbtsConf)
        self.smqueue_conf = Configuration.getConfig(smqueueConf)
        #this will be the same as openbtsConf for range boxes -kurtis
        if (os.path.exists(sipauthserveConf)):
            self.sipauthserve_conf = Configuration.getConfig(sipauthserveConf)
        else:
            self.sipauthserve_conf = Configuration.getConfig(openbtsConf)
        self.sr = SubscriberRegistry.getSubscriberRegistry(self.sipauthserve_conf.getField("SubscriberRegistry.db"))

    def parse(self, msg):
        self.log.info("MessengerParse " + str(msg))
        return SMS_Parse.parse(msg)

    def send_openbts_sms(self, msg, to, fromm, body, empty=False):
        raise NotImplementedError("Subclass Messenger")

    def send_smqueue_sms(self, msg, to, fromm, body, empty=False):
        raise NotImplementedError("Subclass Messenger")

    def chunk_sms(self, body):
        res = []
        i = 0
        while (i + SMS_LENGTH < len(body)):
            res.append(body[i:i+SMS_LENGTH])
            i += SMS_LENGTH
        res.append(body[i:])
        return res

    #Generates the body of an SMS deliver (n->ms). If 'empty' is True, an empty SMS is generated
    def gen_sms_deliver(self, to, fromm, txt, empty=False):
        return SMS_Deliver.gen_msg(to, fromm, txt, empty)

    #Generates the body of an SMS submit (ms->n). If 'empty' is True, an empty SMS is generated
    def gen_sms_submit(self, to, txt, empty=False):
        return SMS_Submit.gen_msg(to, txt, empty)

    #Generates the body of the message. If 'empty' is True, an empty SMS is sent
    def generate(self, to, txt, empty = False):
        return SMS_Generate.gen_msg(to, txt, empty)

    def originate(self, msg, to, fromm, dest, ipaddr=None, port=None):
        raise NotImplementedError("Subclass Manager")

    def SR_get(self, item, qualifier):
        try:
            return self.sr.get(item, qualifier)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def SR_dialdata_get(self, item, qualifier):
        try:
            return self.sr.get_dialdata(item, qualifier)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def SR_get_current_location(self, imsi, fields=('latitude', 'longitude')):
        try:
            return self.sr.get_current_location(imsi, fields)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def SR_set(self, set_pair, qualifier):
        try:
            return self.sr.set(set_pair, qualifier)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def SR_dialdata_set(self, set_pair, qualifier):
        try:
            return self.sr.set_dialdata(set_pair, qualifier)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def SR_provision(self, name, number, ipaddr, port):
        return self.sr.provision(name, number, ipaddr, port)

    def openbts_get(self, field):
        try:
            return self.openbts_conf.getField(field)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def smqueue_get(self, field):
        try:
            return self.smqueue_conf.getField(field)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def sipauthserve_get(self, field):
        try:
            return self.sipauthserve_conf.getField(field)
        except Exception as e:
            self.log.debug(str(e))
            raise e

    def is_imsi(self, imsi):
        return (imsi != None and re.match("^IMSI\d{15}$", imsi) != None)

    def wakeup(self, number, reason):
        #find that person
        name = str(self.SR_dialdata_get('dial', ('exten', number)))
        #get their information
        ipaddr = str(self.SR_get('ipaddr', ('name', name)))
        port = str(self.openbts_conf.getField('VBTS.PA.RPCPort'))
        if (port and port not in ["", "None"] and ipaddr and ipaddr not in ["", "None"]):
            try:
                s = xmlrpclib.ServerProxy('http://' + ipaddr + ":" + port)
                s.onWithReason(str(reason))
            except Exception as e:
                self.log.debug(str(e))
                raise e
        else:
            raise Exception("Bad Target")


if __name__ == '__main__':
    h = "000000069133010000F019069133010000F011000A9133163254760000AA05F330BB4E07"
    imsi = 'IMSI510555550000396'
    m = Messenger()
    a,b = m.SR_get_current_location(imsi)
    print "%f, %f"  % (a, b)
