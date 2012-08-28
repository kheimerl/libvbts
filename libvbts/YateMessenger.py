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
            self.log.info(str(param) + " " + str(val))
        b64 = res["xsip_body"]
        #ugly padding that yate should be doing -kurtis
        b64 += "=" * ((4 - len(b64) % 4) % 4) 
        res.update(Messenger.Messenger.parse(self, base64.b64decode(b64)))
        return res

    def send_openbts_sms(self, msg, to, fromm, body):
        size = 150
        chunks = [body[pos:pos + size] for pos in xrange(0, len(body), size)]
        for c in chunks:
            msg.Yate("xsip.generate")
            msg.retval="true"
            msg.params = []
            msg.params.append(["method","MESSAGE"])
            user_ip = self.SR_get("ipaddr", ("name", to))
            user_port =self.SR_get("port", ("name", to))
            #defaults
            if not (user_ip):
                user_ip = "127.0.0.1"
            if not (user_port):
                user_port = "5062"
            msg.params.append(["uri", "sip:%s@%s:%s" % (to, user_ip, user_port)])
            msg.params.append(["sip_from", fromm])
            msg.params.append(["xsip_type", "text/plain"])
            msg.params.append(["xsip_body", c])
            msg.Dispatch()

    def send_smqueue_sms(self, msg, to, fromm, body):
        size = 150
        chunks = [body[pos:pos + size] for pos in xrange(0, len(body), size)]
        for c in chunks:
            msg.Yate("xsip.generate")
            msg.retval="true"
            msg.params = []
            msg.params.append(["method","MESSAGE"])
            #no defaults, if these fail we should explode
            smqloc = self.smqueue_get("SIP.myIP")
            smqport = self.smqueue_get("SIP.myPort")
            msg.params.append(["uri", "sip:smsc@%s:%s" % (smqloc, smqport)])
            msg.params.append(["sip_from", fromm])
            msg.params.append(["xsip_type", "application/vnd.3gpp.sms"])
            msg.params.append(["xsip_body_encoding", "base64"])
            msg.params.append(["xsip_body", base64.b64encode(self.generate(to, c))])
            msg.Dispatch()

    def originate(self, msg, to, fromm, dest, ipaddr=None, port=None):
        if (not ipaddr):
            ipaddr = self.SR_get("ipaddr", ("name", to))
        if (not port):
            port = self.SR_get("port", ("name", to))
        if not (ipaddr and port):
            self.log.info("Missing IP/Port for user %s" % (to,))
            return False
        msg.Yate("call.execute")
        msg.params = []
        msg.params.append(["callto", dest])
        msg.params.append(["vbts_from", fromm])
        msg.params.append(["caller", to])
        msg.params.append(["ip_host", str(ipaddr)])
        msg.params.append(["ip_port", str(port)])
        msg.params.append(["vbts_target", "sip/sip:" + to + "@" + str(ipaddr) + ":" + str(port)])
        msg.params.append(["id", str(msg.id)])
        msg.Dispatch()
        return True

    def get_param(self, item, params):
        for p in params:
            if (p[0] == item):
                return p[1]
        return None

    def add_param(self, key, value, params):
        for p in params:
            if (p[0] == key):
                params.remove(p)
                break
        params.append([key, value])    

if __name__ == '__main__':
    incoming = [['ip_transport', 'UDP'], ['newcall', 'false'], ['domain', '127.0.0.1'], ['device', 'OpenBTS P2.8TRUNK Build Date Jun 17 2012'], ['connection_id', 'general'], ['connection_reliable', 'false'], ['called', 'smsc'], ['caller', 'IMSI460010018073482'], ['callername', 'IMSI460010018073482 '], ['antiloop', '4'], ['address', '127.0.0.1:5062'], ['ip_host', '127.0.0.1'], ['ip_port', '5062'], ['ip_transport', 'UDP'], ['sip_uri', 'sip:smsc@127.0.0.1'], ['sip_callid', '478788539@127.0.0.1'], ['xsip_dlgtag', '387511113'], ['sip_from', 'IMSI460010018073482 <sip:IMSI460010018073482@127.0.0.1>;tag'], ['sip_to', 'smsc <sip:smsc@127.0.0.1>'], ['sip_content-type', 'application/vnd.3gpp.sms'], ['sip_user-agent', 'OpenBTS P2.8TRUNK Build Date Jun 17 2012'], ['xsip_type', 'application/vnd.3gpp.sms'], ['xsip_body_encoding', 'base64'], ['xsip_body', 'MDA1NDAwMDg5MTY4MzExMDkwMTEwNWYwMGUxMTU0MDM4MTU1ZjUwMDAwZmYwNGQ0ZjI5YzBl']]
    ym = YateMessenger()
    res = ym.parse(incoming)
    print (res)

