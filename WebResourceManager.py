#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 15:27:52 2018

@author: alex
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from PCATParser import *
import json, os, uuid
import numpy as np
import json, nltk, os, re, time, uuid

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
        return len(self.url_to_uuid.values())
        
    def __repr__(self):
        this = { 'url_to_uuid': self.url_to_uuid }
        return json.dumps(this, sort_keys = True, indent = 4)
        
    def __str__(self):
        this = { 'url_to_uuid': self.url_to_uuid }
        return json.dumps(this, sort_keys = True, indent = 4)
        
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
        return score
    
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

            
            
def main():
    with open("kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    wrm = WebResourceManager()
    wrm.load()
    print(len(wrm))
    wrm.train_classifier()
    wrm.rank_by_relevance()
    
if __name__ == "__main__" :
    main()