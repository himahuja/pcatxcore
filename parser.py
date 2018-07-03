from bs4 import BeautifulSoup
import urllib.request

def tag_visible(element):
    #this is to determine whether the content in a tag is visible on a webpage
    if element.parent.name in ['head', 'style', 'script', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    #only extract the visible and relevant content that we care
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def parser(linkList):
    #this is to parse a list of links to text files individually
    for link in linkList:
        html = urllib.request.urlopen(link).read()
        file_name = "page"+str(linkList.index(link))+".txt"
        text_file = open(file_name, "w")
        text_file.write(text_from_html(html))
        text_file.close()
