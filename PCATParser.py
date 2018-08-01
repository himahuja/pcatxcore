#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, os, webbrowser, PyPDF2, nltk, pdfkit, re, wikipedia, json, sys, unicodedata, requests
import wikipedia as wiki
sys.path.append
from knowledge_management.ProfileManager import *

def tag_visible(element):
    """
    HELPER FUNCTION
    Boolean function that filters out non-required tags in HTML-pages
    """
    if element.parent.name in ['[document]', 'head', 'style', 'script', 'title', 'header', 'meta', 'footer']:
        return False
    if isinstance(element, Comment):
        return False
    if element.name in ['header','footer','button','nav']:
        return False
    return True

def text_from_html(body):

    soup = BeautifulSoup(body.decode("utf-8", "ignore"), 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)

def sentence_filter(text_list):
    new_list = [] + text_list
    for sent in text_list:
        for i in range(len(sent) - 2):
            if sent[i] == sent[i+1] and sent[i+1] == sent[i+2]:
                if sent in new_list:
                    new_list.remove(sent)
    return new_list

def get_PDF_content(query_string, link, linkList=None, name=None):
    #download pdf file ,from web
    content=urllib.request.urlopen(link).read()
    if linkList != None:
        file_name = query_string+str(linkList.index(link))+".pdf"
    else:
        file_name = query_string+name
        file_name = re.sub('[^A-Za-z0-9]+', '', file_name)
        if len(file_name) > 240:
                file_name = file_name[:240]
        file_name = file_name + ".pdf"
    fout=open(os.path.join("data/tmp", file_name), "wb")
    fout.write(content)
    fout.close()

    #convert PDF to text
    content = ""
    #load PDF into PyPDF2
    pdf = PyPDF2.PdfFileReader(os.path.join("data/tmp/", file_name))

    if pdf.isEncrypted:
        pdf.decrypt('')
    #iterate pages
    for i in range(pdf.getNumPages()):
    #extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
        content = " ".join(content.replace("\xa0", " ").strip().split())
    return content

def parser(query_string, linkList):
    for link in linkList:
        if link[-4:] != '.pdf':
            try:
                file_name = query_string+str(linkList.index(link)) + ".txt"
                text_file = open(os.path.join("data/sentences", file_name), "w")
                html_file = open(os.path.join("data/source", file_name+".html"), "w")
                html = urllib.request.urlopen(link).read()
                html_file.write(html.decode("utf-8", "ignore"))
                text_list = sentence_filter(nltk.sent_tokenize(text_from_html(html)))
                text_file = open(os.path.join("data/sentences", file_name), "w")
                text_file.write(link + "\n")
                for i in range(len(text_list)):
                    text_list[i] = bytes(text_list[i], 'utf-8').decode('utf-8', 'ignore')
                    text_file.write(text_list[i].strip() + "\n")
                text_file.close()
            except Exception as e:
                print(link + " threw the following exception " + str(e))
        else:
            try:
                content = get_PDF_content(query_string, link, linkList=linkList)
                file_name = query_string+str(linkList.index(link))+".txt"
                text_list = sentence_filter(nltk.sent_tokenize(content))
                text_file = open(os.path.join("data/sentences", file_name), "w")
                text_file.write(link + "\n")
                for i in range(len(text_list)):
                    text_list[i] = bytes(text_list[i], 'utf-8').decode('utf-8', 'ignore')
                    text_file.write(text_list[i].strip() + "\n")
                text_file.close()
            except Exception as e:
                print(link + " threw the following exception " + str(e))
        print("...{:.2f}% done, processing link {}".format(((linkList.index(link)+1)/len(linkList))*100,linkList.index(link)))

def parse_single_page(link):
    if link[-4:] != '.pdf':
            try:
                html = urllib.request.urlopen(link).read()
                return bytes(text_from_html(html), 'utf-8').decode('utf-8', 'ignore')
            except Exception as e:
                print(link + " threw the following exception " + str(e))
    else:
            try:
                return get_PDF_content("test", link, name=link)
            except Exception as e:
                print(link + " threw the following exception " + str(e))

def parser_iter(query_string, linkList):
    for link in linkList:
        doc = {'url' : link, 'query': query_string }
        if link[-4:] != '.pdf':
            try:
                html = urllib.request.urlopen(link).read()
                doc['html'] = html
                doc['text'] = bytes(text_from_html(html), 'utf-8').decode('utf-8', 'ignore')
                yield doc
            except Exception as e:
                print(link + " threw the following exception " + str(e))
        else:
            try:
                content = get_PDF_content(query_string, link, linkList)
                doc['pdf'] = urllib.request.urlopen(link).read()
                doc['text'] = content
                yield doc
            except Exception as e:
                print(link + " threw the following exception " + str(e))
        print("...{:.2f}% done, processing link {}".format(((linkList.index(link)+1)/len(linkList))*100,linkList.index(link)))

