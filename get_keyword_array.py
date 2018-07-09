from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from FileManager import *

# FileManager TODO: open, read documents in a folder and build a list
# document_list = []
def get_keyword_array(document_list, n = 100):
    tfidf = TfidfVectorizer(stop_words='english')
    tfs = tfidf.fit_transform(document_list)
    response = tfidf.transform(document_list)
    
    feature_names = tfidf.get_feature_names()
    feature_array = np.array(feature_names)
    tfidf_sorting = np.argsort(response.toarray()).flatten()[::-1]

    top_keyword_array = feature_array[tfidf_sorting][:n]
    
    return top_keyword_array

# FileManager TODO: iterate through all documents and call lable
def label(document, top_keyword_array):
    for keyword in top_keyword_array:
        if keyword in document:
            return '1'
        else:
            return '0' 

def main():
    fm = FileManager()
    fm.load()
    content = []
    for file in fm:
        content.append(file['text'])
    content = [x.strip() for x in content]
    print(get_keyword_array(content))
    
if __name__ == "__main__" :
    main()