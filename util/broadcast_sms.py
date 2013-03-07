#!/usr/bin/python

import SIPClient
import getopt
import sys
import logging
from twisted.internet import reactor

def usage():
    print ("Stuff goes here")
    print ("-r return | --return=RETURN NUMBER, must be a number. Defaults to config")
    print ("-m message | --message=MESSAGE WE WANT TO SEND")
    print ("-l log_level | --log_level=LOG LEVEL")
    print ("-d subscriber_reg | --subscriber_reg=SUBSCRIBER_REG LOCATION")
    exit(1)

opts, args = getopt.getopt(sys.argv[1:],
                           "m:r:l:d:", ["message=", "return=", "log_level=", "subscriber_reg="])
log_level = "DEBUG"
log_loc = "/tmp/libvbts_util.log"
sub_reg = "/var/lib/asterisk/sqlite3/sqlite3.db"
message=None
ret = None

for o,a in opts:
    if o in ("-l", "--log_level="):
        log_level = a
    elif o in ("-d", "--subscriber_reg="):
        sub_reg = a
    elif o in ("-m", "--message="):
        message = a
    elif o in ("-r", "--return="):
        ret = int(a)
    else:
        usage()

if not (message):
    usage()

if (log_level == "DEBUG"):
    log_level = logging.DEBUG
elif(log_level == "INFO"):
    log_level = logging.INFO
elif(log_level == "WARNING"):
    log_level = logging.WARNING
elif(log_level == "ERROR"):
    log_level = logging.ERROR
elif(log_level == "CRITICAL"):
    log_level = logging.CRITICAL
else:
    print ("Invalid logging level")
    usage()

logging.basicConfig(filename=log_loc, level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger("send_sms")

client = SIPClient.Client(sub_reg, "127.0.0.1", "5065")

reactor.callWhenRunning(client.broadcast_message,message,ret)
reactor.callWhenRunning(reactor.stop)
# Run the server's main loop
reactor.run()
