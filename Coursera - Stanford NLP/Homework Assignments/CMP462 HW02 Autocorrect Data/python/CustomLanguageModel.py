import collections
import math


class CustomLanguageModel:
    """
    The same as StupidBackoffLanguageModel, but with Add-DELTA smoothing (instead of Add-1), when it reverts to
    Unigram Language Model after Bigram Language Model fails.
    This is the model picked after the following attempts:
    1. Trigram LM which then led to implementing TrigramStupidBackoffLanguageModel,
        but failed to beat StupidBackoffLanguageModel.
    2. Simple Good-Turing is then tried for smoothing instead of Add-1. However, achieved 0 correct matches !!!
        Alternative implementation provided online was then used for Simple Good-Turing (instead of my own, to be
        a little bit more safe about bugs), but still 0 matches !!!
        SGT with unigrams achieved 2 matches, as opposed to the above zeros achieved by SGT with bigrams.
    Note: The previous 2 attempts when put together, might point to the an educated-guess, which is the data is NOT
    enough for sophisticated algorithms to achieve better results ... may be more more data is needed?! requires more
    investigation. However, this insight led me to consider Add-something_less_than_1(DELTA) Smoothing.
    The model should be even less confident than 1 that it "saw" unseen events (n-grams)
    3. Add-DELTA Smoothing, when incorporated into StupidBackoffLanguageModel was able to achieve 119 correct matches :)
        This would give the CustomLanguageModel, where you can adjust DELTA used for smoothing in the last function at
        the very-bottom of this class.
    """
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

        # from quick tests, it appears that adding the probability of the very first token (using unigram model)
        # does not affect the overall accuracy of the model.
        # implement add-1 smoothing unigram for very first token
        score += self.__add_1_smoothed_unigram__(prevToken)
        for token in sentence[1:]:
            bicount = self.bigramCounts[(prevToken, token)]
            if bicount > 0:
                # since pair was seen before, then use unsmoothed bigram
                score += (math.log(bicount) - math.log(self.unigramCounts[prevToken]))
            else:
                # else "stupidly" revert to add-1 smoothed unigram
                score += (math.log(0.4) + self.__add_1_smoothed_unigram__(token))
            # sift tokens one step forward
            prevToken = token

        return score

    def __add_1_smoothed_unigram__(self, token, DELTA=1E-5):
        # the delta parameter allows implementing the Add-D Smoothing, a generalization of the Add-1.
        return math.log(self.unigramCounts[token] + DELTA) - math.log(self.total + (DELTA * self.V))
