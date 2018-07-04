# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 20:24:15 2018

@author: alex
"""
from gensim import models
from docsProcessor import docsProcessor
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
                
docs = docsProcessor("../data/sentences/").to_TaggedDocument()
model = models.Doc2Vec(docs, workers=3)

print("Start training process...")
model.train(docs, total_examples=model.corpus_count, epochs=model.iter)

#save model
model.save("doc2vec_model")
print(model.wv.most_similar(positive=['woman', 'king'], negative=['man']))