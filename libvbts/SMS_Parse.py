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
from smspdu import SMS_SUBMIT
from SMS_Helper import clean,smspdu_charstring_to_hex
from rpdu import RPDU

def parse(rp_message):
    rpdu = RPDU.fromPDU(rp_message)
    sms_submit = SMS_SUBMIT.fromPDU(rpdu.user_data, rpdu.rp_originator_address)
    exports = [("vbts_text" , sms_submit.user_data)
            , ("vbts_tp_user_data" , smspdu_charstring_to_hex(sms_submit.tp_ud))
            , ("vbts_tp_data_coding_scheme" ,  sms_submit.tp_dcs)
            , ("vbts_tp_protocol_id" ,  sms_submit.tp_pid)
            , ("vbts_tp_dest_address" ,  sms_submit.tp_da)
            , ("vbts_tp_dest_address_type" ,  sms_submit.tp_toa)
            , ("vbts_tp_message_type" ,  sms_submit.tp_mti)
            , ("vbts_rp_dest_address" ,  rpdu.rp_destination_address)
            , ("vbts_rp_originator_address" ,  rpdu.rp_originator_address)
            , ("vbts_rp_originator_address_type" ,  rpdu.rp_originator_address_type)
            , ("vbts_rp_message_reference" ,  rpdu.rp_message_reference)
            , ("vbts_rp_message_type" ,  rpdu.rp_mti)]
    exports = [(x, clean(y)) for (x, y) in exports]
    return exports

if __name__ == '__main__':
    h = "001000038100000e05df04810011000005cbb7fb0c02"
    if (len(sys.argv) > 1):
        h = sys.argv[1]

    print(parse(h))
