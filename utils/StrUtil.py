#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
from utils import Logger
logger = logging.getLogger('utils.StrUtil')

def combineFullNames(dirs,files):
    fullnames=[]
    if dirs and len(dirs)>0:
        for tdir in dirs:
            tdir=updateFileSeperator(tdir)
            fullnames.extend([tdir+defaultEmpty(tfile) for tfile in files])
    else:
        fullnames.extend([defaultEmpty(tfile) for tfile in files])
    return fullnames

"""
default empty str to ''
"""
def defaultEmpty(str):
    if isEmptyStr(str):
        logger.debug("set default empty string to ''.")
        str=""
    return str

"""
:return file path ends with \ or /
"""
def updateFileSeperator(filePath):
    if not isEmptyStr(filePath):
        if filePath.find("\\")!=-1:
            filePath.replace("\\","/")
        if filePath.endswith("/"):
            pass
        else:
            filePath=filePath+"/"
    return filePath

"""
:return true or false, string is None or '' or '  ' return true
"""
def isEmptyStr(str):
    flag=False
    if(str==None or str=='' or str.strip()==''):
        logger.debug("String is empty.")
        flag=True
    return flag
