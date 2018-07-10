#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 15:27:52 2018

@author: alex
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from PCATParser import *
import numpy as np
import json, nltk, os, time, uuid

class FileManager(object):
    
    def __init__(self, rel_path=None):
        #read in the file
        self.rel_path = rel_path
        self.uuid_to_url = {}
        self.url_to_uuid = {}
        self.classifier = TfidfVectorizer(stop_words='english')
        
    def __iter__(self):
        for elem in self.uuid_to_url.keys():
            yield self.get(elem)
        
    #get the file with the UUID
    def __getitem__(self, key):
        try:
            if self.rel_path == None:
                file = open("data/sentences/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/sentences/{}.json").format(key))
            return json.loads(file.read())
        except:
            return {}
    
    def __len__(self):
        return len(self.uuid_to_url.keys())
        
    def __repr__(self):
        this = { 'uuid_to_url': self.uuid_to_url, 'url_to_uuid': self.url_to_uuid }
        return json.dumps(this, sort_keys = True, indent = 4)
        
    def __str__(self):
        this = { 'uuid_to_url': self.uuid_to_url, 'url_to_uuid': self.url_to_uuid }
        return json.dumps(this, sort_keys = True, indent = 4)
        
    def absorb_file_manager(self, other_file_manager):
        for item in other_file_manager:
            if item['id'] not in self.uuid_to_url.keys():
                self.uuid_to_url[item['id']] = item['url']
                self.url_to_uuid[item['url']] = item['id']
        
    def get(self, key):
        try:
            if self.rel_path == None:
                file = open("data/sentences/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/sentences/{}.json").format(key))
            return json.loads(file.read())
        except:
            return {}
        
    def load(self, file_name=None):
        file = ""
        if file_name == None:
            if self.rel_path == None:
                file = open("data/filemanager.json", "r")
            else:
                file = open(os.path.join(self.rel_path, "data/filemanager.json"), "r")
        else:
            file = open(file_name, "r")
        this = json.loads(file.read())
        file.close()
        self.uuid_to_url = this['uuid_to_url']
        self.url_to_uuid = this['url_to_uuid']
        try:
            self.classifier = this['classifier']
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
        print(score)
        return score
    
    def get_texts(self):
        for file in self:
            yield file['text']
    
    #DOES NOT USE REL_PATH
    def read_in_from_directory(self, directory):
        for file in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, file):
                try:
                    doc = json.loads(file.read())
                    self.uuid_to_url[doc['id']] = doc['url']
                    self.url_to_uuid[doc['url']] = doc['id']
                except:
                    print("File {} was not in the proper format to be tracked with FileManager".format(file))
    
    def read_in_from_iterator(self, iterator_of_docs):
        for item in iterator_of_docs:
            item['id'] = str(self.string_to_uuid(item['url']))
            self.uuid_to_url[item['id']] = item['url']
            self.url_to_uuid[item['url']] = item['id']
            item['time'] = time.time()
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
            file = open(os.path.join("data/sentences", item['id']+".json"), "w")
            file.write(json.dumps(item, sort_keys=True, indent=4))
            file.close()    
    
    def rank_by_relevance(self):
        for file in self:
            file['relevance_score'] = self.get_relevance_score(file['text'])
    
    def string_to_uuid(self, string):
        return uuid.uuid5(uuid.NAMESPACE_DNS, string)
    
    def save(self, file_name=None):
        this = { 'uuid_to_url': self.uuid_to_url, 'url_to_uuid': self.url_to_uuid, 'classifier' : self.classifier }
        if file_name == None:
            if self.rel_path == None:
                file = open("data/filemanager.json", "w")
            else:
                file = open(os.path.join(self.rel_path, "data/filemanager.json"), "w")
        else:
            file = open(file_name, "w")
        file.write(json.dumps(this, sort_keys = True, indent = 4))
        file.close
        
    def train_classifier(self):
        self.classifier.fit_transform(self.get_texts())
        
    def url_to_uuid(self, url):
        return self.url_to_uuid[url]
    
    def uuid_to_url(self, key):
        return self.uuid_to_url[key]
            
        
def main():
    with open("kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    fm = FileManager()
    fm.load()
    fm.train_classifier()
    fm.rank_by_relevance()
    fm.save()
    
if __name__ == "__main__" :
    main()