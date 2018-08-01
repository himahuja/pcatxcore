#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 15:27:52 2018

@author: alex
"""
import sys
sys.path.append("..")
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim.models.doc2vec import TaggedDocument
from PCATParser import *
import json, os, uuid, nltk, re, time
import numpy as np

class WebResourceManager(object):
    
    def __init__(self, rel_path=None):
        #read in the file
        self.rel_path = rel_path
        self.url_to_uuid = {}
        self.classifier = TfidfVectorizer(stop_words='english')
        
    def __iter__(self):
        for elem in self.url_to_uuid.values():
            yield self.get(elem)
        
    #get the file with the UUID
    def __getitem__(self, key):
        try:
            if self.rel_path == None:
                file = open("data/docs/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/docs/{}.json").format(key))
            return json.loads(file.read())
        except:
            print("Error: Problem loading {}.json. Check that your rel_path is correct".format(key))
    
    def __len__(self):
        return len(self.url_to_uuid)
        
    def __repr__(self):
        return json.dumps(self.url_to_uuid, sort_keys = True, indent = 4)
        
    def __str__(self):
        return json.dumps(self.url_to_uuid, sort_keys = True, indent = 4)
        
    def absorb_file_manager(self, other_file_manager):
        for item in other_file_manager:
            if item['id'] not in self.url_to_uuid.values():
                self.url_to_uuid[item['url']] = item['id']
        
    def get(self, key):
        try:
            if self.rel_path == None:
                file = open("data/docs/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/docs/{}.json").format(key))
            return json.loads(file.read())
        except:
            pass
        
    def get_corpus(self, process_all=False):
        corpus_list = []
        count = 0
        stoplist = set(stopwords.words('english'))
        ps = PorterStemmer()  
        if not process_all:
            for item in self:
                try:
                    corpus_list.append(item['corpus'])
                except:
                    text = re.sub('[^A-Za-z]+', ' ', re.sub('\S*@\S*\s?', "", item['text'])).lower().splitlines()
                    doc_list = []
                    for line in text:
                        words = line.split()
                        for word in words:
                            doc_list.append(ps.stem(word.strip()))
                    doc_list = [word for word in doc_list if word not in stoplist]
                    sent_set = set(doc_list)
                    for word in sent_set:
                        if len(word) < 3:
                            while word in doc_list:
                                try:
                                    doc_list.remove(word)
                                except:
                                    pass
                    corpus_list.append(doc_list)
                    item['corpus'] = doc_list
                    file = open(os.path.join("../data/docs", item['id']+".json"), "w")
                    file.write(json.dumps(item, sort_keys=True, indent=4))
                    file.close()
                    if (count % 100 == 99):
                        if (count+1 != len(self)):
                            print("...{:2.2f}% done, processing document {} of {}".format(((count+1)/len(self))*100,count+1,len(self)))
                    count+=1
        else:
            for item in self:
                    text = re.sub('[^A-Za-z]+', ' ', re.sub('\S*@\S*\s?', "", item['text'])).lower().splitlines()
                    for line in text:
                        words = line.split()
                        for word in words:
                            doc_list.append(ps.stem(word.strip()))
                    doc_list = [word for word in doc_list if word not in stoplist]
                    sent_set = set(doc_list)
                    for word in sent_set:
                        if len(word) < 3:
                            while word in doc_list:
                                try:
                                    doc_list.remove(word)
                                except:
                                    pass
                    corpus_list.append(doc_list)
                    item['corpus'] = doc_list
                    file = open(os.path.join("data/docs", item['id']+".json"), "w")
                    file.write(json.dumps(item, sort_keys=True, indent=4))
                    file.close()
                    if (count % 100 == 99):
                        if (count+1 != len(self)):
                            print("...{:2.2f}% done, processing document {} of {}".format(((count+1)/len(self))*100,count+1,len(self)))
                    count+=1
        print("...100.00% done, processing document {} of {}".format(len(self),len(self)))
        return corpus_list
        
    def get_relevance_score(self, document):
        response = self.classifier.transform([document])
        feature_names = self.classifier.get_feature_names()
    
        score_dict = {}
        for col in response.nonzero()[1]:
            score_dict[feature_names[col]] = response[0,col]
    
        word_list = nltk.word_tokenize(document)
        total_score = 0
        count_keywords = 0
        for word in word_list:
            if word in score_dict:
                total_score += score_dict[word]
                count_keywords += 1
        if (count_keywords != 0):   
            score = total_score / count_keywords
        else:
            score = 0
        print(score)
        return score
    
    def get_TaggedDocuments(self):
        for file in self:
            #if query is a list this will throw errors, keep that in mind if the future
            yield TaggedDocument(words=file['corpus'], tags=list({file['id'], file['query']}))
    
    def get_texts(self):
        for file in self:
            yield file['text']
            
    def get_uuid(self, url):
        return(self.url_to_uuid[url])
        
    def load(self, file_name=None):
        file = ""
        if file_name == None:
            if self.rel_path == None:
                file = open("data/webresourcemanager.json", "r")
            else:
                file = open(os.path.join(self.rel_path, "data/webresourcemanager.json"), "r")
        else:
            file = open(file_name, "r")
        this = json.loads(file.read())
        file.close()
        self.url_to_uuid = this['url_to_uuid']
        try:
            self.rel_path = this['rel_path']
        except:
            pass
        
    def rank_by_relevance(self):
        for item in self:
            item['relevance_score'] = self.get_relevance_score(item['text'])
            file = open(os.path.join("data/docs", item['id']+".json"), "w")
            file.write(json.dumps(item, sort_keys=True, indent=4))
            file.close()
    
    #DOES NOT USE REL_PATH
    def read_in_from_directory(self, directory):
        for file in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, file)):
                try:
                    doc = json.loads(file.read())
                    self.url_to_uuid[doc['url']] = doc['id']
                except:
                    print("Error: File {} was not in the proper format to be tracked with WebResourceManager".format(file))
    
    def read_in_from_iterator(self, iterator_of_docs):
        for item in iterator_of_docs:
            item['id'] = str(self.string_to_uuid(item['url'])) + "--" + re.sub('[^A-Za-z0-9]+', '', item['url'])
            if len(item['id']) > 245:
                item['id'] = item['id'][:245]
            self.url_to_uuid[item['url']] = item['id']
            try:
                html = item['html']
                file = open(os.path.join("data/source", item['id'] +".html"), "w")
                file.write(html.decode('utf-8', 'ignore'))
                file.close()
                del item['html']
            except:
                pdf = item['pdf']
                file = open(os.path.join("data/source", item['id'] +".pdf"), "w")
                file.write(pdf.decode('utf-8', 'ignore'))
                file.close()
                del item['pdf']
            file = open(os.path.join("data/docs", item['id']+".json"), "w")
            file.write(json.dumps(item, sort_keys=True, indent=4))
            file.close()    
    
    def string_to_uuid(self, string):
        return uuid.uuid5(uuid.NAMESPACE_DNS, string)
    
    def save(self, file_name=None):
        this = { 'rel_path' : self.rel_path, 'url_to_uuid': self.url_to_uuid }
        if file_name == None:
            if self.rel_path == None:
                file = open("data/webresourcemanager.json", "w")
            else:
                file = open(os.path.join(self.rel_path, "data/webresourcemanager.json"), "w")
        else:
            file = open(file_name, "w")
        file.write(json.dumps(this, sort_keys = True, indent = 4))
        file.close

    def train_classifier(self):
        self.classifier.fit_transform(self.get_texts())

            
def insertionSort(arr):
 
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
 
        key = arr[i]['relevance_score']
 
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >=0 and key < arr[j]['relevance_score'] :
                arr[j+1]['relevance_score'] = arr[j]['relevance_score']
                j -= 1
        arr[j+1]['relevance_score'] = key
    return arr
            
def main():
    with open("../kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    wrm = WebResourceManager("..")
    wrm.load()
    url_list = ["https://www.sec.gov/Archives/edgar/data/1800/000104746914001176/a2218043z10-k.htm", "https://www.sec.gov/Archives/edgar/data/1800/000091205701006039/a2035109zex-21.txt"]
    for url in url_list:
        print(str(wrm.string_to_uuid(url)) + "--" + re.sub('[^A-Za-z0-9]+', '', url))
    
if __name__ == "__main__" :
    main()