def contain(sent,word_list):
    for i in range(len(word_list)):
        if word_list[i] in sent:
            return True
    return False

def eightk_parser(link):
    try:
        html = urllib.request.urlopen(link).read()
        text_list = nltk.sent_tokenize(text_from_html(html).replace("\n", "."))
#        print(text_list)
        start = False
        stop = False
        info = ''
        for sent in text_list:
            if stop:
                return info
            elif contain(sent,['SIGNATURE']):
                #print('end')
                stop = True
            elif start:
                info += sent
            elif contain(sent,['Item','ITEM']):
                #print('start')
                start = True
        return info
    except Exception as e:
        print('{} threw an the following exception during 8K parsing {}'.format(link, str(e)))

def ex21_parser(link):
    try:
        body = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(body, 'lxml')
        table = soup.findAll('table')
        if table != []:
            sub_list = []
            for t in table:
                row = t.findAll('tr')
                for r in row[1:]:
                    division = r.findAll('td')
                    #for d in division[0]:
                    if len(division) > 0:
                        d = division[0]
                        desc = d.get_text().strip('\n')
                        sub_list.append(desc)
            if sub_list != []:
                for i in range(len(sub_list)):
                    sub_list[i] = sub_list[i].replace("\xa0", " ").replace("\n", "").strip()
                return sub_list
            else:
                html = urllib.request.urlopen(link).read()
                text_list = text_from_html(html).splitlines()
                for i in range(len(text_list)):
                    text_list[i] = re.sub('[\s][\s]+[\S]+', "", text_list[i].replace("\xa0", " ").replace("\n", "").replace("-", "").strip())
                while "" in text_list:
                    try:
                        text_list.remove("")
                    except:
                        pass
                return text_list
        else:
            html = urllib.request.urlopen(link).read()
            text_list = text_from_html(html).splitlines()
            for i in range(len(text_list)):
                text_list[i] = re.sub('[\s][\s]+[\S]+', "", text_list[i].replace("\xa0", " ").replace("\n", "").replace("-", "").strip())
            while "" in text_list:
                try:
                    text_list.remove("")
                except:
                    pass
            return text_list

    except Exception as e:
        print('{} threw an the following exception during EX21 parsing {}'.format(link, str(e)))

def tenk_parser(link): # not working
    try:
        html = urllib.request.urlopen(link).read()
        text_list = nltk.sent_tokenize(text_from_html(html))
        start = False
        stop = False
        info = ''
        for sent in text_list:
            if contain(sent,'PART I') and contain(sent,'Item 1'):
                start = True
            if contain(sent,'Item 1A') and contain(sent,'PART I'):
                stop = True
            if stop:
                return info
            if start:
                info += sent
    except Exception as e:
        print('{} threw an the following exception during 10K parsing {}'.format(link, str(e)))

def wikiParser(company):
    """

    """
    wiki_page = {}
    wiki_table = {}
    try:
        page = wiki.page(title = company)
    except:
        print("Reading the wiki page, {} was not possible".format(company))
        return (wiki_page, wiki_table)
    secs = page.sections
    for sec in secs:
        wiki_page[sec] = page.section(sec)
    # Do the wikipedia table
    link = page.url
    body = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(body, 'lxml')
    try:
        table = soup.find('table',{'class':'infobox vcard'})
        rows = table.find_all('tr')
        for row in rows:
            right = row.find_all('td')
            left = row.find_all('th')
            for head, elem in zip(left, right):
                filler = unicodedata.normalize("NFKD", head.get_text(strip=True))
                els = elem.find_all('li')
                if len(els) != 0:
                    temp_list = []
                    for el in els:
                        temp_list.append(unicodedata.normalize("NFKD",re.sub('\[[^()]*\]', "", el.get_text(strip=True))))
                    wiki_table[filler] = temp_list
                elif head.text == "Founded":
                    wiki_table[filler] = unicodedata.normalize("NFKD",elem.get_text(strip=True).split(";", 1)[0])
                elif elem.text != "":
                    wiki_table[filler] = unicodedata.normalize("NFKD",re.sub('\[[^()]*\]', "",elem.get_text(strip=True)))
    except:
        print("Wikipedia Table does not exist for {}".format(company))
    return (wiki_page, wiki_table)


def main():
    # pm = ProfileManager()
#    for company in pm:
#        print("Now getting information for {}".format(company['name']))
#        print(wiki_parser(company['name']))
     print(wikiParser("List of CAS numbers by chemical compound"))
#    (wiki_page, wiki_table) = wikiParser_new('Apple Inc')
#    print(wiki_page)
#    print(wiki_table)

if __name__ == "__main__" :
    main()
