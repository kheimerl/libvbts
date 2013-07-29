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

from smspdu import *
import string
import sys

#converts an integer to hex form (with 2 digits)
def to_hex2(i):
    tmp = hex(i)[2:]
    if (len(tmp) == 1):
        return "0" + tmp
    else:
        return tmp

def encode_num(num):
    #jumble the number. i.e. 123 --> "321f"
    snuml = list(str(num))
    if len(snuml)%2 == 1:
        snuml += 'f'
    for i in range(len(snuml)):
        if (i%2 == 0):
            snuml[i],snuml[i+1] = snuml[i+1],snuml[i]

    enc_num = (
        to_hex2(len(snuml)/2 + 1)  #length of number
        + "81"                  # ext=1 for some fucking reason, use unknown numbering type, unknown numbering plan
        + ''.join(snuml))

    return enc_num

def clean(s):
    if (isinstance(s,basestring)):
        return filter(lambda x: x in string.printable, s).strip()
    elif (isinstance(s,int)):
        return "%X" % s
    else:
        return s

def smspdu_charstring_to_hex(string):
    return ''.join(["%02X" % ord(c) for c in string])

if __name__ == '__main__':
    #jumble the number. i.e. 123 --> "321f"
    to = "1234567"
    if (len(sys.argv) > 1):
        to = sys.argv[1]
    print encode_bcd_called_party_num(to)
