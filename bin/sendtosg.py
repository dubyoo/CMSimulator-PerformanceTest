#!/usr/bin/env python
import sys
import random
import time
from senddte import *
from Logger import *
from LoadFromXml import *


def sendtosg(sgconf):
    sgconf.PrintDebug()
    STBSum = int(sgconf.CMPerSG) * int(sgconf.STBPerCM)
    interval = float(sgconf.RateOfCCP) / 1000
    index = 0                       # CCP index
    TunedInList = [''] * STBSum     # mark the tuned in Mcast IP of stb
    param = Param()
    param.UDP_IP   = sgconf.CVExIP
    param.UDP_PORT = sgconf.CVExPort
    param.SGID     = sgconf.SGID

    log_sgid = sgconf.SGID
    log_duration = 0
    log_ccp_join_count = 0
    log_ccp_leave_count = 0

    while True:
        STBIndex = random.randint(0, STBSum - 1)
        CMIndex = STBIndex / int(sgconf.STBPerCM)
        McastIp = sgconf.McastIpList[random.randint(0, len(sgconf.McastIpList) - 1)]
        CmMac = '%02x-%02x-%02x-%02x-%02x-%02x' % ((sgid>>8)&0xff, sgid&0xff, (CMIndex>>24)&0xff, (CMIndex>>16)&0xff, (CMIndex>>8)&0xff, CMIndex&0xff)
        StbIp = '192.168.1.%d' % (STBIndex%int(sgconf.STBPerCM) + 1)
        param.MAC      = CmMac
        param.STB_IP   = StbIp
        if TunedInList[STBIndex] != '' and TunedInList[STBIndex] != McastIp:
            param.GROUP_IP = TunedInList[STBIndex]
            param.LEAVE_OR_JOIN = 'leave'
            index += 1
            param.INDEX = index
            senddte(param)              # if current stb has tuned in another channel, tuned out it
        param.GROUP_IP = McastIp
        param.LEAVE_OR_JOIN = 'join'
        index += 1
        param.INDEX = index
        senddte(param)                  # current stb tune in selected channel
        TunedInList[STBIndex] = McastIp
        time.sleep(interval)


# sendtosg [SGID]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE :', sys.argv[0], '[SGID]'
        print 'SAMPLE:', sys.argv[0], '101'
        sys.exit()
    sgid = int(sys.argv[1])
    logger = INIT_LOGGER('../log/%d.log' % sgid)
    logconf = LoadLogConfig('../conf/LogConfig.xml')
    logger.SetConsoleLogLevel(logconf.LogToConsoleLevel)
    logger.SetFileLogLevel(logconf.LogToFileLevel)

    allSgConf = LoadSgConfig('../conf/SGConfig.xml')
    sgconf = allSgConf.GetSGConfig(sgid)
    if sgconf:
        sendtosg(sgconf)
    else:
        LOG_ERROR('Failed to find configuration of sgid(%s)' % sgid)

    sys.exit()

