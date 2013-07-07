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
import messaging.utils

#util functions
def strip_fs(s):
    if (len(s) == 0):
        return s
    if (s[-1] in ['f', 'F']):
        return s[:-1]
    else:
        return s

def clean(s):
    if (s):
        return filter(lambda x: x in string.printable, s).strip()
    else:
        return s

#byte order is backwards...
def octet_to_number(o):
    i = 0
    res = ''
    while (i < len(o)):
        res += o[i+1]
        res += o[i]
        i += 2
    return res

def n_bytes(h,n):
    (hex_str, index) = h
    return (hex_str[index:index+n], (hex_str, index+n))

#parsing functions
def __get_rp_message_type(h):
    return n_bytes(h,2)

def __get_rp_message_reference(h):
    return n_bytes(h,2)

def __get_rp_originator_address(h):
    return n_bytes(h,2)

def __get_rp_destination_address(h):
    (num_octets,h) = n_bytes(h,2)
    num_octets = int(num_octets,16)
    (rp_dest_address_type,h) = n_bytes(h,2)
    (rp_dest_address,h) = n_bytes(h,(num_octets-1)*2) #minus for address type, *2 as octets
    return (rp_dest_address_type, strip_fs(octet_to_number(rp_dest_address)), h)


def __get_rp_user_data(h):
    (num_octets,h) = n_bytes(h,2)
    num_octets = int(num_octets,16)*2
    if ((len(h[0]) - h[1]) != num_octets):
        raise Exception("MALFORMED MESSAGE: Bad RP-User-Data length")
    return h

def __get_tp_message_type(h):
    return n_bytes(h,2)

def __get_tp_message_reference(h):
    return n_bytes(h,2)

def __get_tp_destination_address(h):
    (num_bytes,h) = n_bytes(h,2) #not octets!
    num_bytes = int(num_bytes,16)
    if (num_bytes % 2 == 1):
        num_bytes += 1 #has to be even number, they will have inserted extraneous Fs
    (tp_destination_address_type, h) = n_bytes(h,2)
    (tp_destination_address,h) = n_bytes(h,num_bytes)
    return (tp_destination_address_type, strip_fs(octet_to_number(tp_destination_address)), h)

def __get_tp_protocol_identifier(h):
    return n_bytes(h,2)

def __get_tp_data_coding_scheme(h):
    return n_bytes(h,2)

def __get_tp_validity_period(h):
    return n_bytes(h,2)

#hax for now, just read rest of msg
def __get_tp_user_data(h):
    (num_septets,h) =  n_bytes(h,2)
    #num_bits = int(num_septets,16) * 7
    #sys.stderr.write(str(num_bits))
    #return (n_bytes(h,(num_bits+3)/4)) #rounding up
    return (n_bytes(h, len(h[0]) - h[1]))

def parse(rp_message):
    rp_message = (rp_message,0)
    (rp_message_type, rp_message) = __get_rp_message_type(rp_message)
    (rp_message_reference, rp_message) = __get_rp_message_reference(rp_message)
    (rp_originator_address, rp_message) = __get_rp_originator_address(rp_message)
    (rp_dest_address_type, rp_dest_address, rp_message) = __get_rp_destination_address(rp_message)
    rp_user_data = __get_rp_user_data(rp_message)

    #rp_message finished
    (tp_message_type, rp_user_data) = __get_tp_message_type(rp_user_data)
    (tp_message_reference, rp_user_data) = __get_tp_message_reference(rp_user_data)
    (tp_dest_address_type, tp_dest_address, rp_user_data) = __get_tp_destination_address(rp_user_data)
    (tp_protocol_id, rp_user_data) = __get_tp_protocol_identifier(rp_user_data)
    (tp_data_coding_scheme, rp_user_data) = __get_tp_data_coding_scheme(rp_user_data)
    #check to see if validity period field is there
    if (int(tp_message_type, 16) & 0x10 == 0):
        tp_validity_period = None
    else:
        (tp_validity_period, rp_user_data) = __get_tp_validity_period(rp_user_data)
    (tp_user_data, rp_user_data) = __get_tp_user_data(rp_user_data)

    return {"vbts_rp_message_type" : clean(rp_message_type),
            "vbts_rp_message_reference" : clean(rp_message_reference),
            "vbts_rp_originator_address" : clean(rp_originator_address),
            "vbts_rp_dest_address_type" : clean(rp_dest_address_type),
            "vbts_rp_dest_address" : clean(rp_dest_address),
            "vbts_tp_message_type" : clean(tp_message_type),
            "vbts_tp_message_reference" : clean(tp_message_reference),
            "vbts_tp_dest_address_type" : clean(tp_dest_address_type),
            "vbts_tp_dest_address" : clean(tp_dest_address),
            "vbts_tp_protocol_id" : clean(tp_protocol_id),
            "vbts_tp_data_coding_scheme" : clean(tp_data_coding_scheme),
            "vbts_tp_validity_period" : clean(tp_validity_period),
            "vbts_tp_user_data" : clean(tp_user_data),
            "vbts_text" : clean(messaging.utils.unpack_msg(tp_user_data).encode('UTF8'))
            }

if __name__ == '__main__':
    h = "000000069133010000F019069133010000F011000A9133163254760000AA05F330BB4E07"
    if (len(sys.argv) > 1):
        h = sys.argv[1]

    print(parse(h))
