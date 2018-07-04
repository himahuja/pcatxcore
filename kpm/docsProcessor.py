# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 22:17:12 2018

@author: alex
"""
from gensim.models.doc2vec import TaggedDocument
import codecs, os, re

class docsProcessor(object):
    
    def __init__(self, dirname):
        self.dirname = dirname
        self.sent_list = []
        for fname in os.listdir(self.dirname):
            file = codecs.open(os.path.join(self.dirname, fname), "r",encoding='utf-8', errors='ignore')
            text = file.read()
            text = re.sub('[^A-Za-z\']+', ' ', text)
            text = text.lower().splitlines()
            doc_list = []
            for line in text:
                words = line.split()
                for word in words:
                    doc_list.append(word.strip())
            self.sent_list.append(doc_list)
        self.filter_dict()
        print(self.sent_list[:100])
            
    def __iter__(self):
        for elem in self.sent_list:
            yield elem
                
    def __getitem__(self, key):
        return self.sent_list[key]
                
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
        stoplist = set('for a is com gov on it of are this the and to in edu'.split())
        self.sent_list = [[word for word in document if word not in stoplist] for document in self.sent_list]
        
    
    def to_TaggedDocument(self):
        docs = []
        for i in range(len(self.sent_list)):
            docs.append(TaggedDocument(words=self.sent_list[i], tags=[i]))
        return docs
        
    
