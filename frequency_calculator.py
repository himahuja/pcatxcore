from collections import Counter
import nltk

def frequency_calculator(text_string):
    word_list = nltk.word_tokenize(text_string)
    counts = Counter(word_list)
    return counts
