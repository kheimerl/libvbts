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
import libvbts
from libvbts import FreeSwitchMessenger, Database
import logging
import time

def usage():
    res = "VBTS_DB_Get:\n" + "VBTS_DB_Get item|field|qualifier[|table]\n" + "VBTS_DB_Get name|callerid|12345|sip_buddies"
    return res

def parse_args(args):
    reload(libvbts)
    args = args.split('|')
    if (len(args) < 3):
        consoleLog('err', 'Missing Args\n')
        exit(1)
    imsi = args[0]
    ipaddr = args[1]
    port = args[2]
    if ((not imsi or imsi == '')
            or (not ipaddr or ipaddr == '')
            or (not port or port == '')):
        consoleLog('err', 'Malformed Args\n')
        exit(1)
    consoleLog('info', 'Args: ' + str(args) + '\n')
    logging.basicConfig(filename="/tmp/VBTS.log", level="DEBUG")
    return args

def get_location(updater, max_tries=5):
    query_time = time.time()
    do_update = updater
    for update_count in range(max_tries):
        result = do_update()
        if result != None:
            (lat,long,timestamp) = result
            # match a timestamp like: '2013-07-16 22:02:27'
            update_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        else:
            update_time = 0

        if (update_time >= query_time):
            return (lat,long)
        else:
            time.sleep(1)

def chat(message, args):
    dest_address = parse_args(args)
    imsi = dest_address[0]
    fs = FreeSwitchMessenger.FreeSwitchMessenger()
    def updater():
        fs.send_openbts_sms(message, dest_address, '101', '', True)
        return fs.SR_get_current_location(imsi, fields=("latitude", "longitude", "time"))

    (lat,long) = get_location(updater)
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

