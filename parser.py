from bs4 import BeautifulSoup
# used for parsing the HTML contents on webscript
import urllib.request
# to open up the URL to access the webpage
import pandas as pd
# creates a dataframe structure that is efficent than CSV or SQLlite in Python
import os
# for getting directory locations




def newsparser(url):
    """
    Parses the URL passed as an argument and returns a Pandas DF. It also saves a CSV file.
    Keyword arguments:
    url: It is the URL of the webpage it's going to crawl.
    """

    page = urllib.request.urlopen(url) #opens the URL page
    content = page.read() # reads the content of the page
    soup = BeautifulSoup(content, 'html.parser')
    #creates the soup out of the content, so the attributes can be processed
    heads = soup.find_all('span', {'itemprop': 'headline'})

    """
    Takes the input url for processing and returns a csv of the following forrmat:
    ['headline', 'article', 'author', 'date', 'source', 'image']
    where image contains the whole image source
    source contains the articles where the inshorts article is referenced from.
    Returns a PANDAS dataframe
    """

# neighbourhood words
def search(text,n):
    """Searches for text, and retrieves n words either side of the text, which are retuned seperatly"""
    word = r"\W*([\w]+)"
    groups = re.search(r'{}\W*{}{}'.format(word*n,'place',word*n), text).groups()
    return groups[:n],groups[n:]

    articles = soup.find_all('div', {'itemprop': 'articleBody'})
    authors = soup.find_all('span', {'class': 'author'})
    dates = soup.find_all('span', {'clas':'date'})
    sources = soup.find_all('a', {'class':'source'})
    images = soup.find_all('div', {'class': 'news-card-image'})
    data = zip(heads, articles, authors, dates, sources, images)
    stored = []
    cols = ['headline', 'articleBody', 'author', 'date', 'source', 'image']
    for head, article, author, date, source, image in data:
        stored.append([head.get_text(), article.get_text(), author.get_text(), date.get_text(), source['href'], image])
    df = pd.DataFrame(stored, columns = cols)
    return df

def newsparser2(url):
        """
        Takes the input url for processing and returns a csv of the following format:
        text = ['headline' + 'article']
        """
        page = urllib.request.urlopen(url)
        content = page.read()
        soup = BeautifulSoup(content, 'html.parser')
        heads = soup.find_all('span', {'itemprop': 'headline'})
        stored = []
        for head in heads:
            stored.append(head.get_text())
        return stored

if __name__ == "__main__":
    # sample URL for testing.
    url = 'https://news.thomasnet.com/imt/2000/11/13/changing_the_im'



# df = newsparser('file:///Applications/XAMPP/xamppfiles/htdocs/NIS/AI-to-News-in-Shorts/data/7_inshorts.html')
# df.to_csv('data/7.csv')
