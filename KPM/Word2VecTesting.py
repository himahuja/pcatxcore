# -*- coding: utf-8 -*-

from gensim.models import Word2Vec
import logging, os


class MySentences(object):
    
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                l = line.split()
                for elem in l:
                    elem = elem.lower()
                yield l

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = MySentences("Sentences")
model = Word2Vec(sentences, min_count=1, workers = 3)
print(model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1))
#min_count is minimimum appearances to be included (default = 5)
#size is the NN layers (default = 100)
#workers is number of cores (default = 1)
