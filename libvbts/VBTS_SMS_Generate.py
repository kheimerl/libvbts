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

import sys
import re
import random
import messaging.sms.submit
from datetime import datetime, timedelta

#RP-Message Type = 00
#RP-Message Reference = GG -fill out later
#RP-Originator Address = 00
#RP-Destination Address = 9999
RP_GENERIC_HEADER = '00GG0003919999'
#TP-Message Type = 11 - SMS_SUBMIT
#TP-Message Reference = GG - fill out later
TP_GENERIC_HEADER = '11GG'

#MAX GSM time is 63 weeks
MAX_GSM_TIME = 63 * 7

def __gen_header(reference, header):
    return re.sub('GG', reference, header)

#gotta preserve 0s...
def __gen_hex(i):
    tmp = hex(i)[2:]
    if (len(tmp) == 1):
        return "0" + tmp
    else:
        return tmp

def __gen_tpdu(to, text):
    tmp = (messaging.sms.submit.SmsSubmit(str(to), text))
    tmp._validity = timedelta(MAX_GSM_TIME)
    #stripping the nonsense headers, will probably fix later
    return tmp.to_pdu()[0].pdu[6:].lower() 

def gen_msg(to, text):
    reference = str(hex(random.randint(17,255))[2:]) #random reference?
    rp_header = __gen_header(reference, RP_GENERIC_HEADER)
    tp_header = __gen_header(reference, TP_GENERIC_HEADER)
    tp_user_data = __gen_tpdu(to, text)
    tp_len = (len(tp_header) + len(tp_user_data))/2 #octets, not bytes
    return rp_header + gen_hex(tp_len) + tp_header + tp_user_data

if __name__ == '__main__':
    to = "101"
    msg = "Test Message"
    if (len(sys.argv) > 2):
        to = sys.argv[1]
        msg = sys.argv[2]
    
    print (gen_msg(to, msg))
