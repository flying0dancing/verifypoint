#!/usr/bin/python
# -*- coding: UTF-8 -*-
import winreg
import json
import os.path

def main():
    base_dir=os.path.dirname(os.path.abspath(__file__))
    json_inputfile='VerifyPoint.json'
    json_outputfile='VerifyPoint_output.json'
    jsonObj=getJson(updateFileSeperator(base_dir)+json_inputfile)
    resultList=['id','total','pass','fail','skip']
    formatStr="caseId:{result[id]} [total:{result[total]} pass:{result[pass]} fail:{result[fail]}]"
    for obj in jsonObj:
        if 'skip' in obj:
            continue
        result={k:0 for k in resultList} #init result map {'id':0,'total':0,'pass':0,'fail':0,'skip':0}
        if obj['method'].lower()=='verifyregkey':
            verifyRegKey(obj,result)
        if obj['method'].lower()=='verifyfiles':
            verifyFilesExist(obj,result)
        obj['result']=result
        print('\n')
    setJson(updateFileSeperator(base_dir)+json_outputfile,jsonObj)
    for obj in jsonObj:
        if 'skip' in obj:
            continue
        print(formatStr.format(result=obj['result']))

def verifyFilesExist(obj,result):
    formatStr4Print="file {0}exist.[{1}][notes:{2}]"
    result['id']=obj['id']
    files=combineFullNames(obj['dirs'], obj['files'])
    result['total']=len(files)
    print("caseId:{0}".format(obj['id']))
    for tfile in files:
        if fileExist(tfile):
            print(formatStr4Print.format("",tfile,obj['notes']))
            result['pass']+=1
        else:
            print(formatStr4Print.format("doesn't ",tfile,obj['notes']))
            result['fail']+=1

def verifyRegKey(obj,result):
    result['id']=obj['id']
    print("caseId:{0}".format(obj['id']))
    result['total']=1
    formatStr4Print="value name: {0},value data:{1} is {2}\n    details:[{3}]\n    notes:[{4}]"
    if getValueDataOfRegKey(obj['keyname'],obj['valuename'])==obj['valuedata']:
        print(formatStr4Print.format(obj['valuename'],obj['valuedata'],'pass',obj['keyname'],obj['notes']))
        result['pass']=1
    else:
        print(formatStr4Print.format(obj['valuename'],obj['valuedata'],'fail',obj['keyname'],obj['notes']))
        result['fail']=1


def getValueDataOfRegKey(keyName, valueName):
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
            #print(name,value,type)
            if name==valueName:
                return value
            i+=1
    except WindowsError:
        print()
    return None

def combineFullNames(dirs,files):
    fullnames=[]
    for tdir in dirs:
        if not isEmptyStr(tdir):
            tdir=updateFileSeperator(tdir)
            fullnames.extend([tdir+updateStr(tfile) for tfile in files])
    return fullnames

def updateStr(str):
    if isEmptyStr(str):
        str=""
    return str
    
def getJson(fname):
    obj=None
    with open(fname,'r',encoding='utf-8') as fileHd:#for reading chinese charactors
        obj=json.load(fileHd)
    return obj 

def setJson(fname,obj):
    with open(fname,'w',encoding='utf-8') as fileHd:
        json.dump(obj,fileHd,ensure_ascii=False,sort_keys=True,indent=4)#for writing chinese charactors

def fileExist(fname):
    flag=False
    if not isEmptyStr(fname):
        flag=os.path.exists(fname)
    return flag

def updateFileSeperator(filePath):
    if not isEmptyStr(filePath):
        if filePath.find("\\")!=-1:
            filePath.replace("\\","/")
        if filePath.endswith("/"):
            pass
        else:
            filePath=filePath+"/"
    return filePath

def isEmptyStr(str):
    flag=False
    if(str==None or str=='' or str.strip()==''):
        flag=True
    return flag

if __name__=='__main__':
    main()
    input('press any key to quit...')
        