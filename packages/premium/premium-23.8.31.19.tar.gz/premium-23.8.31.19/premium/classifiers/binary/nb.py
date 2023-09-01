import time

import codefast as cf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from premium.classifiers.bases import Benchmark, NNModel, calculate_metrics

# Naive Bayes Classifier


class NaiveBayesBinary(Benchmark):

    def __init__(self, tokenizer=None):
        """ Chinese text may need a tokenizer
        """
        self.name = 'naivebayes'
        self.model = None
        self.vectorizer = CountVectorizer()
        self.tokenizer = tokenizer

    def preprocess(self, X):
        if self.tokenizer:
            X['text'] = X['text'].apply(
                lambda x: ' '.join(self.tokenizer(str(x))))
        return X

    def fit(self, X):
        label = X['label']
        X = self.preprocess(X)
        X = self.vectorizer.fit_transform(X['text'])
        self.model = MultinomialNB()
        self.model.fit(X, label)

    def evaluate(self, Xt):
        label = Xt['label']
        Xt = self.preprocess(Xt)
        Xt = self.vectorizer.transform(Xt['text'])
        preds = self.model.predict(Xt)
        return calculate_metrics(label, preds)

    def inner_run(self, X, Xt):
        """ Run the model and return the results
        Args:
            X(pd.DataFrame): train data
            Xt(pd.DataFrame): test data
        """
        start_time = time.time()
        self.fit(X)
        res = self.evaluate(Xt)
        period = time.time() - start_time
        cf.info({
            'time': '{} seconds'.format(round(period, 2)),
            'res': res,
            'model': self.name,
        })
        return res

    def run(self, X, Xt):
        return self.inner_run(X, Xt)
