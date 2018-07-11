#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 22:17:12 2018

@author: alex
"""
import sys
sys.path.append("..")
from gensim.models.doc2vec import TaggedDocument
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from WebResourceManager import *
import codecs, json, pickle, os, re

class corpusBuilder(object):
    def __init__(self, dirname=None, file_manager=None):
        self.dirname = dirname
        self.sent_list = []
        self.tag_list = []
        if (dirname != None):
            for fname in os.listdir(self.dirname):
                file = codecs.open(os.path.join(self.dirname, fname), "r",encoding='utf-8', errors='ignore')
                text = file.read()
                self.tag_list.append(fname)
                text = re.sub('\S*@\S*\s?', "", text)
                text = re.sub('[^A-Za-z]+', ' ', text)
                text = text.lower().splitlines()
                doc_list = []
                for line in text:
                    words = line.split()
                    for word in words:
                        doc_list.append(word.strip())
                self.sent_list.append(doc_list)
                if (os.listdir(self.dirname).index(fname) % 100 == 99):
                    if (os.listdir(self.dirname).index(fname)+1 != len(os.listdir(self.dirname))):
                        print("...{:2.2f}% done, processing document {} of {}".format(((os.listdir(self.dirname).index(fname)+1)/len(os.listdir(self.dirname)))*100,os.listdir(self.dirname).index(fname)+1,len(os.listdir(self.dirname))))
            print("...100.00% done, processing document {} of {}".format(len(os.listdir(self.dirname)),len(os.listdir(self.dirname))))
            print("...filtering the dictionary...")
            self.filter_dict()
        if (file_manager != None):
            count = 0
            for file in file_manager:
                text = file['text']
                self.tag_list.append([file['query'], file['id']])
                text = re.sub('\S*@\S*\s?', "", text)
                text = re.sub('[^A-Za-z]+', ' ', text)
                text = text.lower().splitlines()
                doc_list = []
                for line in text:
                    words = line.split()
                    for word in words:
                        doc_list.append(word.strip())
                self.sent_list.append(doc_list)
                if (count % 100 == 99):
                    if (count+1 != len(file_manager)):
                        print("...{:2.2f}% done, processing document {} of {}".format(((count+1)/len(file_manager))*100,count+1,len(file_manager)))
                count+=1
            print("...100.00% done, processing document {} of {}".format(len(file_manager),len(file_manager)))
            
            print("...filtering the dictionary...")
            self.filter_dict()
                
            
    def __getitem__(self, key):
        return self.sent_list[key]
            
    def __iter__(self):
        for elem in self.sent_list:
            yield elem
                
    def __len__(self):
        return(len(self.sent_list))
        
    def __repr__(self):
        string = "[ "
        for elem in self.sent_list:
            string+="'{}' ".format(elem)
        string+="]"
        return string
        
    def __str__(self):
        string = "[ "
        for elem in self.sent_list:
            string+="'{}'".format(elem)
        string+="]"
        return string
        
    def filter_dict(self):
        stoplist = set(stopwords.words('english'))
        self.sent_list = [[word for word in document if word not in stoplist] for document in self.sent_list]
        ps = PorterStemmer()        
        for i in range(len(self.sent_list)):
            sent_set = set(self.sent_list[i])
            for word in sent_set:
                if len(word) < 3:
                    while(word in self.sent_list[i]):
                        try:
                            self.sent_list[i].remove(word)
                        except:
                            pass
            for j in range(len(self.sent_list[i])):
                self.sent_list[i][j] = ps.stem(self.sent_list[i][j])
            if (i % 100 == 99):
                    if (i+1 != len(self.sent_list)):
                            print("...{:2.2f}% done, filtering document {} of {}".format((i+1)/len(self.sent_list)*100,i+1,len(self.sent_list)))
        print("...100.00% done, filtering document {} of {}".format(len(self.sent_list),len(self.sent_list)))
        
    def load(self, dir_name=None):
        if dir_name != None:
            with open("{}/corpus.json".format(dir_name), "r") as file:
                this = json.loads(file.read())
        else:
            with open("data/corpus.json", "r") as file:
                this = json.loads(file.read())
        self.sent_list = this['sent_list']
        self.tag_list = this['tag_list']
               
    def save(self, dir_name=None):
        this = { 'sent_list': self.sent_list, 'tag_list': self.tag_list }
        if dir_name != None:
            file = open('{}/corpus.json'.format(dir_name), 'w')
            file.write(json.dumps(this, sort_keys = True, indent = 4))
            file.close()
        else:
            file = open('data/corpus.json', 'w')
            file.write(json.dumps(this, sort_keys = True, indent = 4))
            file.close()
    
    def to_TaggedDocument(self):
        docs = []
        for i in range(len(self.sent_list)):
            docs.append(TaggedDocument(words=self.sent_list[i], tags=self.tag_list[i]))
        return docs

def main():
    fm = WebResourceManager(rel_path="../")
    fm.load()
    docs = corpusBuilder(file_manager=fm)
    docs.save()
    
if __name__ == "__main__" :
    main()
        
    
