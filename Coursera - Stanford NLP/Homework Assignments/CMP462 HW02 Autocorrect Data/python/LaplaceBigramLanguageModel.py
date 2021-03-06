import collections
import math


class LaplaceBigramLanguageModel:
    def __init__(self, corpus):
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.total = 0
        self.V = 0
        self.train(corpus)

    def train(self, corpus):
        """Takes a HolbrookCorpus corpus, does whatever training is needed."""
        for sentence in corpus.corpus:
            self.total += sentence.len()
            prevToken = sentence.get(0).word
            self.unigramCounts[prevToken] += 1
            for i in xrange(1, sentence.len()):
                token = sentence.get(i).word
                self.unigramCounts[token] += 1
                self.bigramCounts[(prevToken, token)] += 1
                prevToken = token
        # count unique vocabs in the corpus
        self.V = len(set(self.unigramCounts.keys()))

    def score(self, sentence):
        """Takes a list of strings, returns a score of that sentence."""
        score = 0.0
        prevToken = sentence[0]
        prevTokenCount = self.unigramCounts[prevToken]

        # from quick tests, it appears that adding the probability of the very first token (using unigram model)
        # does not affect the overall accuracy of the model.
        # implement add-1 smoothing
        score += math.log(prevTokenCount + 1)
        score -= math.log(self.total + self.V)
        for token in sentence[1:]:
            bicount = self.bigramCounts[(prevToken, token)]
            # implement add-1 smoothing
            score += math.log(bicount + 1)
            score -= math.log(prevTokenCount + self.V)
            # sift tokens one step forward
            prevToken = token
            prevTokenCount = self.unigramCounts[prevToken]

        return score
