# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:10:12 2018

@author: alex
"""
import parser
from kpm.corpusBuilder import *

def URLs_to_KPM(list_of_URLs):
#    parser.parser(list_of_URLs)
    cb = corpusBuilder("data/sentences/")
    cb.save("corpus.json")
    docs = cb.to_TaggedDocument()
    model = models.Doc2Vec(docs, workers=3)
    print("Start training process...")
    model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
    print(model.wv.most_similar(positive=['woman', 'king'], negative=['man']))
    print(model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
    print(model.wv.similarity('woman', 'man'))

def main():    
    with open("kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    URLs_to_KPM(content)
    
if __name__ == "__main__" :
    main()