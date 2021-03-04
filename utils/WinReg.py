#!/usr/bin/python
# -*- coding: UTF-8 -*-
import winreg
import logging
from utils import Logger
logger = logging.getLogger('checker.WinReg')

def getValueDataOfRegKey(keyName, valueName):
    logging.debug("reg key is {0}".format(keyName))
    firstSlash=keyName.find('\\')
    if firstSlash==-1:
        return
    keyStart=keyName[:firstSlash]
    switch={'HKEY_CURRENT_USER':winreg.HKEY_CURRENT_USER, 'HKEY_LOCAL_MACHINE':winreg.HKEY_LOCAL_MACHINE}
    regKey=winreg.OpenKey(switch[keyStart.upper()],keyName[firstSlash+1:])

    try:
        i=0
        while 1:
            name,value,type=winreg.EnumValue(regKey,i)
            logging.debug("value name:{0}, data:{1}, type:{2}".format(name,value,type))
            if name==valueName:
                logging.debug("get the value name {0}".format(name))
                return value
            i+=1
    except WindowsError:
        print()
    return None
