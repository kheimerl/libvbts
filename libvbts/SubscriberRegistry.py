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

    def __execute_cmd(self, cmd, args):
        cur = self.conn.cursor()
        cur.execute(cmd, args)
        res = cur.fetchone()[0]
        conn.commit()
        return res

    def get(self, to_get, qualifier):
        to_get = to_get.strip()
        qualifier = (qualifier[0].strip(), qualifier[1].strip())
        cmd = "SELECT %s FROM sip_buddies WHERE %s='?'" % (to_get, qualifier[0])
        args = (qualifier[1],)
        self.log.info(cmd + " " + str(args))
        return self. __execute_cmd(cmd, args)
    
    def provision(self, name, number, ip, port):
        insert1_cmd = "INSERT INTO sip_buddies (name, username, type, context, host, callerid, canreinvite, allow, dtmfmode, ipaddr, port) values (?,?,?,?,?,?,?,?,?,?,?)"
        insert1_args = (name, name, "friend", "phones", "dynamic", number, "no", "gsm", "info", ip, port)
        insert2_cmd = "INSERT INTO dialdata_table (exten, dial) values (?, ?)"
        insert2_args = (number, name)
        cur = self.conn.cursor()
        if (cur.execute("SELECT * FROM sip_buddies WHERE name=?", (name,)).fetchone()):
            return False
        if (cur.execute("SELECT * FROM sip_buddies WHERE callerid=?", (number,)).fetchone()):
            return False
        cur.execute(insert1_cmd, insert1_args)
        cur.execute(insert2_cmd, insert2_args)
        self.conn.commit()
        return True

    def unprovision(self, name):
        rm1_cmd = "DELETE FROM sip_buddies WHERE name=?"
        rm2_cmd = "DELETE from dialdata_table WHERE dial=?"
        cur = self.conn.cursor()
        cur.execute(rm1_cmd, (name,))
        cur.execute(rm2_cmd, (name,))
        self.conn.commit()
        return True
