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
        """
        Constructor

    
        Parameters
        ----------
        rel_path : string
            the relative path to the parent directory of "data" holding the WebResourceManager data
    
        Returns
        -------
        None
    
        """
        self.rel_path = rel_path
        self.url_to_uuid = {}
    

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
        iterator of dicts
            A dictionary which is the profile if found, else None
    
        """
        if instances == 1:
            for elem in self.url_to_uuid.values():
                yield self.get(elem)
        else:
            for i in range(len(self.url_to_uuid.values())):
                if i % instances == iam:
                    yield self.get(list(self.url_to_uuid.values().keys())[i])
        
    def __getitem__(self, key):
        """
        Loads and returns the web resource profile specified by key

    
        Parameters
        ----------
        key : string
            universally unique identifier (UUID) for a web resource being tracked by the Web Resource Manager instance
    
        Returns
        -------
        dict
            A dictionary which is the profile if found, else None
    
        """
        try:
            if self.rel_path == None:
                file = open("data/webresourcemanager/docs/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/webresourcemanager/docs/{}.json").format(key))
            profile = file.read()
            file.close()
            return json.loads(profile)
        except Exception as e:
            print("Error while getting {} with rel_path set to {}: {}".format(key, self.rel_path, str(e)))
    
    def __len__(self):
        """
        Returns the number of web resources being tracked by the instance
        
        
        Returns
        -------
        int
            number of web resources in the instance
    
        """
        return len(self.url_to_uuid)
        
    def __repr__(self):
        '''
        Returns a sorted and indented dictionary representation of URLs to UUIDs of the web resources contained.
        
        
        Returns
        -------
        string
            a sorted and indented dictionary representation of URLs to UUIDs of the web resources map
        '''
        return str(json.dumps(self.url_to_uuid, sort_keys = True, indent = 4))
        
    def __str__(self):
        '''
        Returns a sorted and indented dictionary representation of URLs to UUIDs of the web resources contained.
        
        
        Returns
        -------
        string
            a sorted and indented dictionary representation of URLs to UUIDs of the web resources map
        '''
        return str(json.dumps(self.url_to_uuid, sort_keys = True, indent = 4))
        
    def absorb_file_manager(self, other_wrm):
        """
        This object starts tracking all of the files in the other_file_manager by adding the files to its dictionary. other_file_manager and its files are not altered in any way.

    
        Parameters
        ----------
        other_wrm : string
            another WebResourceManager object
    
        Returns
        -------
        None
    
        """
        for item in other_wrm:
            try:
                if item['id'] not in self.url_to_uuid.values():
                    self.url_to_uuid[item['url']] = item['id']
            except:
                pass
        
    def get(self, key):
        """
        Loads and returns the web resource profile specified by key

    
        Parameters
        ----------
        key : string
            universally unique identifier (UUID) for a web resource being tracked by the Web Resource Manager instance
    
        Returns
        -------
        dict
            A dictionary which is the profile if found, else None
    
        """
        try:
            if self.rel_path == None:
                file = open("data/webresourcemanager/docs/{}.json".format(key))
            else:
                file = open(os.path.join(self.rel_path, "data/webresourcemanager/docs/{}.json").format(key))
            profile = file.read()
            file.close()
            return json.loads(profile)
        except Exception as e:
            print("Error while getting {} with rel_path set to {}: {}".format(key, self.rel_path, str(e)))
        
    def get_corpus(self, process_all=False):
        """
        Converts the text to a format more suitable for NLP processing
        
        The function decodes using the "UTF-8" codec, ignoring errors, uses regular expressions to remove email addresses and all non-alpha-numeric characters except ' and -, then lemmatizes and stems using NLTK's WordNetLemmatizer and PorterStemmer respectively.

    
        Parameters
        ----------
        process_all : bool
            indicates whether you would like to use the 'corpus' fields of previously processed web resources (False) or reprocess all of the resources (True)
            
        Returns
        -------
        None
    
        """
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
                    file = open(os.path.join("../data/webresourcemanager/docs", item['id']+".json"), "w")
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
                file = open(os.path.join("data/webresourcemanager/docs", item['id']+".json"), "w")
                file.write(json.dumps(item, sort_keys=True, indent=4))
                file.close()
                count+=1
                if (count % 1000 == 0):
                    if (count+1 != len(self)):
                        print("...{:2.2f}% done, processing document {} of {}".format(((count+1)/len(self))*100,count+1,len(self)))
        print("...100.00% done, processing document {} of {}".format(len(self),len(self)))
        return corpus_list
        
    def get_docs_by_sentence(self):
        """
        Yields the contained web resources by sentence using nltk.sent_tokenize


        Returns
        -------
        list of strings (Yields)
            the sentences in the contained web resources
    
        """
        for item in self:
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    yield sent_list[i]
            except Exception as e:
                print("{} threw the following exception while yielding text: {}".format(item['id'], str(e)))
    
    def get_TaggedDocuments(self):
        """
        Yields TaggedDocuments using the contained web resources by sentence using nltk.sent_tokenize and convert_to_corpus

 
        Returns
        -------
        list of gensim.models.doc2vec.TaggedDocument (Yields)
            the TaggedDocument representations of the contained web resource sentences
    
        """
        for item in self:
            try:
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    yield TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list("{}{:04d}".format(item['id'], i)))
            except (KeyError, TypeError) as e:
                print(str(e))
    
    def get_texts(self):
        """
        Yields `text' fields of the web resources contained

 
        Returns
        -------
        iterator of strings (Yields)
            the `text' fields of the web resources contained
    
        """
        for file in self:
            yield file['text']
            
    def get_uuid(self, url):
        """
        Returns the UUID (Universally Unique Identifier) for the URL (Uniform Resource Locator)

    
        Parameters
        ----------
        url : string
            url of the web resource of interest
            
        Returns
        -------
        string
            the UUID (Universally Unique Identifier) of the web resource
    
        """
        return(self.url_to_uuid[url])
        
    def load(self, file_name=None):
        """
        Loads the saved WebResourceManager data into this instance (overwritting it). NOTE: this will overwrite rel_path IF the saved instance had rel_path set.

    
        Parameters
        ----------
        file_name : string
            path to the file you would like to load (USES REL_PATH IF SET)
            
        Returns
        -------
        None
    
        """
        file = ""
        if file_name == None:
            if self.rel_path == None:
                file = open("data/webresourcemanager/webresourcemanager.json", "r")
            else:
                file = open(os.path.join(self.rel_path, "data/webresourcemanager/webresourcemanager.json"), "r")
        else:
            file = open(file_name, "r")
        this = json.loads(file.read())
        file.close()
        self.url_to_uuid = this['url_to_uuid']
        try:
            self.rel_path = this['rel_path']
        except:
            pass
            
    
    #DOES NOT USE REL_PATH
    def read_in_from_directory(self, directory):
        """
        Reads in the web resource profiles in the directory and begins tracking them by adding them to url_to_uuid

    
        Parameters
        ----------
        directory : string
            path to the directory where you'd like to load files from (DOES NOT USE REL_PATH)
            
        Returns
        -------
        None
    
        """
        for file in os.listdir(directory):
            if not os.path.isdir(os.path.join(directory, file)):
                try:
                    doc = json.loads(file.read())
                    self.url_to_uuid[doc['url']] = doc['id']
                except:
                    print("Error: File {} was not in the proper format to be tracked with WebResourceManager".format(file))
    
    def read_in_from_iterator(self, iterator_of_docs):
        """
        Adds web resources from the Parser to the Web Resource Manager instance using an iterator

    
        Parameters
        ----------
        iterator_of_docs : iterator of dicts
            iterator of dictionaries containing a 'url', 'text', and either 'html' or 'pdf' field
            
        Returns
        -------
        None
    
        """
        for item in iterator_of_docs:
            item['id'] = str(self.string_to_uuid(item['url'])) + "--" + re.sub('[^A-Za-z0-9]+', '', item['url'])
            if len(item['id']) > 100:
                item['id'] = item['id'][:100]
            self.url_to_uuid[item['url']] = item['id']
            try:
                html = item['html']
                file = open(os.path.join("data/webresourcemanager/source", item['id'] +".html"), "w")
                file.write(html.decode('utf-8', 'ignore'))
                file.close()
                del item['html']
            except:
                pdf = item['pdf']
                file = open(os.path.join("data/webresourcemanager/source", item['id'] +".pdf"), "w")
                file.write(pdf.decode('utf-8', 'ignore'))
                file.close()
                del item['pdf']
            file = open(os.path.join("data/webresourcemanager/docs", item['id']+".json"), "w")
            file.write(json.dumps(item, sort_keys=True, indent=4))
            file.close()    
    
    def string_to_uuid(self, string):
        #not my function, read documentation elsewhere
        return uuid.uuid5(uuid.NAMESPACE_DNS, string)
    
    def save(self, file_name="data/webresourcemanager.json"):
        """
        Saves the Web Resource Manager Instance (rel_path and url_to_uuid in JSON). USES rel_path

    
        Parameters
        ----------
        file_name : string
            file where you'd like to save the instance (default = "data/webresourcemanager.json")
            
        Returns
        -------
        None
    
        """
        this = { 'rel_path' : self.rel_path, 'url_to_uuid': self.url_to_uuid }
        if self.rel_path == None:
            file = open(file_name, "w")
        else:
            file = open(os.path.join(self.rel_path, file_name), "w")
        file.write(json.dumps(this, sort_keys = True, indent = 4))
        file.close


    def update_profile(self, item):
        """
        Updates the saved version of the web resource profile with the instance passed in

    
        Parameters
        ----------
        item : dict
            a web resource profile (must have 'id' field)
            
        Returns
        -------
        None
    
        """
        if self.rel_path == None:
            file = open("data/webresourcemanager/docs/{}.json".format(item['id']), "w")
            file.seek(0)
            file.write(json.dumps(item, sort_keys = True, indent = 4))
            file.truncate()
            file.close()
        else:
            file = open(os.path.join(self.rel_path, "data/webresourcemanager/docs/{}.json".format(item['id'])), "w")
            file.seek(0)
            file.write(json.dumps(item, sort_keys = True, indent = 4))
            file.truncate()
            file.close()

def convert_to_corpus(doc):
    """
    Sets all of the text to lower case, removes all non-alphanumeric characters besides apostrophe (') and hyphen (-) with a Regular Expression. All words are lemmatized and then stemmed.


    Parameters
    ----------
    doc : string or list of strings
    a sentence in either string for or list of words form
    
    Returns
    -------
    list of strings
    the sentence after the Natural Language Processing techniques have been applied
    
    """
    ps = PorterStemmer()  
    lmtzr = WordNetLemmatizer()
    doc_list = []
    if type(doc) is list:
        for word in doc:
            doc_list.append(ps.stem(lmtzr.lemmatize(re.sub("[^A-Za-z0-9'-]+", '', word.lower()).strip())))
    if type(doc) is str:
        for word in word_tokenize(doc):
            doc_list.append(ps.stem(lmtzr.lemmatize(re.sub("[^A-Za-z0-9'-]+", '', word.lower()).strip())))
    return doc_list
            
def main():
    for file in os.listdir("../data/webresourcemanager/webresourcemanagers"):
        wrm = WebResourceManager(rel_path = "..")
        wrm.load(os.path.join("../data/webresourcemanager/webresourcemanagers", file))
        wrm.rel_path=".."
    
if __name__ == "__main__" :
    main()