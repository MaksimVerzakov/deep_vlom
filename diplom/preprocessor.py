#!/usr/bin/env python
# -- coding: utf-8 --
import re
import os
from pymorphy import get_morph
from settings import DICTS_DIR

def get_stop_words(path):
    '''Return stop-words list.'''
    try:
        f = open(path)
    except IOError:
        return []
    return f.read().decode("utf-8", 'ignore').split()

def formalize(filename):
    morph = get_morph(DICTS_DIR)
    stop_words = get_stop_words(os.path.join(DICTS_DIR, 'stop_test.txt'))
    dict = {}
    words = 0.0
    try:
        f = open(filename)
    except IOError:
        raise
    for line in f.readlines():
        for word in line.split():
            word = word.decode("utf-8", 'ignore')
            word = word.strip(u'[,.:;\"\')$«»(?<>!-_—//=]\n\t')
            word = word.replace('.', '_')
            word = morph.normalize(word.upper())
            if isinstance(word, set):
                word = word.pop()
            else:
                continue
            word = word.lower()
            words += 1
            if word in stop_words or not word:
                continue
            if not word in dict:
                dict[word] = 1.0
            else:
                dict[word] += 1.0
    for key in dict:
        dict[key] /= words
    return dict

def remove_transfer(filename):
    o = open(filename,"r+")
    data = o.read()
    new = re.sub("-\n","", data)
    o.seek(0)
    o.write(new)
    o.close()
