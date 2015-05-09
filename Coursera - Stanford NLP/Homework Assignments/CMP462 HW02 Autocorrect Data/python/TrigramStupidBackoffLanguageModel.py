import collections
import math


class TrigramStupidBackoffLanguageModel:
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
        score += self.__add_1_smoothed_unigram__(sentence[0])
        if len(sentence) < 2:
            return score
        score += self.__add_1_smoothed_bigram__(sentence[0], sentence[1])
        for i in xrange(2, len(sentence)):
            tricount = self.trigramCounts[(sentence[i - 2], sentence[i - 1], sentence[i])]
            bicount = self.bigramCounts[(sentence[i - 1], sentence[i])]
            if tricount > 0:
                score += (math.log(tricount) - math.log(self.bigramCounts[(sentence[i - 2], sentence[i - 1])]))
            elif bicount > 0:
                # since pair was seen before, then revert to unsmoothed bigram
                score += (math.log(0.4) + math.log(bicount) - math.log(self.unigramCounts[sentence[i - 1]]))
            else:
                # else "stupidly" revert to add-1 smoothed unigram
                score += (2. * math.log(0.4) + self.__add_1_smoothed_unigram__(sentence[i]))

        return score

    def __add_1_smoothed_unigram__(self, token):
        return math.log(self.unigramCounts[token] + 1) - math.log(self.total + self.V)

    def __add_1_smoothed_bigram__(self, prevToken, token):
        return math.log(self.bigramCounts[(prevToken, token)] + 1) - math.log(self.unigramCounts[prevToken] + self.V)