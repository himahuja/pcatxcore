from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from urllib.request import urlopen
import os
import webbrowser
import PyPDF2

 
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

def get_PDF_content(url):
    #download pdf file from web
    content=urlopen(url).read()
    file_name = "pdf"+str(linkList.index(link))+".pdf"
    fout=open(file_name, "wb")
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
            html = urllib.request.urlopen(link).read()
            file_name = "page"+str(linkList.index(link))+".txt"
            text_file = open(file_name, "w")
            text_file.write(text_from_html(html))
            text_file.close()
        else:
            content = get_PDF_content(link)
            file_name = "page"+str(linkList.index(link))+".txt"
            text_file = open(file_name, "w")
            text_file.write(content)
            text_file.close()  

linkList = ['https://www.wired.com/2009/03/greenpeace-faul/','https://www.dtsc.ca.gov/PollutionPrevention/upload/SemiconductorReport.pdf']
parser(linkList)
