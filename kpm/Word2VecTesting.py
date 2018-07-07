# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from gensim.utils import SaveLoad
from gensim import corpora
from six import iteritems
import logging
from corpusBuilder import corpusBuilder

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
documents = corpusBuilder()
documents.load()

model = Word2Vec(documents, workers=3)
model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
print(model.wv.most_similar(positive=['woman', 'king'], negative=['man']))
print(model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
print(model.wv.similarity('woman', 'man'))
