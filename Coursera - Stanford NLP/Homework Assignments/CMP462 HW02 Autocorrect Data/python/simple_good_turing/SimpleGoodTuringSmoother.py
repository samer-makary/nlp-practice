import math
import collections


class SGTSmoother:
    """
    NOT TESTED - Code has some fatal bugs. First attempt at understanding/implementing SGT.
    """
    def __init__(self, dictCountOfFreq):
        """
        Create a new smoother.
        :param dictCountOfFreq: A mapping from a frequency r to the frequency of r, N(r)
        :return: new instance
        """
        # this holds the list of frequencies that we have encountered.
        self.frequencies = sorted(list(dictCountOfFreq.keys()))
        # this holds the counts (frequencies) of everyone of the frequencies.
        self.countOfFreq = dictCountOfFreq
        self.N = sum(r * Nr for r, Nr in dictCountOfFreq.items())
        self.PZero = 0
        self.smoothedCounts = collections.defaultdict(lambda: 0)
        self.__smooth__()

    def __smooth__(self):
        if 1 in self.countOfFreq:
            self.smoothedCounts[0] = self.countOfFreq[1]
            self.PZero = self.smoothedCounts[0] / self.N
        else:
            print("Warn: No tokens seen only once?!")

        # average every non-zero frequency with its near-by non-seen frequencies
        avgdCountOfFreq = [0] * len(self.frequencies)
        logFreqs = [0] * len(self.frequencies)
        logAvgdCountOfFreq = [0] * len(self.frequencies)
        for j in xrange(1, len(self.frequencies)):
            # figure out the range of zero(un-seen) frequencies around the seen frequency j
            i = 0 if j == 0 else float(self.frequencies[j - 1])
            k = (2.0 * self.frequencies[j] - i) if j == len(self.frequencies) - 1 else float(self.frequencies[j + 1])
            avgdCountOfFreq[j] = 2.0 * self.countOfFreq[self.frequencies[j]] / (k - i)
            # compute the log of both the frequency and its newly-averaged count
            logFreqs[j] = math.log(self.frequencies[j])
            logAvgdCountOfFreq[j] = math.log(avgdCountOfFreq[j])

        # find best linear fit for log-frequencies and log-averaged-counts
        slope, intercept = __fit_linear__(logFreqs, logAvgdCountOfFreq)
        if slope > -1:
            print("Warn: SGT had a linear fit with slope greater than -1")

        def __S(r):
            return math.exp(intercept + slope * math.log(r))

        for r in self.frequencies:
            self.smoothedCounts[r] = (r + 1) * (__S(r + 1) / __S(r))
        self.N = sum(rStar * SrStar for rStar, SrStar in self.smoothedCounts.items())

    def countOf(self, rFreq):
        return self.smoothedCounts[rFreq]

    def probOf(self, rFreq):
        return (1.0 - self.PZero) * self.smoothedCounts[rFreq] / self.N


def __fit_linear__(logFrequencies, logAvgdCountOfFrequencies):
    XYs, Xsquares = 0, 0
    meanX = sum(logFrequencies) / len(logFrequencies)
    meanY = sum(logAvgdCountOfFrequencies) / len(logAvgdCountOfFrequencies)
    for logFreq, logAvgdCount in zip(logFrequencies, logAvgdCountOfFrequencies):
        XYs += (logFreq - meanX) * (logAvgdCount - meanY)
        Xsquares += (logFreq - meanX) ** 2

    slope = XYs / Xsquares
    intercept = meanY - slope * meanX
    return slope, intercept


