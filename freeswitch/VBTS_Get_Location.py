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

from freeswitch import *
from libvbts import FreeSwitchMessenger, Database
import logging

def usage():
    res = "VBTS_DB_Get:\n" + "VBTS_DB_Get item|field|qualifier[|table]\n" + "VBTS_DB_Get name|callerid|12345|sip_buddies"
    return res

def get(imsi):
    consoleLog('info', "Got imsi: " + str(imsi) + "\n")
    if not (imsi):
        return None
    logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
    fs = FreeSwitchMessenger.FreeSwitchMessenger()
    res = fs.SR_get_current_location(imsi)
    return res

def chat(message, args):
    (lat,long) = get(args)
    if (lat and long):
        consoleLog('info', "Returned Chat: " + str((lat,long)) + "\n")
        message.chat_execute('set', 'ms_latitude=%s' % str(lat))
        message.chat_execute('set', 'ms_longitude=%s' % str(long))
    else:
        consoleLog('info', usage())

def fsapi(session, stream, env, args):
    res = get(args)
    if (res):
        consoleLog('info', "Returned FSAPI: " + res + "\n")
        stream.write(res)
    else:
        stream.write(usage())

