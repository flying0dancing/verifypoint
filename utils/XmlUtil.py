#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import shutil
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et
from xml.dom import minidom
import logging
from utils import Logger
logger = logging.getLogger('checker.XmlUtil')

def verifyElement1(xmlfile,verifyElt):
    logger.debug("verify element {0}".format(verifyElt))
    tree = et.parse(xmlfile)
    root = tree.getroot()
    flag=False
    for rootChild in root:
        logger.debug(rootChild.tag + ":" )
        logger.debug(rootChild.attrib)
        if verifyTagAttributes(rootChild, verifyElt):
            flag=True
            break
    #tree.write(xmlfile)
    #tree.write(xmlfile, encoding="utf-8", xml_declaration=True)
    return flag

def verifyElement(xmlfile,verifyParentElt,verifyElt):
    logger.debug("verify element {0} under {1}".format(verifyElt,verifyParentElt))
    tree = et.parse(xmlfile)
    root = tree.getroot()
    flag=False
    findParent=False
    for rootChild in root:
        logger.debug(rootChild.tag + ":")
        logger.debug(rootChild.attrib)
        if verifyTagAttributes(rootChild, verifyParentElt):
            findParent=True
            for child in rootChild:
                if verifyTagAttributes(child, verifyElt):
                    flag=True
                    break
    if not findParent:
        logger.error("cannot find parent element {0}".format(verifyParentElt))
    #tree.write(xmlfile)
    #tree.write(xmlfile, encoding="utf-8", xml_declaration=True)
    return flag

def verifyTagAttributes(elt,eltVerify):
    flag=True
    if eltVerify['tag']==elt.tag:
        for attr in eltVerify['attributes']:
            if attr in elt.attrib and eltVerify['attributes'][attr]==elt.attrib[attr]:
                logger.debug("verify element's attrib:{0}:{1} is in this element's attrib:{1}".format(attr, elt.attrib[attr]))
            else:
                flag=False
    else:
        flag=False
    return flag
