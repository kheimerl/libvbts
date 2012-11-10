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
from libvbts import FreeSwitchMessenger
import logging

def usage():
    res = "VBTS_DB:\n" + "VBTS_DB item|value|field|qualifier[|table]\n" + "VBTS_DB name|bob|callerid|12345|sip_buddies"
    return res

def parse(args):
    res = args.split("|")
    if (len(res) < 4):
        return (None, None, None)
    table = "sip_buddies"
    if (len(res) > 4):
        table = res[4]
    return ((res[0], res[1]), (res[2], res[3]), table)

def set_cmd(args):
    (to_set, qualifier, table) = parse(args)
    consoleLog('info', "Got Args: " + str(args) + "\n")
    if not (to_set and qualifier and table):
        return None
    logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
    fs = FreeSwitchMessenger.FreeSwitchMessenger()
    if (table == "sip_buddies"):
        res = fs.SR_set(to_set, qualifier)
    elif (table == "dialdata_table"):
        res = fs.SR_dialdata_set(to_set, qualifier)
    else:
        consoleLog('info', "Bad Table")
        return None
    return str(res)

def chat(message, args):
    res = set_cmd(args)
    if (res):
        consoleLog('info', "Returned Chat: " + res + "\n")
        message.chat_execute('set', '_openbts_ret=%s' % res)
    else:
        consoleLog('info', usage())

def fsapi(session, stream, env, args):
    res = set_cmd(args)
    if (res):
        consoleLog('info', "Returned FSAPI: " + res + "\n")
        stream.write(res)
    else:
        stream.write(usage())

