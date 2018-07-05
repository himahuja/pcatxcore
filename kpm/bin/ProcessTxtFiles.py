# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 18:56:05 2018

@author: alex
"""
import codecs, os, re

def ProcessAbstracts(dirname):
    for fname in os.listdir(dirname):
        file = codecs.open(os.path.join(dirname, fname), "r+",encoding='utf-8', errors='ignore')
        text = file.read()
        text = text.replace("### abstract ###", "").replace("### introduction ###", "").replace("CITATION", "")
        text = re.sub('[^A-Za-z\']+', ' ', text)
        text = text.lower()
        file.seek(0)
        file.write(text)
        file.truncate()
        file.close()
        if (os.listdir(dirname).index(fname) != 0 and os.listdir(dirname).index(fname) % 100 == 99):
            print("...{:.2f}% done, processing document {} of {}".format(((os.listdir(dirname).index(fname)+1)/len(os.listdir(dirname)))*100,os.listdir(dirname).index(fname)+1,len(os.listdir(dirname))))
    print("...{:.2f}% done, processing document {} of {}".format(100,len(os.listdir(dirname)),len(os.listdir(dirname))))

def Process20NewsGroups(dirname):
    for fname in os.listdir(dirname):
        file = codecs.open(os.path.join(dirname, fname), "r+",encoding='utf-8', errors='ignore')
        text = file.read()
        text = text[text.find("Lines:"):]
        text = text[text.find("\n"):]
        text = re.sub('\S*@\S*\s?', "", text)
        text = re.sub('[^A-Za-z\']+', ' ', text)
        text = text.lower()
        file.seek(0)
        file.write(text)
        file.truncate()
        file.close()
        if (os.listdir(dirname).index(fname) != 0 and os.listdir(dirname).index(fname) % 100 == 99):
            print("...{:.2f}% done, processing document {} of {}".format(((os.listdir(dirname).index(fname)+1)/len(os.listdir(dirname)))*100,os.listdir(dirname).index(fname)+1,len(os.listdir(dirname))))
    print("...{:.2f}% done, processing document {} of {}".format(100,len(os.listdir(dirname)),len(os.listdir(dirname))))


def main():    
    ProcessAbstracts(os.getcwd())
    
if __name__ == "__main__" :
    main()
    