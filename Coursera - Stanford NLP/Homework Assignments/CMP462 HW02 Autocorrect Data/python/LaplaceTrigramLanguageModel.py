import collections
import math


class LaplaceTrigramLanguageModel:
    def __init__(self, corpus):
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.trigramCounts = collections.defaultdict(lambda: 0)
        self.total = 0
        self.V = 0
        self.train(corpus)

    def train(self, corpus):
        """Takes a HolbrookCorpus corpus, does whatever training is needed."""
        for sentence in corpus.corpus:
            self.total += sentence.len()
            prevPrevToken = sentence.get(0).word
            self.unigramCounts[prevPrevToken] += 1
            if sentence.len() < 2:
                continue
            prevToken = sentence.get(1).word
            self.unigramCounts[prevToken] += 1
            self.bigramCounts[(prevPrevToken, prevToken)] += 1
            for i in xrange(2, sentence.len()):
                token = sentence.get(i).word
                self.unigramCounts[token] += 1
                self.bigramCounts[(prevToken, token)] += 1
                self.trigramCounts[(prevPrevToken, prevToken, token)] += 1
                prevPrevToken = prevToken
                prevToken = token
        # count unique vocabs in the corpus
        self.V = len(set(self.unigramCounts.keys()))

    def score(self, sentence):
        """Takes a list of strings, returns a score of that sentence."""
        score = 0.0
        # from quick tests, it appears that adding the probability of the very first token (using unigram model)
        # does not affect the overall accuracy of the model.
        # implement add-1 smoothing
        score += math.log(self.unigramCounts[sentence[0]] + 1) - math.log(self.total + self.V)
        if len(sentence) < 2:
            return score
        score += math.log(self.bigramCounts[(sentence[0], sentence[1])] + 1) - math.log(
            self.unigramCounts[sentence[0]] + self.V)
        for i in xrange(2, len(sentence)):
            tricount = self.trigramCounts[(sentence[i - 2], sentence[i - 1], sentence[i])]
            bicount = self.bigramCounts[(sentence[i - 1], sentence[i])]
            # implement add-1 smoothing
            score += math.log(tricount + 1) - math.log(bicount + self.V**2)

        return score
