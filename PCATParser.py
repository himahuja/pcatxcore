#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, os, webbrowser, PyPDF2, nltk, os, pdfkit
import wikipedia

def tag_visible(element):
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

def get_PDF_content(query_string, link, linkList):
    #download pdf file ,from web
    content=urllib.request.urlopen(link).read()
    file_name = query_string+str(linkList.index(link))+".pdf"
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
                content = get_PDF_content(query_string, link, linkList)
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

def wiki_parser(company):
    link = wikipedia.page(company).url
    body = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(body, 'lxml')
    table = soup.findAll('table',{'class':'infobox vcard'})
    info_dict = {}
    for t in table:
        row = t.findAll('tr')
        for r in row:
            head = r.findAll('th')
            division = r.findAll('td')
            for h,d in zip(head,division):
                desc = h.get_text().strip('\n')
                detail = d.get_text().strip('\n')
                info_dict[desc] = detail
    return info_dict

def contain(sent,word):
    if word in sent:
        return True
    return False

def tenk_parser(link):       
    try:
        html = urllib.request.urlopen(link).read()
        text_list = nltk.sent_tokenize(text_from_html(html))
        start = False
        stop = False
        info = ''
        for sent in text:
            if contain(sent,'PART I') and contain(sent,'Item 1'):
                start = True
            if contain(sent,'Item 1A') and contain(sent,'PART I'):
                stop = True
            if stop:
                return info
            if start:
                info += sent
    except:
        print('exception when parsing 10k, returning an empty string')
        return ''
    
def main():
    with open("kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    parser("test", content)


if __name__ == "__main__" :
    main()
