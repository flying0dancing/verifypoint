#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,datetime
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from checker import Main
base_name=os.path.basename(os.path.abspath(__file__))
mainName=base_name.replace('.py','')
suffixName='.json'
inputfile=mainName+suffixName
resultfile=mainName+'['+datetime.datetime.now().strftime("%Y-%m-%d")+']'+suffixName
Main.main(inputfile,resultfile)