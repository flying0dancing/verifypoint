#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, csv,logging,re
import json
import os.path
import configparser
from utils import StrUtil
from utils import Logger
logger = logging.getLogger('utils.FileUtil')


"""
:return true or false
"""
def fileExist(fname):
    flag=False
    if not StrUtil.isEmptyStr(fname):
        flag=os.path.exists(fname)
    return flag


def getJson(fname):
    obj=None
    with open(fname,'r',encoding='utf-8') as fileHd:#for reading chinese charactors
        obj=json.load(fileHd)
    return obj

def setJson(fname,obj):
    with open(fname,'w',encoding='utf-8') as fileHd:
        json.dump(obj,fileHd,ensure_ascii=False,sort_keys=True,indent=4)#for writing chinese charactors

def createDirectories(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__=='__main__':
    pass