# -- coding: utf-8 --
import math, collections
from pymorphy import get_morph
import json
from settings import DICTS_DIR

class LaplaceBigramLanguageModel:

    def __init__(self, corpus=None):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.V = 0
        self.morph = get_morph(DICTS_DIR)
        if corpus:
            self.train(corpus)

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        w_prev = None
        for sentence in corpus:
            i = 0
            old_perc = -1
            for string in sentence:
                perc = round(float(i) / len(sentence) * 100)
                if perc % 5 == 0 and perc != old_perc:
                    print perc
                    old_perc = perc
                i += 1
                for word in string.split():
                    w = word.decode("utf-8", 'ignore')
                    w = w.strip(u'[,.:;\"\')$«»(?<>!-_—//=]\n\t')
                    w = self.morph.normalize(w.upper())
                    if isinstance(w, set):
                        w = w.pop()
                    w = w.lower()
                    if not self.unigramCounts.has_key(w):
                        self.V += 1
                    self.unigramCounts[w] += 1
                    if w_prev is not None:
                        key = '%s_%s' % (w_prev, w)
                        self.bigramCounts[key] += 1
                    w_prev = w

    def score(self, sentence, add):
        """ Takes a list of strings as argument and returns the log-probability of the
            sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        w_prev = None
        w = None
        for string in sentence:
            for word in string.split():
                w = word.decode("utf-8", 'ignore')
                w = w.strip(u'[,.:;\"\')$«»(?<>!-_—//=]\n\t')
                w = self.morph.normalize(w.upper())
                if isinstance(w, set):
                    w = w.pop()
                w = w.lower()
                key = '%s_%s' % (w_prev, w)
                score += math.log(self.bigramCounts.get(key, 0.0) + add)
                score -= math.log(self.unigramCounts.get(w_prev, 0.0) + add * self.V)
            w_prev = w
        return score

    def good_score(self, sentence, add):
        """ Takes a list of strings as argument and returns the log-probability of the
            sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        w_prev = None
        w = None
        for string in sentence:
            for word in string.split():
                w = word.decode("utf-8", 'ignore')
                w = w.strip(u'[,.:;\"\')$«»(?<>!-_—//=]\n\t')
                w = self.morph.normalize(w.upper())
                if isinstance(w, set):
                    w = w.pop()
                w = w.lower()
                key = '%s_%s' % (w_prev, w)
                score += math.log(self.bigramCounts.get(key, 0.0) + add)
                score -= math.log(self.unigramCounts.get(w_prev, 0.0) + add * self.V)
            w_prev = w
        return score

    def dumps(self, path):
        f = open(path, 'wb+')
        f.write(str(self.V))
        f.write('\n')
        f.write(json.dumps(self.bigramCounts))
        f.write('\n')
        f.write(json.dumps(self.unigramCounts))

    def loads(self, path):
        f = open(path, 'r+')
        self.V = int(f.readline())
        self.bigramCounts = json.loads(f.readline())
        self.unigramCounts = json.loads(f.readline())
