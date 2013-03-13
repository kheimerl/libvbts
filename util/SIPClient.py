from twisted.internet import reactor
from twisted.protocols import sip
import random
import logging
import string
import sqlite3
import traceback
import time

class Client(sip.Base):
    
    def __init__(self, sub_reg, sender_ip, sender_port):
        sip.Base.__init__(self)
        self.log = logging.getLogger('BM.SIPClient.Client')
        self.ast_db = sqlite3.connect(sub_reg)
        self.ip = sender_ip
        self.port = int(sender_port)
        self.log.info('Starting...')
        self.started = False
        self.cseq = 1

    def __start(self):
        self.started = True
        reactor.listenUDP(self.port, self)

    def __gen_string(self, length):
        return ''.join(random.choice(string.letters) for i in xrange(length))

    def __get_ip(self, target):
        cur = self.ast_db.cursor()
        cur.execute('SELECT ipaddr FROM SIP_BUDDIES where name=?', (target,))
        line = cur.fetchone()
        res = None
        if (line):
            res = line[0]
        cur.close()
        return res

    def __get_port(self, target):
        cur = self.ast_db.cursor()
        cur.execute('SELECT port FROM SIP_BUDDIES where name=?', (target,))
        line = cur.fetchone()
        res = None
        if (line):
            res = line[0]
        cur.close()
        return res

    #sends a SIMPLE message to smqueue
    def send_message(self, target, body, return_num):
        if (not self.started):
            self.__start()
        if (not return_num):
            return_num = "000"
        target_ip = self.__get_ip(target)
        target_port = self.__get_port(target)
        if (target_ip and target_port):
            r = sip.Request('MESSAGE', sip.URL(target_ip, 
                                               port=target_port, 
                                               username=target))
            r.body = body
            r.addHeader('via', sip.Via(self.ip).toString())
            r.addHeader('from', "%s <sip:%s@%s:%s>;tag=%s" % (return_num, return_num,
                                                           self.ip, self.port, self.__gen_string(6)))
            r.addHeader('to', "%s <sip:%s@%s>" % (target, target, 
                                                  target_ip))
            r.addHeader('call-id', (random.randint(100000, 10000000)))
            r.addHeader('cseq', "18 MESSAGE")
            r.addHeader('content-type', "text/plain")
            r.addHeader('content-length', len(r.body))
            self.sendMessage(sip.URL(target_ip,
                                     port=target_port), r)
            self.log.info("Sent SIP message to %s: %s" % (target, body))
        else:
            self.log.warn("Unable to send message to %s: %s" % (target, body))

    def broadcast_message(self, body, return_num):
        cur = self.ast_db.cursor()
        cur.execute('SELECT name FROM SIP_BUDDIES')
        self.log.info("Broadcasting %s" % body)
        for name in cur:
            try:
                self.send_message(name[0], body, return_num)
                time.sleep(2)
            except:
                self.log.warn("Unable to broadcast to %s" % name[0])
                self.log.warn("%s" % traceback.format_exc())
                pass
