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

import random
import SMS_Helper
from smspdu import SMS_DELIVER

import sys

def gen_tpdu(ref, to, fromm, text, empty):
    # see: 3GPP TS 23.040 version 11.5.0 Release 11
    TPPID = 0x40 if empty else 0 #TP-PID = 40 ==> short message type 0
    TPDCS = 0xc3 if empty else 0 #TP-DCS = c3 ==> disable "other message indicator" and discard message

    if empty:
        text = ""

    return [SMS_DELIVER.create(fromm, to, text, tp_pid=TPPID, tp_dcs=TPDCS).toPDU()]

def gen_rp_header(ref, empty):
    # If 'empty' is true, generates for Empty SMS
    # GSM 4.11: 8.21, 8.22
    rp_header = ["01"           #Message Type = n -> ms
            , ref               #Message Reference
            , SMS_Helper.encode_num("0000")
            , "00"]  #RP-destination address for Service Center
    return rp_header

def gen_msg(to, fromm, text, empty=False):
    # note we are constructing a RPDU which encapsulates a TPDU
    ref = str(SMS_Helper.to_hex2(random.randint(0,255)))
    rp_header = gen_rp_header(ref, empty)
    tpdu = gen_tpdu(ref, to, fromm, text, empty)
    tp_len = len("".join(tpdu)) / 2 #in octets

    body = rp_header + [SMS_Helper.to_hex2(tp_len)] + tpdu
    return "".join(body)

if __name__ == '__main__':
    to = "9091"
    fromm = "101"
    msg = "Test Message"
    if (len(sys.argv) > 2):
        to = sys.argv[1]
        msg = sys.argv[2]
    print (gen_msg(to, fromm, msg))
