#!/usr/bin/env python

import sys
import os
import re
import sets
import xml.dom.minidom
from Logger import *

class SGConfiguration:
    def __init__(self):
        self.SGID = ''
        self.CMPerSG = ''
        self.STBPerCM = ''
        self.RateOfCCP = ''
        self.McastIpList = []
        self.CVExIP = ''
        self.CVExPort = ''
    def PrintDebug(self):
        LOG_DEBUG('<--- SG(%s) Configuration Begin --->' % self.SGID)
        LOG_DEBUG('CVExIP(%s), CVExPort(%s), ' % (self.CVExIP, self.CVExPort))
        LOG_DEBUG('CMPerSG(%s), STBPerCM(%s), RateOfCCP(%s), ' % (self.CMPerSG, self.STBPerCM, self.RateOfCCP))
        LOG_DEBUG('McastIpList(%s)' % self.McastIpList)
        LOG_DEBUG('<--- SG(%s) Configuration End --->' % self.SGID)

class LogLevelConfiguration:
    def __init__(self):
        self.LogToConsoleLevel = ''
        self.LogToFileLevel = ''
    def PrintDebug(self):
        LOG_DEBUG('Log to console level: %s, log to file level: %s' % (self.LogToConsoleLevel, self.LogToFileLevel))

class AllSGConfiguration:
    def __init__(self):
        self.SgConfDict = {}

    def Insert(self, sgconfig):
        self.SgConfDict[int(sgconfig.SGID)] = sgconfig

    def GetSGConfig(self, sgid):
        SgConf = None
        if self.SgConfDict.has_key(int(sgid)):
            SgConf = self.SgConfDict[int(sgid)]
        return SgConf


def GetValueByName(parentnode, name):
    value = ''
    itemlist = parentnode.getElementsByTagName(name)
    if itemlist == []:
        LOG_ERROR('Faild to get element(%s)' % name)
    else:
        value = itemlist[0].firstChild.data.strip()
    return value

def GetAttrByName(parentnode, nodename, attrname, index = 0):
    return parentnode.getElementsByTagName(nodename)[index].getAttribute(attrname).strip()

def GetMcastIpList(parentnode):
    itemlist = parentnode.getElementsByTagName('McastIP')
    IpList = []
    for item in itemlist:
        ip_from = item.getAttribute('From').strip()
        ip_to = item.getAttribute('To').strip()
        
        matchFrom = re.search(r'(\d+\.\d+\.\d+\.)(\d+)', ip_from)
        IpPrefixFrom = matchFrom.group(1)
        IpSuffixFrom = int(matchFrom.group(2))
        matchTo = re.search(r'(\d+\.\d+\.\d+\.)(\d+)', ip_to)
        IpPrefixTo = matchTo.group(1)
        IpSuffixTo = int(matchTo.group(2))
        
        if IpPrefixFrom != IpPrefixTo or IpSuffixFrom > IpSuffixTo:
            LOG_ERROR('Faild to generate McastIP From(%s) To(%s)' % (ip_from, ip_to))
            continue
        
        for i in range(IpSuffixFrom, IpSuffixTo + 1):
            ip = '%s%d' % (IpPrefixFrom, i)
            if IpList.count(ip) is 0:
                IpList.append(str(ip))
    return IpList

def LoadLogConfig(filename):
    if not os.path.exists(filename):
        LOG_ERROR('xml file("%s") not exists' % filename)
        sys.exit()
    #LOG_DEBUG('Load log config from file("%s")' % filename)
    parser = xml.dom.minidom.parse(filename)
    root = parser.documentElement
    LogConf = LogLevelConfiguration()
    LogConf.LogToConsoleLevel = GetValueByName(root, 'LogToConsole')
    LogConf.LogToFileLevel = GetValueByName(root, 'LogToFile')
    return LogConf

def LoadSgConfig(filename):
    AllSgConf = AllSGConfiguration()
    if not os.path.exists(filename):
        LOG_ERROR('xml file("%s") not exists' % filename)
        sys.exit()
    LOG_DEBUG('Load SG config from file("%s")' % filename)
    parser = xml.dom.minidom.parse(filename)
    root = parser.documentElement
    
    nodes = root.getElementsByTagName('SG')
    for node in nodes:
        SgConf = SGConfiguration()
        SgConf.SGID = node.getAttribute('SGID')
        SgConf.CMPerSG = GetValueByName(node, 'CMPerSG')
        SgConf.STBPerCM = GetValueByName(node, 'STBPerCM')
        SgConf.RateOfCCP = GetValueByName(node, 'RateOfCCP')
        SgConf.CVExIP = GetAttrByName(node, 'CVExAddr', 'IP')
        SgConf.CVExPort = GetAttrByName(node, 'CVExAddr', 'Port')
        SgConf.McastIpList = GetMcastIpList(node)
        AllSgConf.Insert(SgConf)
    return AllSgConf


if __name__ == '__main__':
    #logger = INIT_LOGGER()
    #logger.SetConsoleLogLevel('DEBUG')
    AllSgConf = LoadSgConfig('../conf/SGConfig.xml')
    sgconfs = AllSgConf.SgConfDict
    for sgid in sgconfs:
        sgconfs[sgid].PrintDebug()
    #logconf = LoadLogConfig('../conf/LogConfig.xml')
    #logconf.PrintDebug()
    sys.exit()

