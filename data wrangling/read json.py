# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 20:01:12 2021

@author: Guest.acc
"""
import requests
import json
import pprint

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# define a structure to hold parameters
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}

def query_site(url,paras,uid="",fmt="json"):
    """
    this is the main function to call the web API to musicbrainz.org

    Parameters
    ----------
    url : the web API url.
    paras : parameters to go with the API url.
    uid : id used with some API
    fmt : "json" or "xml" The default is "json".

    Returns
    -------
    a json object

    """
    # assemble the url
    apiUrl = url + uid
    # assemble the paras: add option for json
    paras["fmt"] = fmt    
    # send the request
    r = requests.get(apiUrl, paras)
    # process outcome
    print("requesting: {0}".format(r.url))
    
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status
        
def query_by_name(url,paras,name):
    """
    this adds an artist name to the parameters before making the API call

    Parameters
    ----------
    url : API url
    paras : API parameter
    name : name of artist.

    Returns
    -------
    a json object

    """
    # assemble parameter
    paras["query"] = name
    return query_site(url, paras)

def pretty_print(data, indent = 4):
    if type(data) == dict:
        #with open("json.json",'w') as f:
        #    json_string = json.dumps(data, indent=indent, sort_keys=True)
        #    json.dump(data, f)
            
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        pprint.pprint(data)
    
def main():

    # query by name
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")        
    #pretty_pprint(results)
    # 
    print("\nARTIST")
    pretty_print(results["artists"][3])
    artist_id = results["artists"][3]["id"]
    # releases query
    artist_data = query_site(ARTIST_URL, query_type["releases"],artist_id)
    releases = artist_data["releases"]
    print(type(releases))
    release_title = [r["title"] for r in releases]
    for t in release_title:
        print(t)
    
    
if __name__ == '__main__':
    main()
    