#Copyright 2011 Kurtis Heimerl <kheimerl@cs.berkeley.edu>. All rights reserved.
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
import SMS_Generate
import Configuration
import SubscriberRegistry

class Messenger:

    def __init__(self, openbtsConf="/etc/OpenBTS/OpenBTS.db", 
                 smqueueConf="/etc/OpenBTS/smqueue.db", 
                 sipauthserveConf="/etc/OpenBTS/sipauthserve.db"):
        self.log = logging.getLogger("libvbts.VBTSMessenger.Messenger")
        self.openbts_conf = Configuration.getConfig(openbtsConf)
        self.smqueue_conf = Configuration.getConfig(smqueueConf)
        #this will be the same as openbts_conf for range boxes -kurtis
        self.sipauthserve_conf = Configuration.getConfig(sipauthserveConf)
        self.sr = SubscriberRegistry.getSubscriberRegistry(self.sipauthserve_conf.getField("SubscriberRegistry.db")[0])

    def parse(self, msg):
        self.log.info("MessengerParse " + str(msg))
        return SMS_Parse.parse(msg)

    def send_openbts_sms(self, msg, to, fromm, body):
        raise NotImplementedError("Subclass Messager")

    def send_smqueue_sms(self, msg, to, fromm, body):
        raise NotImplementedError("Subclass Messager")

    #generates the body message
    def generate(self, to, txt):
        return SMS_Generate.gen_msg(to, txt)

    

if __name__ == '__main__':
    h = "000000069133010000F019069133010000F011000A9133163254760000AA05F330BB4E07"
    if (len(sys.argv) > 21):
        h = sys.argv[1]
    
    m = Messenger()
    print(m.parse(h))
    

        
