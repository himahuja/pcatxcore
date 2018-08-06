# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:10:12 2018

@author: alex
"""
import parser, pickle, difflib, nltk
from webcrawlAll import crawlerWrapper
from PCATParser import *
from knowledge_management.WebResourceManager import *
from knowledge_management.ProfileManager import *
from gensim import models
import logging, re

def PCATx_CORE():
    name = input("What company would you like to crawl for?   ")
    pm = ProfileManager()
    wiki = wikiParser(name)
    newName = wiki[2]
    foundInDatabase = False
    if pm.get(name) != None or pm.get(newName) != None:
        foundInDatabase = True
        query = { 'name' : name }
        print("Currently web crawling: {}".format(name))
    else:
        yon = input("Did you mean this company? (y/n) {}   ".format(wiki[2]))
        if yon.lower() == "y":
            query = { 'name' : newName }
        else:
            query = { 'name' : name }
        matches = difflib.get_close_matches(name, pm.get_aliases(), cutoff = .4) + difflib.get_close_matches(newName, pm.get_aliases(), cutoff = .4)
        if len(matches) > 0:
            print("0. None of the below")
            for i in range(len(matches)):
                print("{}. {}".format(str(i+1), matches[i]))
            answer = input("Did you mean any of these?  ")
            if answer != 0:
                foundInDatabase = True
                name = matches[int(answer)]
    crawlerWrapper(query, "google")
#    crawlerWrapper(query, "google-subs")
    with open("data/parsedLinks/{}.pk".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])), "rb") as handle:
        url_list = pickle.load(handle)
    wrm = WebResourceManager()
    if foundInDatabase:
        #list of tuples (link, text)
        if pm.get(name) != None:
            resources = pm.get_resources_by_company(pm.get(name))
        else:
            resources = pm.get_resources_by_company(pm.get(newName))
        resources.append((wiki[3], str(wiki[0]) + str(wiki[1])))
    else:
        resources = []
        resources.append((wiki[3], str(wiki[0]) + str(wiki[1])))
    wrm.read_in_from_iterator(parser_iter(query['name'], url_list))
    if(len(wrm) > 0):
        wrm.save(file_name="data/webresourcemanagers/{}.json".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])))
    generate_HTML_output(wrm, resources, query['name'])
#        wrm.train_classifier()
#        wrm.rank_by_relevance()
        
def generate_HTML_output(wrm, dbresources, name):
    html = '<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>\n<title>{}</title>\n<meta charset="iso-8859-1">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<!--<link rel="stylesheet" href="../styles/layout.css" type="text/css">-->\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n</head>\n<body>'.format(name)
    for item in wrm:
        html+='<div width="100%" style="display:block; clear:both">\n<a href="{}"><iframe float: src="{}" style="width:49%; height:100%; min-height:600px; float:left; style:block"></iframe></a>'.format(item['url'],item['url'])
        html+='<p style="width:49%; float:right; style:block">\n{}\n</p>\n</div>\n<div width="100%" style="display:block; clear:both"></div>\n<p style="visibility:hidden">break</p>\n\n<div width="100%" style="display:block; clear:both"></div>'.format(nltk.sent_tokenize(item['text']))
    for item in dbresources:
        pass
    html+='</body>\n</html>'
    file = open("data/wrm_html_outputs/{}.html".format(name), "w")
    file.write(html)
    file.close()
        
def main():
    PCATx_CORE()
    
if __name__ == "__main__" :
    main()