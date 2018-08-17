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
from sklearn.feature_extraction.text import TfidfVectorizer
from PCATParser import *
import json, os, uuid, nltk, re, time
import numpy as np

class WebResourceManager(object):
    
    def __init__(self, rel_path=None):
        #read in the file
        self.rel_path = rel_path
        self.url_to_uuid = {}
        self.classifier = TfidfVectorizer(stop_words='english')
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
            profile = file.read()
            file.close()
            return json.loads(profile)
        except Exception as e:
            pass
#            print("Error while getting {} with rel_path set to {}: {}".format(key, self.rel_path, str(e)))
    
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
    
    def clean_resource(self):
        for item in self:
            try:
                del item['tfidf_classifier']
            except Exception as e:
                print(str(e))
            try:
                del item['ss_classifier']
            except Exception as e:
                print(str(e))
            try:
                self.update_profile(item)
            except:
                pass
        
    def get(self, key):
        try:
            if self.rel_path == None:
                file = open("data/docs/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/docs/{}.json").format(key))
            profile = file.read()
            file.close()
            return json.loads(profile)
        except Exception as e:
            pass
#            print("Error while getting {} with rel_path set to {}: {}".format(key, self.rel_path, str(e)))
        
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
        
    def get_docs_by_sentence(self):
        for item in self:
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    yield sent_list[i]
            except Exception as e:
                print("{} threw the following exception while yielding text: {}".format(item['id'], str(e)))
        
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
    
    def get_TaggedDocuments(self):
        doc_count = -1
        for item in self:
            doc_count+=1
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    yield TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list("{:06d}{:04d}".format(doc_count, i)))
            except (KeyError, TypeError) as e:
                print(str(e))
                doc_list-=1
    
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
        doc_count = 0
        doc_list = []
        for item in self:
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    doc_list.append(TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list("{}{:04d}".format(item['id'], i))))
                doc_count+=1
            except (KeyError, TypeError) as e:
                print(str(e))
        model.train(doc_list, total_examples=model.corpus_count, epochs=model.iter)
        model.save("../data/doc2vec_model")
        doc_count = 0
        for item in self:
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                doc_tags = []
                tag2sent = {}
                for i in range(len(sent_list)):
                    tag = "{:06d}{:04d}".format(doc_count, i)
                    doc_tags.append(tag)
                    tag2sent[tag] = sent_list[i]
                tuples = []
                for doc_vec in doc_tags:
                    try:
                        tuples.append((model.docvecs.similarity('bad',doc_vec), tag2sent[doc_vec]))
                    except KeyError as e:
                        pass
#                        print("Error in wrm:rank_by_relevance \n The following error was thrown while attempting to get the Doc2Vec similarity of {}: \n {}".format(item['id'], str(e)))
                print(tuples)
                mergeSortTuples(tuples)
                print(tuples)
                temp_text = ""
                for i in range(len(tuples)//2):
                    temp_text+=tuples[i][1] + "\n"
                item['ss_classifier'] = temp_text
                
                self.train_classifier()
                tfidf_tuples = []
                for i in range(len(sent_list)):
                    tfidf_tuples.append((self.get_relevance_score(sent_list[i]), sent_list[i]))
                mergeSortTuples(tuples)
                for i in range(len(tuples)//2):
                    temp_text+=tuples[i][1] + "\n"
                item['tfidf_classifier'] = temp_text
                
                self.update_profile(item)
                print("Finished item {}".format(item['id']))
                doc_count+=1
            except (KeyError, TypeError) as e:
                print("Error in wrm:rank_by_relevance \n {}".format(str(e)))
            
    
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
            if len(item['id']) > 100:
                item['id'] = item['id'][:100]
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

    def update_profile(self, item):
        if self.rel_path == None:
            file = open("data/docs/{}.json".format(item['id']), "w")
            file.seek(0)
            file.write(json.dumps(item, sort_keys = True, indent = 4))
            file.truncate()
            file.close()
        else:
            file = open(os.path.join(self.rel_path, "data/docs/{}.json".format(item['id'])), "w")
            file.seek(0)
            file.write(json.dumps(item, sort_keys = True, indent = 4))
            file.truncate()
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

        mergeSortTuples(lefthalf)
        mergeSortTuples(righthalf)

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
    for file in os.listdir("../data/webresourcemanagers"):
        wrm = WebResourceManager(rel_path = "..")
        wrm.load(os.path.join("../data/webresourcemanagers", file))
        wrm.rel_path=".."
        wrm.clean_resource()
    
if __name__ == "__main__" :
    main()