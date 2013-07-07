#Copyright 2012 Kurtis Heimerl <kheimerl@cs.berkeley.edu>. All rights reserved.
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
from libvbts import FreeSwitchMessenger

def chat(message, args):
    reload(libvbts)
    args = args.split('|')
    if (len(args) < 3):
        consoleLog('err', 'Missing Args\n')
        exit(1)
    to = args[0]
    ipaddr = args[1]
    port = args[2]
    if ((not to or to == '')
            or (not ipaddr or ipaddr == '')
            or (not port or port == '')):
        consoleLog('err', 'Malformed Args\n')
        exit(1)
    consoleLog('info', 'Args: ' + str(args) + '\n')
    fs = FreeSwitchMessenger.FreeSwitchMessenger()
    fs.send_openbts_sms(message, (to, ipaddr, port), '101', '', True)

def fsapi(session, stream, env, args):
    #chat doesn't use message anyhow
    chat(None, args)
