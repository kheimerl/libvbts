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
import Messenger
import base64

#handles yate specific messaging
class YateMessenger(Messenger.Messenger):
    
    def __init__(self):
        Messenger.Messenger.__init__(self)
        self.log = logging.getLogger("libvbts.VBTSYateMessenger.YateMessenger")

    def parse(self, msg):
        #first, get it in a real format
        res = {}
        for (param, val) in msg:
            res[param] = val
        res.update(Messenger.Messenger.parse(self, base64.b64decode(res["xsip_body"])))
        return res
    
if __name__ == '__main__':
    incoming = [['ip_transport', 'UDP'], ['newcall', 'false'], ['domain', '127.0.0.1'], ['device', 'OpenBTS P2.8TRUNK Build Date Jun 17 2012'], ['connection_id', 'general'], ['connection_reliable', 'false'], ['called', 'smsc'], ['caller', 'IMSI460010018073482'], ['callername', 'IMSI460010018073482 '], ['antiloop', '4'], ['address', '127.0.0.1:5062'], ['ip_host', '127.0.0.1'], ['ip_port', '5062'], ['ip_transport', 'UDP'], ['sip_uri', 'sip:smsc@127.0.0.1'], ['sip_callid', '478788539@127.0.0.1'], ['xsip_dlgtag', '387511113'], ['sip_from', 'IMSI460010018073482 <sip:IMSI460010018073482@127.0.0.1>;tag'], ['sip_to', 'smsc <sip:smsc@127.0.0.1>'], ['sip_content-type', 'application/vnd.3gpp.sms'], ['sip_user-agent', 'OpenBTS P2.8TRUNK Build Date Jun 17 2012'], ['xsip_type', 'application/vnd.3gpp.sms'], ['xsip_body_encoding', 'base64'], ['xsip_body', 'MDA1NDAwMDg5MTY4MzExMDkwMTEwNWYwMGUxMTU0MDM4MTU1ZjUwMDAwZmYwNGQ0ZjI5YzBl']]
    ym = YateMessenger()
    print (ym.parse(incoming))
