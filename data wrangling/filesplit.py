# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 22:37:02 2021

@author: xz
"""
import os
import re

datadir = os.getcwd() + '\documents'
f = "patent.data"

def split_string(file):
    #print(file)
    # xml tag
    xml = r'<\?xml version="1.0" encoding="UTF-8"\?>'
    p = [m.start() for m in list(re.finditer(xml, file))]
    #print(p)
    files = []
    for i in range(len(p)-1):
        files.append(file[p[i]:p[i+1]-1])
    files.append(file[p[-1]:-1])    
    return files

def save_files(strs):
    for i in range(len(strs)):
        # file name
        fname = datadir + "\{}-{}".format(f,i);
        #print(fname)
        #write the file
        with open(fname,'w') as file:
            file.write(strs[i])

def test():
    with open("{}\{}".format(datadir, f), "r") as file:
        s = split_string(file.read())
        save_files(s)
    
if __name__ == "__main__":
    test()    