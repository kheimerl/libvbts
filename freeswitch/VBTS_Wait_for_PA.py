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
import sys
import random
import os
import time
from datetime import datetime, timedelta

MIN_WAIT = 30
PING_TIME = 5

def runtime(arg1):
    (fromm, ip, port, to) = arg1.split("|")
    time.sleep(MIN_WAIT) #this is just to test that we are actually
                       # running in a separate thread.  
    consoleLog("info", "%s@%s:%s called %s %d second ago\n" % (fromm, ip, port, to, MIN_WAIT))
    new_api_obj = API()
    new_api_obj.executeString("originate {origination_caller_id_number=%s}sofia/openbts/%s@%s:%s %s" % (to, fromm, ip, port, to))

def chat(message, args):
    args = args.split('|')

def handler(session, args):
    args =  args.split('|')
    session.answer()
    #session.execute("playback", "tone_stream://path=${base_dir}/conf/tetris.ttml;loops=1")
    session.hangup()
    os.system('VBTS_PA_On.py')
    #runs the "runtime" function above in another thread
    new_api_obj = API()
    #this will need to be changed when we use a real DID
    new_api_obj.executeString("pyrun VBTS_Wait_for_PA %s|%s|%s|%s\n" % 
                              (session.getVariable('caller_id_name'), 
                               session.getVariable('sip_received_ip'),
                               session.getVariable('sip_received_port'),
                               session.getVariable('destination_number')))

#not used
#def fsapi(session, stream, env, args):
#    pass
