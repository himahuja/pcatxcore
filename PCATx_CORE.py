# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:10:12 2018

@author: alex
"""
import parser, pickle, difflib, nltk, json, queue, re
from webcrawlAll import crawlerWrapper
from PCATParser import *
import google_sub_all_level
from knowledge_management.WebResourceManager import *
from knowledge_management.ProfileManager import *
from gensim import models

def PCATx_CORE_supervised():
    name = input("What company would you like to crawl for?   ")
    pm = ProfileManager()
    wiki = wikiParser(name)
    newName = wiki[2]
    foundInDatabase = False
    if pm.get(name) != None or pm.get(newName) != None:
        foundInDatabase = True
        query = { 'name' : name }
        print("Currently web crawling: {}".format(name))
        driver = google_sub_all_level.setDriver()
        sub_list = google_sub_all_level.get_sub_list(name, driver)
    else:
        yon = input("Did you mean this company? (y/n) {}   ".format(wiki[2]))
        if yon.lower() == "y":
            query = { 'name' : newName }
            driver = google_sub_all_level.setDriver()
            sub_list = google_sub_all_level.get_sub(newName, driver)
        else:
            query = { 'name' : name }
            driver = google_sub_all_level.setDriver()
            sub_list = google_sub_all_level.get_sub_list(name, driver)
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
        #list of tuples (text, link)
        if pm.get(name) != None:
            resources = pm.get_resources_by_company(pm.get(name))
        else:
            resources = pm.get_resources_by_company(pm.get(newName))
        resources.append((str(wiki[0]), wiki[3]))
    else:
        resources = []
        resources.append((str(wiki[0]), wiki[3]))
    wrm.read_in_from_iterator(parser_iter(query['name'], url_list))
    if(len(wrm) > 0):
        wrm.save(file_name="data/webresourcemanagers/{}.json".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])))
    generate_HTML_output(wrm, wiki[4], sub_list, resources, query['name'])
#        wrm.train_classifier()
#        wrm.rank_by_relevance()

def PCATx_CORE_unsupervised(list_of_companies):
    company_queue = queue.Queue()

    for company in list_of_companies:
        company_queue.put(company)

    driver = google_sub.setDriver()
    while not company_queue.empty():
        name = company_queue.get()
        pm = ProfileManager()
        wiki = wikiParser(name)
        query = { 'name' : name }
        print("Currently web crawling: {}".format(name))
        sub_list = google_sub.get_sub(name, driver)
        for company in sub_list:
            company_queue.put(company)
        crawlerWrapper(query, "google", headless = False)
        with open("data/parsedLinks/{}.pk".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])), "rb") as handle:
            url_list = pickle.load(handle)
        wrm = WebResourceManager()
        resources = []
        wrm.read_in_from_iterator(parser_iter(query['name'], url_list))
        if(len(wrm) > 0):
            wrm.save(file_name="data/webresourcemanagers/{}.json".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])))
        generate_HTML_output(wrm, wiki[4], sub_list, resources, query['name'])

def basic_relevance_filter(document):
    new_doc = []
    for sentence in document:
        words = sentence.split()
        letters_in_sentence = sum([len(w) for w in words])
        if letters_in_sentence < 750 and letters_in_sentence > 50:
            new_doc.append(sentence)
    return new_doc


def generate_HTML_output(wrm, table, sub_list, dbresources, name):
    html = '<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>\n<title>{}</title>\n<meta charset="iso-8859-1">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<!--<link rel="stylesheet" href="../styles/layout.css" type="text/css">-->\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n</head>\n<body>\n<div style="width:49%; float:left; style:block"><center>{}</center></div>\n<div style="width:49%; float:right; style:block">\n<center><h2>We found this list of subsidiaries:</h2>\n<ul>\n'.format(name, table)
    for item in sub_list:
        html+='<a href="{}.html"><li>{}</li></a>\n'.format(item, item)
    html+='</center>\n</ul>\n</div>'
    for item in wrm:
        html+='\n</div>\n<div width="100%" style="display:block; clear:both"></div>\n<p style="visibility:hidden">break</p>\n<center><a href="{}"><h2>{}</h2></a></center>\n<div width="100%" style="display:block; clear:both"></div>\n\n\n<div style="width:49%; height:100%; float:left; min-height:600px; style:block">\n<iframe src="{}" style="width:100%; min-height:600px; style:block"></iframe>'.format(item['url'], item['url'], item['url'])
        if item['id'][-3:] == 'pdf':
            html+='\n\n<iframe src="../source/{}.pdf" style="width:100%; min-height:600px; style:block"></iframe>\n</div>\n<div style="width:49%; overflow:auto; height:1200px; float:right; style:block">'.format(item['id'])
        else:
            html+='\n\n<iframe src="../source/{}.html" style="width:100%; min-height:600px; style:block"></iframe>\n</div>\n<div style="width:49%; overflow:auto; height:1200px; float:right; style:block">'.format(item['id'])
        for sent in basic_relevance_filter(nltk.sent_tokenize(item['text'])):
            html+='\n<p>{}</p>\n'.format(sent)
        html+='</div>'
    for item in dbresources:
        html+='\n</div>\n<div width="100%" style="display:block; clear:both"></div>\n<p style="visibility:hidden">break</p>\n<center><a href="{}"><h2>{}</h2></a></center>\n<div width="100%" style="display:block; clear:both"></div>\n\n\n<div style="width:49%; height:100%; min-height:600px; float:left; style:block">\n<iframe src="{}" style="width:100%; min-height:600px; style:block"></iframe>\n</div>\n<div style="width:49%; overflow:auto; height:1200px; float:right; style:block">'.format(item[1], item[1], item[1])
        for sent in basic_relevance_filter(nltk.sent_tokenize(item[0])):
            html+='\n<p>{}</p>\n'.format(sent)
        html+='</div>'
    html+='</body>\n</html>'
    file = open("data/wrm_html_outputs/{}.html".format(re.sub('[^0-9A-Za-z-]+', '', name)), "w")
    file.write(html)
    file.close()

def main():
    company_list = json.loads(open("data/praedicat_data/target_companies_with_aliases.json").read())
    PCATx_CORE_unsupervised(company_list)

if __name__ == "__main__" :
    main()
