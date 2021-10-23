# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:47:21 2021

@author: Guest.acc
"""

import os
#import xml.etree.ElementTree as ET
import pprint
from xml.etree import ElementTree as ET, ElementInclude as EI

DATADIR =  os.getcwd() + '\documents'
DATAFILE = "countries.xml"
outfile = ""

def ET_Tutorial(file):
    # get the root
    tree = ET.parse(file)
    root = tree.getroot()
    pprint.pprint('root tag: {0}, root attributes: {1}'.format(root.tag, root.attrib))
    # get all the children
    for child in root:
        pprint.pprint('child tag: {0}, child attributes: {1}, child text: {2}'.format(child.tag, child.attrib, child.text))
    # access specific nodes
    print(root[0][1].text)    
    
    for neighbor in root.iter('neighbor'):
        print(neighbor.attrib)
        
    for country in root.findall('country'):
        rank = country.find('rank').text
        name = country.get('name')
        print(name,rank)
    # modify xml
    for rank in root.iter('rank'):
        new_rank = int(rank.text) + 1
        rank.text = str(new_rank)
        rank.set('updated','yes')
    
    for country in root.findall('country'):
        rank = int(country.find('rank').text)
        if rank > 50:
            root.remove(country)
        
    tree.write('output.xml')
    
 
def ET_Namespace_Tutorial(file):
    tree = ET.parse(file)
    root = tree.getroot()
    
    ns = {'real_person': 'http://people.example.com',
      'role': 'http://characters.example.com'}
    for actor in root.findall('real_person:actor',ns):
        name = actor.find('real_person:name',ns)
        print(name.text)
        for char in actor.findall('role:character',ns):
            print('|-->',char.text)
        
def XPath_Tutoral(file):
    tree = ET.parse(file)
    root = tree.getroot()
    # top-level    
    toplevel = root.findall(".")
    for country in toplevel[0]:
        print(country.tag, country.attrib)
        
    # top -> country -> neighors
    for neighbor in root.iter('neighbor'):
        print(neighbor.attrib)
    for country in root.findall('country'):
        for n in country.findall('neighbor'):
            print(n.attrib)
    for n in root.findall('./country/neighbor'):
        print(n.attrib)
        
    # country nodes: name = 'Singapore' have a 'year' child
    country = root.findall(".//year/..[@name = 'Singapore']")
    for c in country:
        print(c.attrib)
        
    # year node: name = 'Signapore'
    years = root.findall(".//country[@name='Singapore']/year")
    for year in years:
        print(year.text)
        
    # all 'neighor' nodes that are the second child of their parents
    for neighbor in root.findall(".//neighbor[2]"):
        print(neighbor.attrib)
        
def XInclude_Tutorial(file):
    tree =   ET.parse(file)
    root = tree.getroot()
    EI.include(root)
    
    tree.write('include.xml')
    
def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    ET_Tutorial(datafile)
    
    ns_xml =  os.path.join(DATADIR, 'namespace.xml')

    ET_Namespace_Tutorial(ns_xml)
    
    XPath_Tutoral(datafile)
    
    XInclude_Tutorial(os.path.join(DATADIR, 'document1.xml'))
    XInclude_Tutorial(os.path.join(DATADIR, 'document2.xml'))
    
if __name__ == "__main__":
    test()    