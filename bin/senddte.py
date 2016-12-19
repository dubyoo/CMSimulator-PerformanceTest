#!/usr/bin/env python

import sys
from socket import *
from Logger import *

class Param:
    def __init__(self):
        self.UDP_IP = ""
        self.UDP_PORT = ""
        self.SGID = ""
        self.MAC = ""
        self.STB_IP = ""
        self.GROUP_IP = ""
        self.LEAVE_OR_JOIN = ""
        self.INDEX = 0
    def print_debug(self):
        mcastStr = "Mcast(%s)" % self.GROUP_IP
        indexStr = ""
        if self.INDEX:
            indexStr = "Index(%d)" % self.INDEX
        LOG_INFO("%-5s %-18s in SGID(%s) from CM(%s) STB(%s) %s" % (self.LEAVE_OR_JOIN, mcastStr, self.SGID, self.MAC, self.STB_IP, indexStr))

#def print_debug(message, param):
#    debugmessage = "send to %s(%s):\n" % (param.UDP_IP, param.UDP_PORT)
#    for c in message:
#        if '\r' == c:
#            debugmessage += '\\r'
#        elif '\n' == c:
#            debugmessage += '\\n'
#        else:
#            debugmessage += c


def senddte(param):
    leaveorjoin = ""
    if param.LEAVE_OR_JOIN == "join":
        leaveorjoin = "0"
    elif param.LEAVE_OR_JOIN == "leave":
        leaveorjoin = "1"
    else:
        LOG_ERROR("unknown param in [leave_or_join]: %s", param.LEAVE_OR_JOIN)
        sys.exit()

    payload = "message_payload: session_id=" + leaveorjoin + "; client_destination=" + param.STB_IP + "; client_cablemodem_mac_address=" + param.MAC + "; " + "source_ip=" + param.GROUP_IP + ";retry_count=2;rc_index=1;rc_chan_freq=480000000; client_cpe_destination=10.90.242.82;" + "cm_vednor=name;cm_type=1;sgid=" + param.SGID + ";\r\n"
    content_length = len(payload)
    head = "SETUP rtsp://hlit.net RTSP/1.0\r\nCSeq: 313\r\nRequire: com.harmonic.d2e.ccp\r\nHeader: protocolDescriminator=17;dsmcc_type=4;message_id=1;transaction_id=393;\r\nContent-Length: " + str(content_length) + "\r\n\r\n"
    message = head + payload
    
    param.print_debug()
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.sendto(message, (param.UDP_IP, int(param.UDP_PORT)))
    sock.close()


# senddte [IP] [Port] [SGID] [mac] [stb_ip] [group_ip] [leave_or_join]
if __name__ == '__main__':
    if len(sys.argv) < 8:
        print "USAGE :", sys.argv[0], "[IP] [Port] [SGID] [MAC] [stb_ip] [group_ip] [leave_or_join]"
        print "SAMPLE:", sys.argv[0], "10.90.242.246 20000 801 00-1C-26-C8-5C-50 192.168.1.1 238.1.1.1 join"
        sys.exit()

    param = Param()
    param.UDP_IP   = sys.argv[1]
    param.UDP_PORT = sys.argv[2]
    param.SGID     = sys.argv[3]
    param.MAC      = sys.argv[4]
    param.STB_IP = sys.argv[5]
    param.GROUP_IP = sys.argv[6]
    param.LEAVE_OR_JOIN = sys.argv[7]
    senddte(param)

    sys.exit()
