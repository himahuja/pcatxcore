#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 15:27:52 2018

@author: alex
"""
import sys
sys.path.append("..")
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from PCATParser import *
import json, os, uuid, nltk, re, time
import numpy as np

class WebResourceManager(object):
    
    def __init__(self, rel_path=None):
        #read in the file
        self.rel_path = rel_path
        self.url_to_uuid = {}
#        if rel_path == None:
#            self.classifier = Doc2Vec.load("data/doc2vec_model")
#        else:
#            self.classifier = Doc2Vec.load(os.path.join(self.rel_path, "data/doc2vec_model"))
    

    def __iter__(self, instances=1, iam = 0):
        """
        An iterator function with the ability to be accessed by multiple instances at once in a safe way.

    
        Parameters
        ----------
        instances : int
            the number of instances using the iterator (default = 1)
        iam : int
            the current instance's assignment [0-*instances*) (default = 0)
    
        Returns
        -------
        dict
            A dictionary which is the profile if found, else None (Yields)
    
        """
        if instances == 1:
            for elem in self.url_to_uuid.values():
                yield self.get(elem)
        else:
            for i in range(len(self.url_to_uuid.values())):
                if i % instances == iam:
                    yield self.get(list(self.url_to_uuid.values().keys())[i])
        
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
        except Exception as e:
            print(self.rel_path)
            print("Error while getting {}: {}".format(key, str(e)))
        
    def get_corpus(self, process_all=False):
        corpus_list = []
        count = 0
        ps = PorterStemmer()
        lmtzr = WordNetLemmatizer()
        if not process_all:
            for item in self:
                try:
                    corpus_list.append(item['corpus'])
                except:
                    text = re.sub("[^A-Za-z0-9'-]+", ' ', re.sub('\S*@\S*\s?', "", item['text'])).lower().splitlines()
                    doc_list = []
                    for line in text:
                        words = line.split()
                        for word in words:
                            doc_list.append(ps.stem(lmtzr.lemmatize(word.strip())))
                    corpus_list.append(doc_list)
                    item['corpus'] = doc_list
                    file = open(os.path.join("../data/docs", item['id']+".json"), "w")
                    file.write(json.dumps(item, sort_keys=True, indent=4))
                    file.close()
                    count+=1
                    if (count % 1000 == 0):
                        if (count+1 != len(self)):
                            print("...{:2.2f}% done, processing document {} of {}".format(((count+1)/len(self))*100,count+1,len(self)))
        else:
            for item in self:
                text = re.sub("[^A-Za-z'-]+", ' ', re.sub('\S*@\S*\s?', "", item['text'])).lower().splitlines()
                doc_list = []
                for line in text:
                    words = line.split()
                    for word in words:
                        doc_list.append(ps.stem(lmtzr.lemmatize(word.strip())))
                corpus_list.append(doc_list)
                item['corpus'] = doc_list
                file = open(os.path.join("data/docs", item['id']+".json"), "w")
                file.write(json.dumps(item, sort_keys=True, indent=4))
                file.close()
                count+=1
                if (count % 1000 == 0):
                    if (count+1 != len(self)):
                        print("...{:2.2f}% done, processing document {} of {}".format(((count+1)/len(self))*100,count+1,len(self)))
        print("...100.00% done, processing document {} of {}".format(len(self),len(self)))
        return corpus_list
        
    def get_docs_by_sentence(self, instances=1, iam=0):
        for item in self.__iter__(instances=1, iam=0):
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    yield (sent_list[i], str(item['id'] + "_" + str(i)))
            except Exception as e:
                print("{} threw the following exception while yielding text: {}".format(item['id'], str(e)))
        
    def get_relevance_score(self, document):
        pass
    
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
        model = Doc2Vec.load("../data/doc2vec_model")
        for item in self:
            sent_list = nltk.sent_tokenize(item['text'])
            doc_tags = []
            tag2sent = {}
            tag2vec = {}
            for i in range(len(sent_list)):
                doc_tags.append(str(item['id'] + "_" + str(i)))
                tag2sent[item['id'] + "_" + str(i)] = i
                tag2vec[item['id'] + "_" + str(i)] = TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list(str(str(item['id'] + "_" + str(i)))))
            model.train(list(tag2vec.values()), total_examples=model.corpus_count, epochs=model.iter)
            tuples = []
            for doc_vec in doc_tags:
                tuples.append((model.docvecs.similarity('bad',doc_vec), tag2vec[doc_vec]))
            mergeSortTuples(tuples)
            temp_text = ""
            for i in range(len(doc_tags)//2):
                temp_text+=sent_list[tag2sent[vec]] + "\n"
            item['classifier'] = temp_text
            self.update_profile(item)
            
    
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

#    def train_classifier(self):
#        self.classifier.fit_transform(self.get_texts())

    def update_profile(self, item):
        if self.rel_path == None:
            file = open("data/docs/{}.json".format(item['id']), "w")
            file.write(json.dumps(item, sort_keys = True, indent = 4))
            file.close()
        else:
            file = open(os.path.join(self.rel_path, "data/docs/{}.json".format(item['id'])), "w")
            file.write(json.dumps(item, sort_keys = True, indent = 4)) 
            file.close()

def convert_to_corpus(doc):
    ps = PorterStemmer()  
    lmtzr = WordNetLemmatizer()
    text = re.sub("[^A-Za-z0-9'-]+", ' ', re.sub('\S*@\S*\s?', "", doc.lower())).splitlines()
    doc_list = []
    for line in text:
        words = line.split()
        for word in words:
            doc_list.append(ps.stem(lmtzr.lemmatize(word.strip())))
    return doc_list
            
def mergeSortTuples(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][0] < righthalf[j][0]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
            
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