# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 13:10:27 2021

@author: Guest.acc
"""
from bs4 import BeautifulSoup
import csv
import os
import pprint
import requests
import json

def get_carrierlist(soup):
    # select tage with name = 'carrierlist'
    carrierlist = []
    select_tag = soup.find_all("select",id = 'CarrierList')
    #print(select_tag)
    for carrier in select_tag[0].find_all("option"):
        carrierlist.append(str(carrier.string).strip())
    return carrierlist

def writelist_csv(file,data):
    with open(file,'w') as f:
        writer = csv.writer(f, delimiter = '\n')
        writer.writerow(data)

def writedict_csv(fieldnames,file,data):
    #data: list of dictionary
    with open(file,'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
def get_airportlist(soup):
    # return list of dictionary
    # select tage with name = 'carrierlist'
    airportlist = []    
    
    select_tag = soup.find_all("select",id = 'AirportList')
    #print(select_tag)
    for airport in select_tag[0].find_all("option"):
        data = {'Airport Code':None,'Airport Description':None}
        
        data['Airport Code'] = airport['value']
        data['Airport Description'] = str(airport.string).strip()
        airportlist.append(data)
        
    return airportlist

def find_input(soup, tag, id):
    return soup.find(tag,id = id)
    
def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html,'html.parser')
        #tag = soup.find('input',id = "__EVENTVALIDATION")
        tag = find_input(soup, 'input', "__EVENTVALIDATION")
        data["eventvalidation"] = tag['value']
        tag = find_input(soup, 'input', "__VIEWSTATE")
        data["viewstate"] = tag['value']

    return data

'''
def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text
'''

def test():
    DATADIR =  os.getcwd() + '\documents'
    CSVFILE1 = "carrierlist.csv"
    CSVFILE2 = "airportlist.csv"
    HTMLFILE = "page_source.html"
    HTMLFILE1 = "page_source_from_course.html"
    
    html_doc = os.path.join(DATADIR, HTMLFILE)
    
    # airport and air carrier lists
    soup = BeautifulSoup(open(html_doc),'html.parser')
    csv_carrier = os.path.join(DATADIR, CSVFILE1)
    writelist_csv(csv_carrier, get_carrierlist(soup))
    csv_carrier = os.path.join(DATADIR, CSVFILE2)
    writedict_csv(['Airport Code','Airport Description'],csv_carrier, get_airportlist(soup))
    
    # build the http post request    
    data = extract_data(os.path.join(DATADIR, HTMLFILE1))
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")
        
if __name__ == "__main__":
    test()    

