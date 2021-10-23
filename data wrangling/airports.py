#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete the 'extract_airports()' function so that it returns a list of airport
codes, excluding any combinations like "All".

Refer to the 'options.html' file in the tab above for a stripped down version
of what is actually on the website. The test() assertions are based on the
given file.
"""

from bs4 import BeautifulSoup
import os

html_page = "page_source_from_course.html"

def find_input(soup, tag, id):
    return soup.find(tag,id = id)

def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        tag = find_input(soup, 'select', 'AirportList')
        for option in tag.find_all("option"):
            t = option['value']
            if t != 'All' and t != 'AllMajors' and t != 'AllOthers':
                data.append(t)
        #print(data)
    return data


def test():
    html_doc = os.path.join(os.getcwd() + '\documents', html_page)
    data = extract_airports(html_doc)
    assert len(data) == 6
    assert "ATL" in data
    #assert "ABR" in data

if __name__ == "__main__":
    test()