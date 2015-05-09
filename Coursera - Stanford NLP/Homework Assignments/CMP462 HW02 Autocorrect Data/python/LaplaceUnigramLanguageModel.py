import collections
import math


class LaplaceUnigramLanguageModel:
    def __init__(self, corpus):
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.total = 0
        self.V = 0
        self.train(corpus)

    def train(self, corpus):
        """Takes a HolbrookCorpus corpus, does whatever training is needed."""
        for sentence in corpus.corpus:
            self.total += sentence.len()
            for datum in sentence.data:
                token = datum.word
                self.unigramCounts[token] += 1
        # count unique vocabs in the corpus
        self.V = len(set(self.unigramCounts.keys()))

    def score(self, sentence):
        """Takes a list of strings, returns a score of that sentence."""
        score = 0.0
        for token in sentence:
            count = self.unigramCounts[token]
            # implement add-1 smoothing
            score += math.log(count + 1)
            score -= math.log(self.total + self.V)

        return score
