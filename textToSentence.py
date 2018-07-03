import nltk
def textToSentence(filePath):
    file = open(filePath)
    raw = file.read()
    sentList = nltk.sent_tokenize(raw)
    return sentList
