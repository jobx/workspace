# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 16:24:22 2021

@author: Guest.acc
"""

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
import pprint

# simple navigation
def simple_navigation(soup):
    '''
    print(soup.title, soup.title.name, soup.title.string)
    print(soup.title.parenet)
    print(soup.p, soup.p['class'])
    print(soup.a, soup.find_all('a'), soup.find(id='link3'))
    '''
    print(soup.prettify())
    print("soup.title={0},\nsoup.title.name={1},\nsoup.title.string={2}\n".format(soup.title, soup.title.name, soup.title.string))
    print("soup.title.parent={0}".format(soup.title.parent))
    print("soup.p={0}, soup.p['class']={1}\n".format(soup.p,soup.p['class']))
    print("soup.a: ",soup.a)
    print("all a: ", soup.find_all('a'))
    print("id = link3: ",soup.find(id='link3'))     
    
    for As in soup.find_all('a'):
        print(As['href'])
        print(As.get('href'))
        
    # get all text 
    print(soup.get_text())
    
def kinds_of_objects():
    tag_object()
    navigable_string()
    bs_object()
    comment()

def tag_object():
    #tag
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>',features="lxml")
    tag = soup.b
    print("tag = {0},\ntag type: {1}\n,tag name: {2}".format(tag,type(tag),tag.name))
    # tag.name
    # this changes tag in both soup & tag
    tag.name = "blockquote"
    #print(tag, soup.b)
    print("tag: {0}\nsoup.b: {1}".format(tag,soup.b))
    
    # tag.attr
    #print(tag['class'], tag.attrs)
    print("tag['class']={0}\ntag.attrs={1}".format(tag['class'],tag.attrs))
    tag['another-attr'] = 1
    print(tag)
    # multi-valued attr    
    css_soup = BeautifulSoup('<p class="body"></p>',features="lxml")
    print(css_soup.p['class'])
    css_soup = BeautifulSoup('<p class="body strikeout"></p>',features="lxml")
    print(css_soup.p['class'])

def navigable_string():
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>',features="lxml")
    tag = soup.b
    print("tag.string: {0}\ntype(tag.string): {1}".format(tag.string, type(tag.string)))
    unicode_string = str(tag.string)
    print(unicode_string, type(unicode_string))
    #string replacement
    tag.string.replace_with("No longer bold")
    print(tag)
 
def bs_object():
    doc = BeautifulSoup("<document><content/>INSERT FOOTER HERE</document", "lxml")
    footer = BeautifulSoup("<footer>Here's the footer</footer>", "lxml")
    doc.find(text="INSERT FOOTER HERE").replace_with(footer)
    print("doc: {0}".format(doc))
    print("doc.name: {0}".format(doc.name))
    
def comment():    
    markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
    soup = BeautifulSoup(markup,"lxml")
    comment = soup.b.string
    print("comment: {0}\ntype: {1}".format(comment, type(comment)))
    print(soup.b.prettify())

def navigating_tree(soup):
    going_down(soup)
    going_up(soup)
    going_sideway(soup)
    going_backforth(soup)

def going_down(soup):
    #using tag
    print("navigate using tab names")
    print("head: {0}, title: {1}".format(soup.head,soup.title))
    print("tag names can be chained")
    print("b: {0} or body.b: {1}".format(soup.b, soup.body.b))
    #multiple value
    print("the first a: {0}".format(soup.a))
    pprint.pprint("all a: {0}".format(soup.find_all('a')))
    
    #content
    head_tag = soup.head
    print("soup.head: {0}".format(head_tag))
    print("soup.head.contents[0]: {0}".format(head_tag.contents[0]))
    print("soup.head.contents: {0}".format(head_tag.contents))
    #children
    for child in head_tag.children:
        print(child)
    #.descendants
    for child in head_tag.descendants:
        print(child)
        
    #.strings
    for string in soup.stripped_strings:
        print(repr(string))

def going_up(soup):
    #.parent
    title_tag = soup.title
    print("title: {0}\ntitle parent: {1}".format(title_tag,title_tag.parent))
    #string has parenet
    print("title string: {0}\ntitle string parent: {1}".format(title_tag.string,title_tag.string.parent))
    #parents
    link = soup.a
    print("link: {0}".format(link))
    for parent in link.parents:
        if parent is None:
            print(parent)
        else:
            print(parent.name)
            
def going_sideway(soup):
    sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>","lxml")
    print(sibling_soup.prettify())
    
    link = soup.a
    print("link: {0}\n link next sibling: {1}\nthe next sibling: {2}\
          ".format(link,link.next_sibling,link.next_sibling.next_sibling))
          
    for sibling in link.next_siblings:
        print(repr(sibling))
        
    for sibling in soup.find(id="link3").previous_siblings:
        print(repr(sibling))

def going_backforth(soup):
    last_a_tag = soup.find("a",id="link3")
    print("last a tag: {0}".format(last_a_tag))
    
    print("next sibling of last a tag: {0}".format(repr(last_a_tag.next_sibling)))
    print("next element of last a tag: {0}".format(last_a_tag.next_element))
    
def test():    
    soup = BeautifulSoup(html_doc,'html.parser')
    #print(soup.prettify())
    
    simple_navigation(soup)
    kinds_of_objects()
    navigating_tree(soup)
    
if __name__ == "__main__":
    test()      
    