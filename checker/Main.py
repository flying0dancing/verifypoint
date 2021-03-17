#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from docs import Conf
from utils import FileUtil
from utils import StrUtil
from utils import WinReg
from utils import XmlUtil
from utils import Logger
logger = logging.getLogger('checker.Main')
BUILD_STATUS=True
def main(inputfile,resultfile):

    base_dir=Conf.BASE_DIR
    #json_inputfile='VerifyPoint.json'
    #json_outputfile='VerifyPoint_output.json'
    json_inputfile = inputfile
    json_outputfile = resultfile
    json_outputpath=StrUtil.updateFileSeperator(base_dir)+'results/'
    jsonObj=FileUtil.getJson(StrUtil.updateFileSeperator(base_dir)+json_inputfile)
    resultList=['id','total','pass','fail','skip']
    formatStr="caseId:{result[id]} [total:{result[total]} pass:{result[pass]} fail:{result[fail]}]"
    for obj in jsonObj:
        if 'skip' in obj:
            continue
        logger.info('setup environment')
        result={k:0 for k in resultList} #init result map {'id':0,'total':0,'pass':0,'fail':0,'skip':0}
        if obj['method'].lower() == 'verifyxmlelementnotexist':
            verifyXmlElementNotExist(obj, result)
        if obj['method'].lower() == 'verifyxmlatrr':
            verifyXmlAtrr(obj, result)
        if obj['method'].lower() == 'verifyregkey':
            verifyRegKey(obj, result)
        if obj['method'].lower() == 'verifyfiles':
            verifyFilesExist(obj, result)
        obj['result']=result
        logger.info('tear down\n')
    FileUtil.createDirectories(json_outputpath)
    FileUtil.setJson(json_outputpath+json_outputfile,jsonObj)
    for obj in jsonObj:
        if 'skip' in obj:
            continue
        logger.info(formatStr.format(result=obj['result']))

def verifyFilesExist(obj,result):
    formatStr4Print="{0} on verified file {1}exist.[{2}][notes:{3}]"
    result['id']=obj['id']
    dirs = None
    if 'dirs' in obj:
        dirs = obj['dirs']
    files=StrUtil.combineFullNames(dirs, obj['files'])
    result['total']=len(files)
    logger.info("caseId:{0}".format(obj['id']))
    for tfile in files:
        if FileUtil.fileExist(tfile):
            logger.info(formatStr4Print.format("pass","",tfile,obj['notes']))
            result['pass']+=1
        else:
            logger.info(formatStr4Print.format("fail","doesn't ",tfile,obj['notes']))
            result['fail']+=1

def verifyRegKey(obj,result):
    result['id']=obj['id']
    logger.info("caseId:{0}".format(obj['id']))
    result['total']=1
    formatStr4Print="{2} on verified registry value name: {0},value data:{1}\n    details:[{3}]\n    notes:[{4}]"
    if WinReg.getValueDataOfRegKey(obj['keyname'],obj['valuename'])==obj['valuedata']:
        logger.info(formatStr4Print.format(obj['valuename'],obj['valuedata'],'pass',obj['keyname'],obj['notes']))
        result['pass']=1
    else:
        logger.info(formatStr4Print.format(obj['valuename'],obj['valuedata'],'fail',obj['keyname'],obj['notes']))
        result['fail']=1

def verifyXmlAtrr(obj,result):
    result['id'] = obj['id']
    logger.info("caseId:{0}".format(obj['id']))
    formatStr4Print = "{3} on verified element: {0} {1} {2}\n    notes:[{4}]"
    dirs = None
    if 'dirs' in obj:
        dirs = obj['dirs']
    files = StrUtil.combineFullNames(dirs, obj['files'])
    total=0
    if not files or len(files)==0:
        result['fail'] = 1
        total = 1
        logger.log("fail on file doesn't exist, please provide files.")
    for tfile in files:
        if 'parentElements' in obj and len(obj['parentElements']) > 0:
            for parentElement in obj['parentElements']:
                for tElement in obj['elements']:
                    flag=XmlUtil.verifyElement(tfile, parentElement, tElement)
                    total += 1
                    if flag:
                        logger.info(formatStr4Print.format(tElement, 'under element:', parentElement, 'pass', obj['notes']))
                        result['pass'] += 1
                    else:
                        logger.info(formatStr4Print.format(tElement, 'under element:', parentElement, 'fail', obj['notes']))
                        result['fail'] += 1
        else:
            for tElement in obj['elements']:
                flag=XmlUtil.verifyElement1(tfile, tElement)
                total += 1
                if flag:
                    logger.info(formatStr4Print.format(tElement, '', '', 'pass', obj['notes']))
                    result['pass'] += 1
                else:
                    logger.info(formatStr4Print.format(tElement, '', '', 'fail', obj['notes']))
                    result['fail'] += 1
    result['total'] = total


def verifyXmlElementNotExist(obj,result):
    result['id'] = obj['id']
    logger.info("caseId:{0}".format(obj['id']))
    formatStr4Print = "{3} on verified element: {0} {1} {2}\n    notes:[{4}]"
    dirs=None
    if 'dirs' in obj:
        dirs=obj['dirs']
    files = StrUtil.combineFullNames(dirs, obj['files'])
    total=0
    if not files or len(files)==0:
        result['fail'] = 1
        total = 1
        logger.log("fail on file doesn't exist, please provide files.")
    for tfile in files:
        if 'parentElements' in obj and len(obj['parentElements']) > 0:
            for parentElement in obj['parentElements']:
                for tElement in obj['elements']:
                    flag=XmlUtil.verifyElement(tfile, parentElement, tElement)
                    total += 1
                    if not flag:
                        logger.info(formatStr4Print.format(tElement, 'not existed under element:', parentElement, 'pass', obj['notes']))
                        result['pass'] += 1
                    else:
                        logger.info(formatStr4Print.format(tElement, 'existed under element:', parentElement, 'fail', obj['notes']))
                        result['fail'] += 1
        else:
            for tElement in obj['elements']:
                flag=XmlUtil.verifyElement1(tfile, tElement)
                total += 1
                if not flag:
                    logger.info(formatStr4Print.format(tElement, 'not existed', '', 'pass', obj['notes']))
                    result['pass'] += 1
                else:
                    logger.info(formatStr4Print.format(tElement, 'existed', '', 'fail', obj['notes']))
                    result['fail'] += 1
    result['total'] = total


if __name__=='__main__':
    json_inputfile='VerifyPoint.json'
    json_outputfile='VerifyPoint_output.json'
    main(json_inputfile,json_outputfile)
    input('press any key to quit...')
    #flag=main()
    #print(flag)
        