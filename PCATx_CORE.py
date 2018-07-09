# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:10:12 2018

@author: alex
"""
import parser, pickle
from kpm.corpusBuilder import *
from webcrawlAll import crawlerWrapper

def WC_to_KPM(query_string):
    crawlerWrapper(query_string, "google")
    with open("data/parsedLinks/{}.pk".format(query_string), "rb") as handle:
        url_list = pickle.load(handle)
    parser.parser(query_string, url_list)
    cb = corpusBuilder("data/sentences/")
    cb.save()
    docs = cb.to_TaggedDocument()
    model = models.Doc2Vec(docs, workers=3, min_count=20)
    print("Start training process...")
    model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
    print(model.wv.most_similar(positive=['woman', 'king'], negative=['man']))
    print(model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
    print(model.wv.similarity('woman', 'man'))

def main():
    WC_to_KPM("olin polyethyl")
    
if __name__ == "__main__" :
    main()