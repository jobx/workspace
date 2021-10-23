# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 21:52:35 2021

@author: Guest.acc
"""
import os
import csv
import xlrd
from zipfile import ZipFile
import pprint

DATADIR = os.getcwd() + '\documents'
CSVDATAFILE = 'beatles-diskography.csv'

#################### csv file #####################

# DIY CSV
def parse_csv1(datafile):
    data = []
    
    with open(datafile,'r') as f:
        # get the headers
        headers = f.readline()
        
        # read the rest of the lines
        for line in f:
            # set empty dict
            entry = {}
            for header,v in zip(headers.split(","),line.split(",")):
                entry[header.strip()] = v.strip()
            data.append(entry)
            
    return data

# use csv package
def parse_csv2(datafile):
    data = []
    
    with open(datafile,'r') as f:
        lines = csv.DictReader(f)
        for line in lines:
            data.append(line)
            
    return data
    
def test1():
    datafile = os.path.join(DATADIR, CSVDATAFILE)
    d = parse_csv1(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

def test2():
    datafile = os.path.join(DATADIR, CSVDATAFILE)
    d = parse_csv2(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline
    
test1()
test2()

################### excel file #####################

EXCELDATAFILE = "2013_ERCOT_Hourly_Load_Data.xls"
EXCELZIPDATAFILE = "2013-ercot-hourly-load-data.zip"

def open_zip(datafile):
    with ZipFile(datafile,'r') as myzip:
        myzip.extractall()
        
def parse_excel_test(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    data = [[sheet.cell_value(r,col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]    
    print(data[3][2])
    
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            if row == 50:
                print(sheet.cell_value(row,col))
                
    print(sheet.cell_type(3,2))
    print(sheet.cell_value(3,2))
    print(sheet.col_values(3,start_rowx=1,end_rowx=4))
    
    print(sheet.cell_type(1,0))
    exceltime = sheet.cell_value(1,0)
    
    print(exceltime)
    print(xlrd.xldate_as_tuple(exceltime, 0))
    
def parse_excel(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)  
    
    data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
    }
    
    # get the column
    column = sheet.col_values(1,start_rowx = 1, end_rowx = None)
    
    # max, min & avg values
    data["maxvalue"] = max(column)
    data["minvalue"] = min(column)
    data["avgcoast"] = sum(column)/len(column)
    
    # find the index of max & min
    data["maxtime"] = xlrd.xldate_as_tuple(sheet.cell_value(column.index(max(column))+1,0),0)
    data["mintime"] = xlrd.xldate_as_tuple(sheet.cell_value(column.index(min(column))+1,0),0)
    
    return data

def test_excel()    :
     #datafile = os.path.join(DATADIR, EXCELZIPDATAFILE)   
     #open_zip(datafile)
     datafile = os.path.join(DATADIR, EXCELDATAFILE) 
     #parse_excel_test(datafile)
     data = parse_excel(datafile)
     pprint.pprint(data)
     
     assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
     assert round(data['maxvalue'], 10) == round(18779.02551, 10)
     
test_excel()