# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 20:24:15 2018

@author: alex
"""
from gensim import models
from gensim.models.doc2vec import TaggedDocument

class MySentences(object):
    
    def __init__(self, dirname):
        self.dirname = dirname
        self.sent_list = []
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                l = line.split()
                for elem in l:
                    elem = elem.lower()
                self.sent_list.append(elem)

    def __iter__(self):
        for elem in self.sent_list:
            yield elem
                
    def __getitem__(self, key):
        return self.sent_list[key]
                
    def __len__(self):
        return(len(self.sent_list))
                
sentences = MySentences("../data/sentences/")

docs = []
for i in range(len(sentences)):
    docs.append(TaggedDocument(words=sentences[i].split(), tags=[i]))


model = models.Doc2Vec(docs, workers=3)

print("Start training process...")
model.train(docs, total_examples=model.corpus_count, epochs=model.iter)

#save model
model.save("doc2vec_model")