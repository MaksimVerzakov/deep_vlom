#!/usr/bin/env python
# -- coding: utf-8 --

from pymorphy import get_morph
from settings import DICTS_DIR

def get_stop_words(path):
    try:
        f = open(path)
    except IOError:
        return None
    return f.read().decode("utf-8", 'ignore').split()

def formalize(filename):
    morph = get_morph(DICTS_DIR)
    stop_words = get_stop_words(DICTS_DIR + '/stop_test.txt')
    dict = {}
    words = 0.0
    try:
        f = open(filename)
    except IOError:
        raise
    for line in f.readlines():
        for word in line.split():
            word = word.decode("utf-8", 'ignore')
            word = word.strip(u'[,.:;\"\')«»(?<>!-_—//=]\n\t')
            word = morph.normalize(word.upper())
            if isinstance(word, set):
                word = word.pop()
            if not word:
                continue
            word = word.lower()
            words += 1
            if word in stop_words:
                continue
            if not word in dict:
                dict[word] = 1.0
            else:
                dict[word] += 1.0
    for key in dict:
        dict[key] /= words
    return dict

if __name__=='__main__':
    d = formalize("/home/xam_vz/GULAG2.TXT")
    for el in d:
        print '%s : %s\n' % (el, d[el])
