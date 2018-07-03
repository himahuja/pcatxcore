#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from urllib.request import urlopen
import os
import webbrowser
import PyPDF2
import nltk, os, urllib.request


def tag_visible(element):
    if element.parent.name in ['[document]', 'head', 'style', 'script', 'title', 'header', 'meta', 'footer']:
        return False
    if isinstance(element, Comment):
        return False
    if element.name in ['header','footer','button','nav']:
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def get_PDF_content(link, linkList):
    #download pdf file ,from web
    content=urlopen(link).read()
    file_name = "pdf"+str(linkList.index(link))+".pdf"
    fout=open(os.path.join("data/source", file_name), "wb")
    fout.write(content)
    fout.close()

    #convert PDF to text
    content = ""
    #load PDF into PyPDF2
    pdf = PyPDF2.PdfFileReader(file_name)
    #iterate pages
    for i in range(pdf.getNumPages()):
    #extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
        content = " ".join(content.replace("\xa0", " ").strip().split())
    return content

def parser(linkList):
    for link in linkList:
        if link[-4:] != '.pdf':
            try:
                html = urllib.request.urlopen(link).read()
                file_name = "page"+str(linkList.index(link))+".txt"
                text_list = nltk.sent_tokenize(text_from_html(html))
                text_file = open(os.path.join("data/sentences", file_name), "w")
                for i in range(len(text_list)):
                    text_file.write(text_list[i].strip() + "\n")
                text_file.close()
            except:
                pass
        else:
            try:
                content = get_PDF_content(link, linkList)
                file_name = "page"+str(linkList.index(link))+".txt"
                text_list = nltk.sent_tokenize(text_from_html(html))
                text_file = open(os.path.join("data/sentences", file_name), "w")
                for i in range(len(text_list)):
                    text_file.write(text_list[i].strip() + "\n")
                text_file.close()
            except:
                pass
        print("...{:.2f}% done, processing link {}".format(((linkList.index(link)+1)/len(linkList))*100,linkList.index(link)))

def main():
    with open("KPM/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    parser(content)


if __name__ == "__main__" :
    main()
