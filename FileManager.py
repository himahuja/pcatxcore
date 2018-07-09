#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 15:27:52 2018

@author: alex
"""
from PCATParser import *
import json, os, uuid

class FileManager(object):
    
    def __init__(self, rel_path=None):
        #read in the file
        self.rel_path = rel_path
        self.uuid_to_url = {}
        self.url_to_uuid = {}
        
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
    
    def read_in_docs(self, iterator_of_docs):
        for item in iterator_of_docs:
            item['id'] = str(self.string_to_uuid(item['url']))
            self.uuid_to_url[item['id']] = item['url']
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
            file = open(os.path.join("data/sentences", item['id']+".json"), "w")
            file.write(json.dumps(item, sort_keys=True, indent=4))
            file.close()    
    
    def string_to_uuid(self, string):
        return uuid.uuid5(uuid.NAMESPACE_DNS, string)
    
    def save(self, file_name=None):
        this = { 'uuid_to_url': self.uuid_to_url, 'url_to_uuid': self.url_to_uuid }
        if file_name == None:
            if self.rel_path == None:
                file = open("data/filemanager.json", "w")
            else:
                file = open(os.path.join(self.rel_path, "data/filemanager.json"), "w")
        else:
            file = open(file_name, "w")
        file.write(json.dumps(this, sort_keys = True, indent = 4))
        file.close
        
    def url_to_uuid(self, url):
        return self.url_to_uuid[url]
    
    def uuid_to_url(self, key):
        return self.uuid_to_url[key]
            
        
def main():
    with open("kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    fm = FileManager()
    fm.read_in_docs(parser_iter("test", content))
    fm.save()
    
if __name__ == "__main__" :
    main()