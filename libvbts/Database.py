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
import os
import syslog

REQ_VERSION = (3,7,0)

NULLVALUE = "~~~"

sqlite_version=None
sqlite_version_info=None

using_sqlite3=True

class OperationalError(sqlite3.OperationalError):
    pass

def version_check(sqlite_version_info):
    return ((sqlite_version_info[0] > REQ_VERSION[0]) or
            ((sqlite_version_info[0] == REQ_VERSION[0]) and (sqlite_version_info[1] >= REQ_VERSION[1])))

if (version_check(sqlite3.sqlite_version_info)):
    sqlite_version = sqlite3.sqlite_version
    sqlite_version_info = sqlite3.sqlite_version_info
    using_sqlite3=True
else:
    res = os.popen('sqlite3 --version').read().split(" ")[0].strip()
    sqlite_version=res
    res = res.split(".")
    sqlite_version_info=(int(res[0]),int(res[1]),int(res[2]))
    #if the CLI is better, use that
    if (version_check(sqlite_version_info)):
            using_sqlite3=False
    else:
            using_sqlite3=True

class FakeCursor:

    def __init__(self, db_loc):
        self.db_loc = db_loc

    def execute(self, cmd, args=[]):
        for arg in args:
            cmd = cmd.replace('?', '\''+arg+'\'', 1)
        sql_cmd = 'sqlite3 -nullvalue %s %s "%s"' % (NULLVALUE, self.db_loc, cmd)
        syslog.syslog("Kurtis:" + sql_cmd)
        ans = os.popen(sql_cmd).read().strip()
        self.res = []
        self.index = 0
        if (ans == ""):
            return self
        ans = ans.split("\n")
        for r in ans:
            r = r.strip()
            r = r.split("|")
            cleaned = []
            #eventually figure out if they are numbers or not here
            for a in r:
                if (a == NULLVALUE):
                    cleaned.append(None)
                else:
                    cleaned.append(unicode(a))
            self.res.append(tuple(cleaned))
        return self
    
    def fetchone(self):
        if (self.index < len(self.res)):
            self.index += 1
            return self.res[self.index - 1]
        else:
            return None

    def fetchall(self):
        if (self.index >= len(self.res)):
            return []
        old_index = self.index
        self.index = len(self.res)
        return self.res[old_index:]
        
class FakeDB:

    def __init__(self, db_loc):
        self.db_loc = db_loc

    def cursor(self):
        return FakeCursor(self.db_loc)

    def commit(self):
        pass

def connect(db_loc):
    if (using_sqlite3):
        return sqlite3.connect(db_loc) 
    else:
        return FakeDB(db_loc)

