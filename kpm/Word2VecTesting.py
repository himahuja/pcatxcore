# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from gensim.utils import SaveLoad
from gensim import corpora
from six import iteritems
import logging
from corpusBuilder import corpusBuilder

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
documents = corpusBuilder("../data/sentences/")

model = Word2Vec(min_count=1)
model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.iter)
print(model.wv.most_similar(positive=['cat']))
