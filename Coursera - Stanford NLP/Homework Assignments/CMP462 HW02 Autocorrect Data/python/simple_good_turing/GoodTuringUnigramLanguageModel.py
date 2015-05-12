import collections
import math
from SimpleGoodTuringSmoother import SGTSmoother

UNKNOWN = '__++##$$<UKN>$$##++__'


class GoodTuringBigramLanguageModel:
    def __init__(self, corpus):
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.train(corpus)
        self.sgt = None

    def train(self, corpus):
        """Takes a HolbrookCorpus corpus, does whatever training is needed."""
        for sentence in corpus.corpus:
            prevToken = sentence.get(0).word
            for i in xrange(1, sentence.len()):
                token = sentence.get(i).word
                self.bigramCounts[(prevToken, token)] += 1
                prevToken = token

        countsOfFrequencies = {r: 0 for r in set(self.bigramCounts.values())}
        for r in self.bigramCounts.values():
            countsOfFrequencies[r] += 1
        self.sgt = SGTSmoother(countsOfFrequencies)

    def score(self, sentence):
        """Takes a list of strings, returns a score of that sentence."""
        score = 0.0
        prevToken = sentence[0]
        for token in sentence[1:]:
            bicount = self.bigramCounts[(prevToken, token)]
            score += math.log(self.sgt.probOf(bicount))
            prevToken = token

        return score
