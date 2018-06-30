# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:09:11 2018

@author: amichels
"""
import json

class Mapper(object):
    
    def __init__(self, file=None):
        if (file != None):
            try:
                self.mapping = json.loads(open(file).read())
            except Exception as e:
                self.mapping = {}
                print("THERE WAS AN ERROR IN LOADING {}".format(file))
                print(e)
        else:
            self.mapping = {}
    
    #shortcut to accessing "in" and "__contains__" for the dict in it
    def __contains__(self, key):
        return(self.mapping.__contains__(key))
    
    #deletes the key, value pair from the dict
    def __delitem__(self, key):
        self.mapping.__delitem__(key)
    
    #get the aliases (list of strings) from the ID number by [] operators
    def __getitem__(self, key):
        try:
            return(self.mapping[key])
        except:
            return []
    
    #Returns the number of keys in the dictionary in the Mapper object
    def __len__(self):
        return(len(self.mapping.keys()))
    
    #Prints the dictionary in a pretty JSON format.
    def __repr__(self):
        return json.dumps(self.mapping, sort_keys = True, indent = 4)
    
    #sets the key to the value
    def __setitem__(self, key, value):
        self.mapping[key] = value
    
    #Prints the dictionary in a pretty JSON format.
    def __str__(self):
        return json.dumps(self.mapping, sort_keys = True, indent = 4)
        
    #get the aliases (list of strings) from the ID number
    def get(self, key):
        return(self.mapping[key])
    
    #get the aliases (list of strings) from the ID number
    def id_to_alias(self, key):
        return(self.mapping[key])

    
        
        
def main():
    mapper = Mapper(file="KPM/id_to_alias.JSON")
    print(mapper)
    print(mapper["0000004"])
    
    
if __name__ == u"__main__" :
    main()
