#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task in this exercise is to modify 'extract_carrier()` to get a list of
all airlines. Exclude all of the combination values like "All U.S. Carriers"
from the data that you return. You should return a list of codes for the
carriers.

All your changes should be in the 'extract_carrier()' function. The
'options.html' file in the tab above is a stripped down version of what is
actually on the website, but should provide an example of what you should get
from the full file.

Please note that the function 'make_request()' is provided for your reference
only. You will not be able to to actually use it from within the Udacity web UI.
"""

from bs4 import BeautifulSoup
import requests
import os
import pprint

html_page = "page_source.html"

def find_input(soup, tag, id):
    return soup.find(tag,id = id)

def extract_carriers(soup):
    data = []

    #with open(page, "r") as html:
        # do something here to find the necessary values
        #soup = BeautifulSoup(html, "lxml")
        # find the tag
    tag = find_input(soup, "select", "CarrierList")
    for option in tag.find_all("option"):
        t = option['value']
        if t == 'All' or t == 'AllUS' or t =='AllForeign' or t =='AllScheduled':
            pass
        else:
            data.append(option['value'])
        #print(data)
        #print(len(data))
    return data

def extract_airports(soup):
    data = []
    #with open(page, "r") as html:
        # do something here to find the necessary values
        #soup = BeautifulSoup(html, "lxml")
    tag = find_input(soup, 'select', 'AirportList')
    for option in tag.find_all("option"):
        t = option['value']
        if t != 'All' and t != 'AllMajors' and t != 'AllOthers':
            data.append(t)
        #print(data)
    return data

def extract_data(soup):
    data = {"eventvalidation": "",
            "viewstate": "",
            "eventtarget":"",
            "eventargument":"",
            "viewstategenerator":""}
    
    #with open(page, "r") as html:
        # do something here to find the necessary values
        #soup = BeautifulSoup(html,'html.parser')
        #tag = soup.find('input',id = "__EVENTVALIDATION")
    tag = find_input(soup, 'input', "__EVENTVALIDATION")
    if tag != None:
        data["eventvalidation"] = tag['value']
    tag = find_input(soup, 'input', "__VIEWSTATE")
    if tag != None:
        data["viewstate"] = tag['value']
    tag = find_input(soup, 'input', "__EVENTTARGET")
    if tag != None:
        data["eventtarget"] = tag['value']
    tag = find_input(soup, 'input', "__EVENTARGUMENT")
    if tag != None:
        data["eventargument"] = tag['value']
    tag = find_input(soup, 'input', "__VIEWSTATEGENERATOR")
    if tag != None:
        data["viewstategenerator"] = tag['value']

    return data

def make_request(s, data, file):
    eventtarget = data["eventtarget"]
    eventargument = data["eventargument"] 
    viewstategenerator = data["viewstategenerator"]
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]    

    r = s.post("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
               data = (("__EVENTTARGET", eventtarget),
                       ("__EVENTARGUMENT", eventargument),
                       ("__VIEWSTATE", viewstate),
                       ("__VIEWSTATEGENERATOR",viewstategenerator),
                       ("__EVENTVALIDATION", eventvalidation),
                       ("CarrierList", carrier),
                       ("AirportList", airport),
                       ("Submit", "Submit")))
    f = open(file,'w')
    return f.write(r.text)
    #return r.text

def get_file(s, airport, carrier, data, file):
    data1 = {"eventtarget":data["eventtarget"],
            "eventargument":data["eventargument"],
            "viewstate":data["viewstate"],
            "viewstategenerator":data["viewstategenerator"],
            "eventvalidation":data["eventvalidation"],
            "carrier":carrier,
            "airport":airport,
            "Submit":"Submit"}
    
    return make_request(s, data1, file)
    #return data1
    
def test1():
    html_doc = os.path.join(os.getcwd() + '\documents', html_page)
    soup = BeautifulSoup(open(html_doc),'html.parser')
    
    s = requests.Session()
    r = s.get("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2", verify = False)
    soup = BeautifulSoup(r.text)
    
    carriers = extract_carriers(soup)
    airports = extract_airports(soup)
    data = extract_data(soup)
    file = os.path.join(os.getcwd() + '\documents\data', "UA-MKE.html")
    data1 = get_file(s, "MKE", "UA", data, file)
    print(carriers)
    print(airports)

if __name__ == "__main__":
    test1()