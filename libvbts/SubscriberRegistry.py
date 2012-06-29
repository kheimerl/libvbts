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

import sqlite3
import logging

SR = {}

#singleton pattern
def getSubscriberRegistry(db_loc):
    global SR
    if (db_loc not in SR):
        SR[db_loc] = SubscriberRegistry(db_loc)
    return SR[db_loc]

class SubscriberRegistry:

    def __init__(self, db_loc):
        self.conn = sqlite3.connect(db_loc)
        self.log = logging.getLogger("libvbts.VBTSSubscriberRegistery.SubscriberRegistry")

    def __execute_cmd(self, cmd):
        cur = self.conn.cursor()
        cur.execute(cmd)
        res = cur.fetchone()[0]
        return res

    def get(self, to_get, qualifier):
        cmd = "SELECT %s FROM sip_buddies WHERE %s='%s'" % (to_get, qualifier[0], qualifier[1])
        return self. __execute_cmd(cmd)
