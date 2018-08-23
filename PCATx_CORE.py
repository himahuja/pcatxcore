# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:10:12 2018

@author: alex
"""
import parser, pickle, difflib, nltk, json, queue, re
from webcrawlAll import crawlerWrapper, setDriver
from PCATParser import *
import Site_Crawler_Parser_All
from knowledge_management.WebResourceManager import *
from knowledge_management.ProfileManager import *
from gensim import models

def PCATx_CORE_supervised(recursive=True):
    """
    Runs the Web Crawling Architecture, PCATx CORE, in a supervised fashion
    
    Asks for a company name as input which it sends to Wikipedia. The dialog then asks if Wikipedia match (if one is found) is the company you are looking for and looks for close matches in the ProfileManager to retrieve relevant company info. From there, the Web Crawler retrieves relevant web pages and generate_HTML_output produces a Master Document. Web Resource Managers for each company are saved.

    
    Parameters
    ----------
    recursive : bool
        whether or not you'd like to call PCATx_CORE_unsupervised on the list of subsidiaries found (default = True)
    
    Returns
    -------
    None
    
    """
    name = input("What company would you like to crawl for?   ")
#    pm = ProfileManager()
    wiki = wikiParser(name)
    newName = wiki[2]
    foundInDatabase = False
    driver = setDriver()
#    if pm.get(name) != None or pm.get(newName) != None:
#        foundInDatabase = True
#        query = { 'name' : name }
#        print("Currently web crawling: {}".format(name))
#        driver = Site_Crawler_Parser_All.setDriver()
#        sub_list = Site_Crawler_Parser_All.get_sub(name, driver)
#    else:
    yon = input("Did you mean this company? (y/n) {}   ".format(wiki[2]))
    if yon.lower() == "y":
        query = { 'name' : newName }
        sub_list = Site_Crawler_Parser_All.get_sub(newName, driver)
    else:
        query = { 'name' : name }
        sub_list = Site_Crawler_Parser_All.get_sub(name, driver)
#        matches = difflib.get_close_matches(name, pm.get_aliases(), cutoff = .4) + difflib.get_close_matches(newName, pm.get_aliases(), cutoff = .4)
#        if len(matches) > 0:
#            print("0. None of the below")
#            for i in range(len(matches)):
#                print("{}. {}".format(str(i+1), matches[i]))
#            answer = input("Did you mean any of these?  ")
#            if answer != 0:
#                foundInDatabase = True
#                name = matches[int(answer)]
    crawlerWrapper(query, "google", driver, headless = True)
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
        wrm.save(file_name="data/webresourcemanager/webresourcemanagers/{}.json".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])))
    generate_HTML_output(wrm, wiki[4], sub_list, resources, query['name'])
    driver.quit()
    if recursive:
        PCATx_CORE_unsupervised(sub_list)

def PCATx_CORE_unsupervised(list_of_companies):
    """
    Runs the Web Crawling Architecture, PCATx CORE, in an unsupervised fashion
    
    The Web Crawler retrieves relevant web pages and generate_HTML_output produces a Master Document for each company in the list, adding subsidiaries found to the queue. Web Resource Managers for each company are saved. The queue is saved as JSON list at "data/PCATx_CORE_unsupervised_save_list.json" every 100 companies and when the function throws an exception

    
    Parameters
    ----------
    list_of_companies : list of strings
        the list of companies you would like to produce Master Documents for
    
    Returns
    -------
    None
    
    """
    company_queue = queue.Queue()

    for company in list_of_companies:
        company_queue.put(company)

    driver = setDriver()
    count = 0
    while not company_queue.empty():
        count+=1
        if count % 25 == 0:
            #hopefully helps us from getting blocked
            time.sleep(3)
        name = company_queue.get()
        pm = ProfileManager()
        wiki = wikiParser(name)
        query = { 'name' : name }
        print("Currently web crawling: {}".format(name))
        sub_list = Site_Crawler_Parser_All.get_sub(name, driver)
        for company in sub_list:
            if company != "":
                company_queue.put(company)
        try:
            crawlerWrapper(query, "google", driver)
            with open("data/parsedLinks/{}.pk".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])), "rb") as handle:
                url_list = pickle.load(handle)
            wrm = WebResourceManager()
            resources = []
            wrm.read_in_from_iterator(parser_iter(query['name'], url_list))
            if(len(wrm) > 0):
                wrm.save(file_name="data/webresourcemanager/webresourcemanagers/{}.json".format(re.sub('[^0-9A-Za-z-]+', '', query['name'])))
            generate_HTML_output(wrm, wiki[4], sub_list, resources, query['name'])
        except:
            driver = setDriver()
            company_queue.put(name)
            save_list = []
            while not company_queue.empty():
                company = company_queue.get()
                if company not in save_list:
                    save_list.append(company)
            for elem in save_list:
                company_queue.put(elem)
            file = open("data/PCATx_CORE_unsupervised_save_list.json", "w")
            file.seek(0)
            file.write(json.dumps(save_list, sort_keys = True, indent = 4))
            file.truncate()
            file.close()
        if count % 100 == 0:
            company_queue.put(name)
            save_list = []
            while not company_queue.empty():
                company = company_queue.get()
                if company not in save_list:
                    save_list.append(company)
            for elem in save_list:
                company_queue.put(elem)
            file = open("data/PCATx_CORE_unsupervised_save_list.json", "w")
            file.seek(0)
            file.write(json.dumps(save_list, sort_keys = True, indent = 4))
            file.truncate()
            file.close()



def basic_relevance_filter(document):
    """
    Basic relevance filter on the basis of characters in sentence. Filters out sentences with fewer than 50 characters or more than 750 characters.

    
    Parameters
    ----------
    document : list of strings
        a list of sentences you would like to filter
    
    Returns
    -------
    None
    
    """
    new_doc = []
    for sentence in document:
        words = sentence.split()
        letters_in_sentence = sum([len(w) for w in words])
        if letters_in_sentence < 750 and letters_in_sentence > 50:
            new_doc.append(sentence)
    return new_doc


def generate_HTML_output(wrm, table, sub_list, dbresources, name):
    """
    Generates an HTML Master Document

    
    Parameters
    ----------
    wrm : WebResourceManager
        the WebResourceManager tracking the web resources generated for the Master Document
    table : beautifulsoup.table
        the Wikipedia infobox table in HTML
    sub_list : list of strings
        list of subsidiaries
    dbresources : list of tuples (string (text), string (URL))
        a list of resources for the company in the company's profile in Profile Manager
    name : string
        name of the company the Master Document is about (for the title of the doc)
    
    Returns
    -------
    None
    
    """
    html = '<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>\n<title>{}</title>\n<meta charset="iso-8859-1">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<!--<link rel="stylesheet" href="../styles/layout.css" type="text/css">-->\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n</head>\n<body>\n<div style="width:49%; float:left; style:block"><center>{}</center></div>\n<div style="width:49%; float:right; style:block">\n<center><h2>We found this list of subsidiaries:</h2>\n<ul>\n'.format(name, table)
    for item in sub_list:
        html+='<a href="{}.html"><li>{}</li></a>\n'.format(re.sub('[^0-9A-Za-z-]+', '', item), item)
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
#    file = open("data/PCATx_CORE_unsupervised_save_list.json")
#    company_list = json.loads(file.read())
#    file.close()
    PCATx_CORE_supervised()

if __name__ == "__main__" :
    main()
