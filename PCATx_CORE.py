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
        resources.append((wiki[3], str(wiki[0])))
    wrm.read_in_from_iterator(parser_iter(query['name'], url_list))
    if(len(wrm) > 0):
        wrm.save(file_name="data/webresourcemanagers/{}.json".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])))
    generate_HTML_output(wrm, wiki[4], resources, query['name'])
#        wrm.train_classifier()
#        wrm.rank_by_relevance()
    
def basic_relevance_filter(document):
#    rankings = []
#    bad_phrases = ['about me', 'navigation', 'all rights reserved', 'learn more', 'privacy policy', 'terms of use', 'contact us', 'subscribe']
#    good_phrases = ['produc', 'manufactur', 'chemical', 'hazard', 'activit']
#    for sentence in document:
#        count = 0
#        for word in bad_phrases:
#            if word in sentence:
#                count-=1
#        for word in good_phrases:
#            if word in sentence:
#                count+=1
#        rankings.append((count, sentence))
#    for i in range(1, len(rankings)):
#        key = rankings[i][0]
#        j = i-1
#        while j >=0 and key < rankings[j][0] :
#                rankings[j+1][0] = rankings[j][0]
#                j -= 1
#        rankings[j+1][0] = key
#    return rankings
    new_doc = []
    for sentence in document:
        words = sentence.split()
        letters_in_sentence = sum([len(w) for w in words])
        if letters_in_sentence < 750 and letters_in_sentence > 50:
            new_doc.append(sentence)
    return new_doc      
        
        
def generate_HTML_output(wrm, table, dbresources, name):
    html = '<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>\n<title>{}</title>\n<meta charset="iso-8859-1">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<!--<link rel="stylesheet" href="../styles/layout.css" type="text/css">-->\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n</head>\n<body>\n<center>{}</center>\n'.format(name, table)
    for item in wrm:
        html+='<div width="100%" style="display:block; clear:both">\n<iframe float: src="{}" style="width:49%; height:100%; min-height:600px; float:left; style:block"></iframe>\n<div style="width:49%; float:right; style:block">'.format(item['url'])
        for sent in basic_relevance_filter(nltk.sent_tokenize(item['text'])):
            html+='\n<p>{}</p>\n'.format(sent)
        html+='\n</div>\n</div>\n<div width="100%" style="display:block; clear:both"></div>\n<p style="visibility:hidden">break</p>\n\n<div width="100%" style="display:block; clear:both"></div>\n\n'
    for item in dbresources:
        html+='<div width="100%" style="display:block; clear:both">\n<iframe float: src="../source/{}" style="width:49%; height:100%; min-height:600px; float:left; style:block"></iframe>\n<div style="width:49%; float:right; style:block">'.format(item[0])
        for sent in basic_relevance_filter(nltk.sent_tokenize(item[1])):
            html+='\n<p>{}</p>\n'.format(sent)
        html+='\n</div>\n</div>\n<div width="100%" style="display:block; clear:both"></div>\n<p style="visibility:hidden">break</p>\n\n<div width="100%" style="display:block; clear:both"></div>\n\n'
    html+='</body>\n</html>'
    file = open("data/wrm_html_outputs/{}.html".format(name), "w")
    file.write(html)
    file.close()
        
def main():
    PCATx_CORE()
    
if __name__ == "__main__" :
    main()