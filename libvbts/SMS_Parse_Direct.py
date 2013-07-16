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
import string
from smspdu import SMS_DELIVER
from rpdu import RPDU

#util functions
def clean(s):
    if (isinstance(s,str)):
        return filter(lambda x: x in string.printable, s).strip()
    else:
        return s


def parse(rp_message):
    # rp stays pretty much the same
    rpdu = RPDU.fromPDU(rp_message)
    sms_deliver = SMS_DELIVER.fromPDU(rpdu.user_data, rpdu.rp_destination_address)
    export_names = ("vbts_text"
    , "vbts_tp_user_data"
    , "vbts_tp_data_coding_scheme"
    , "vbts_tp_protocol_id"
    , "vbts_tp_orig_address"
    , "vbts_tp_orig_address_type"
    , "vbts_tp_message_type"
    , "vbts_rp_dest_address"
    , "vbts_rp_originator_address"
    , "vbts_rp_originator_address_type"
    , "vbts_rp_message_reference"
    , "vbts_rp_message_type")

    export_values = (sms_deliver.user_data
    , sms_deliver.tp_ud
    , sms_deliver.tp_dcs
    , sms_deliver.tp_pid
    , sms_deliver.tp_oa
    , sms_deliver.tp_toa
    , sms_deliver.tp_mti
    , rpdu.rp_destination_address
    , rpdu.rp_originator_address
    , rpdu.rp_originator_address_type
    , rpdu.rp_message_reference
    , rpdu.rp_mti)
    export_values = map(lambda x: clean(x), export_values)
    return zip(export_names, export_values)

if __name__ == '__main__':
    h = "013A038100000022000491000100003170502160650015F9771D340FA7C93A10F3FD5EE741ECF77B9D07"
    if (len(sys.argv) > 1):
        h = sys.argv[1]

    for i in range(0,999):
        parse(h)

