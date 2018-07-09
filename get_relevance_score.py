from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk

# FileManager TODO: open, read documents in a folder and build a list
# document_list = []
tfidf = TfidfVectorizer(stop_words='english')
tfidf.fit_transform(document_list)

def get_relevance_score(document, tfidf):
    response = tfidf.transform([document])
    feature_names = tfidf.get_feature_names()
  
    score_dict = {}
    for col in response.nonzero()[1]:
        score_dict[feature_names[col]] = response[0,col]
    
    word_list = nltk.word_tokenize(document)
    total_score = 0
    count_keywords = 0
    for word in word_list:
        if word in score_dict:
            total_score += score_dict[word]
            count_keywords += 1
    score = total_score / count_keywords
    return score

# document = ''
score = get_relevance_score(document, tfidf)
print(score)
