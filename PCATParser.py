#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, os, webbrowser, PyPDF2, nltk, pdfkit, re, wikipedia, json, sys, unicodedata, requests, time, signal
import wikipedia as wiki
sys.path.append
from knowledge_management.ProfileManager import *

#helper class for try_one
class Timeout(Exception): 
    pass 

def try_one(func, t, **kwargs):
    """
    Calls the function with the keyword arguments and after t seconds, interupts the call and moves on


    Parameters
    ----------
    func : function
        the function to be called
    t : int
        the number of seconds 
    **kwargs : keyword-arguments
        arguments you'd like to pass to func
    
    Returns
    -------
    func's return type

    """
    
    #helper function
    def timeout_handler(signum, frame):
        raise Timeout()

    old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
    signal.alarm(t) # triger alarm in t seconds
    parsed_page = None

    try: 
        t1=time.clock()
        parsed_page = func(**kwargs)
        t2=time.clock()

    except Timeout:
        print('{}() timed out after {} seconds'.format(func.__name__, t))
        return None
    finally:
        signal.signal(signal.SIGALRM, old_handler) 

    signal.alarm(0)
    return parsed_page

def tag_visible(element):
    """
    Determines if an HTML tag is visible


    Parameters
    ----------
    element : BeautifulSoup.element
        an HTML element
    
    Returns
    -------
    bool
        True if the element is visible, False else

    """
    if element.parent.name in ['[document]', 'head', 'style', 'script', 'title', 'header', 'meta', 'footer']:
        return False
    if isinstance(element, Comment):
        return False
    if element.name in ['header','footer','button','nav']:
        return False
    return True

def text_from_html(body):
    """
    Gets all of the visible text from the body of an HTML document


    Parameters
    ----------
    body : string
        the body of an HTML document
    
    Returns
    -------
    string
        the visible text in the body

    """
    soup = BeautifulSoup(body.decode("utf-8", "ignore"), 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)

def get_PDF_content(query_string, link):
    """
    Gets all of the text from a PDF document


    Parameters
    ----------
    query_string : string
        the query that generated the PDF document
    link : string
        the URL for the document
    
    Returns
    -------
    string
        the visible text in the PDF

    """
    #read the PDF from the web
    content=urllib.request.urlopen(link).read()
    #name file and write to tmp directory
    file_name = query_string+link
    file_name = re.sub('[^A-Za-z0-9]+', '', file_name)
    if len(file_name) > 100:
        file_name = file_name[:100]
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

def parse_single_page(link, query_string = "test"):
    """
    Gets all of the text from web page


    Parameters
    ----------
    link : string
        the URL for the document
    query_string : string
        the generating query, default is "test"
    
    Returns
    -------
    tuple (bytes, string)
        the source code (HTML/PDF) of the web page and the visible text

    """
    if link[-4:] != '.pdf':
            try:
                html = urllib.request.urlopen(link).read()
                print(type(html))
                return (html, bytes(text_from_html(html), 'utf-8').decode('utf-8', 'ignore'))
            except Exception as e:
                print(link + " threw the following exception " + str(e))
    else:
            try:
                html = urllib.request.urlopen(link).read()
                return (html, get_PDF_content(query_string, link))
            except Exception as e:
                print(link + " threw the following exception " + str(e))

def parser_iter(query_string, linkList):
    """
    Parses the URLs in linkList using a timeout of 60 seconds on each page (a la try_one) and yields them as dictionaries.


    Parameters
    ----------
    query_string : string
        the generating query, default is "test"
    linkList : list of strings
        list of URLs for the documents you would like to parse
    
    Returns
    -------
    iterator of dicts
        * dict['text'] (string) : the visible text on the web page
        * dict['html'] (bytes) : the HTML code of the page (if it is HTML based)
        * dict['pdf'] (bytes) : the PDF code of the page (if it is PDF based)

    """
    for link in linkList:
        print("...{:.2f}% done, processing link {}: {}".format(((linkList.index(link)+1)/len(linkList))*100,linkList.index(link), link))
        doc = {'url' : link, 'query': query_string }
        parsed_page = try_one(parse_single_page, 60, link=link, query_string=query_string)
        if parsed_page != None:
            if link[-4:] != '.pdf':
                doc['html'] = parsed_page[0]
                doc['text'] = parsed_page[1]
            else:
                doc['pdf'] = parsed_page[0]
                doc['text'] = parsed_page[1]
            yield doc

def contain(sent,word_list):
    #you can figure it out
    for i in range(len(word_list)):
        if word_list[i] in sent:
            return True
    return False

def eightk_parser(link):
    """
    Parses an SEC document known as an 8-K


    Parameters
    ----------
    link : string
        the URL for the 8-K
    
    Returns
    -------
    string
        the important text for the 8-K

    """
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
    """
    Parses an SEC document known as an EX-21


    Parameters
    ----------
    link : string
        the URL for the EX-21
    
    Returns
    -------
    list of strings
        the subsidiaries in the company listed in the EX-21

    """
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

def tenk_parser(link):
    """
    Parses an SEC document known as an 10-K


    Parameters
    ----------
    link : string
        the URL for the 10-K
    
    Returns
    -------
    string
        the important information in the 10-K

    """
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
        Search the Wikipedia page for a company and get wikipedia infobox
        together with all other contents
 
        Parameters
        ----------
        company: str
            the company you would like to query Wikipedia for
        
        Returns
        -------
        tuple
            dict
                a dictionary of all other contents on wikipedia
            dict
                a dictionary of wikipedia infobox
            str
                page title
            str
                page url
            beautifulsoup.table
                wikipedia infobox HTML
        
    """ 
    wiki_page = {}
    wiki_table = {}
    try:
        page = wiki.page(title = company)
    except:
        print("Reading the wiki page, {} was not possible".format(company))
        return (wiki_page, wiki_table, "", "", "<ul></ul>")
    secs = page.sections
    for sec in secs:
        wiki_page[sec] = page.section(sec)
    # Do the wikipedia table
    link = page.url
    body = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(body, 'lxml')
    title = soup.find('title')
    if title != None:
        title = str(title).replace("<title>", "").replace("</title>", "").replace("- Wikipedia", "").strip()
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
    return (wiki_page, wiki_table, title, link, table)


def main():
    # pm = ProfileManager()
#    for company in pm:
#        print("Now getting information for {}".format(company['name']))
#        print(wiki_parser(company['name']))
     parse_single_page("http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0128193")
#    (wiki_page, wiki_table) = wikiParser_new('Apple Inc')
#    print(wiki_page)
#    print(wiki_table)

if __name__ == "__main__" :
    main()
