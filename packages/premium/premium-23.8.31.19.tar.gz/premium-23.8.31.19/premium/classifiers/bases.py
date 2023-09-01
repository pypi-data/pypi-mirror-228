#!/usr/bin/env python

import pickle
import time
from abc import ABC
from typing import Callable, Dict, Union

import codefast as cf
import jieba
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)

from .tokenizers import en_tokenizer, zh_tokenizer

class AbstractBenchmark(ABC):
    pass


class Benchmark(AbstractBenchmark):

    def get_data(self, datadict: pd.DataFrame):
        raise NotImplementedError()


def calculate_metrics(y_true, y_pred) -> Dict:
    acc = accuracy_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred, zero_division=0)
    prec = precision_score(y_true, y_pred, zero_division=0)

    f1 = 2 * prec * rec / (prec + rec + 1e-8)
    tp, fp, tn, fn = 0, 0, 0, 0
    for y1, y2 in zip(y_true, y_pred):
        if y1 == y2:
            if y1 == 1:
                tp += 1
            else:
                tn += 1
        else:
            if y1 == 1:
                fn += 1
            else:
                fp += 1

    return {
        'accuracy': acc,
        'recall': rec,
        'precision': prec,
        'f1': f1,
        'confusion_matrix': {
            'tp': tp,
            'fp': fp,
            'tn': tn,
            'fn': fn,
        }
    }


class NNModel(Benchmark):

    def __init__(self):
        self.name = 'network'
        self.model = None

    def fit(self, X: pd.DataFrame):
        raise NotImplementedError()

    def evaluate(self, Xt: pd.DataFrame) -> Dict:
        raise NotImplementedError()

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

    def run(self, train, test):
        raise NotImplementedError()


class TreeModel(Benchmark):

    def __init__(self,
                 vectorizer: Union[str, Callable] = 'tfidf',
                 tokenizer: Callable = zh_tokenizer):
        """ Built-in jieba toknizer, therefore there is no need to pass a tokenizer
        """
        if isinstance(vectorizer, CountVectorizer):
            self.vectorizer = vectorizer
        elif vectorizer not in ['tfidf', 'count']:
            raise ValueError('vectorizer must be one of tfidf or count')
        else:
            self.vectorizer = TfidfVectorizer(
            ) if vectorizer == 'tfidf' else CountVectorizer()
        self.tokenizer = tokenizer
        self.name = 'tree'

    def preprocess(self, X: pd.DataFrame) -> pd.DataFrame:
        X['text'] = X['text'].apply(lambda x: ' '.join(self.tokenizer(x))
                                    if self.tokenizer else x)
        return X

    def fit(self, X: pd.DataFrame):
        texts = [' '.join(self.tokenizer(x)) for x in X['text']]
        x = self.vectorizer.fit_transform(texts).astype('float32')
        self.model.fit(x, X['label'])

    def evaluate(self, Xt: pd.DataFrame) -> Dict:
        texts = [' '.join(self.tokenizer(x)) for x in Xt['text']]
        x = self.vectorizer.transform(texts).astype('float32')
        x = x.astype('float32')
        y = Xt['label']
        y_pred = self.model.predict(x)
        return calculate_metrics(y, y_pred)

    def inner_run(self, X, Xt):
        """ Run the model and return the results
        Args:
            X(pd.DataFrame): train data
            Xt(pd.DataFrame): test data
        """
        X, Xt = self.preprocess(X), self.preprocess(Xt)
        cf.info({
            'vectorizer': self.vectorizer.__class__.__name__,
            'tokenizer': self.tokenizer.__name__,
            'model': self.name,
            'step': 'fit',
            'length of train': len(X),
            'train value counts': X['label'].value_counts().to_dict(),
            'length of test': len(Xt),
            'test value counts': Xt['label'].value_counts().to_dict(),
        })
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
        raise NotImplementedError()

    def predict(self, X, threshold=0.5):
        assert isinstance(X, list), 'X must be a list of strings'
        texts = [' '.join(self.tokenizer(x)) for x in X]
        x = self.vectorizer.transform(texts).astype('float32')
        x = x.astype('float32')
        prob = self.model.predict_proba(x)
        return prob[:, 1] > threshold

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(
                {
                    'vectorizer': self.vectorizer,
                    'tokenizer': self.tokenizer,
                    'model': self.model,
                }, f)

    def load_model(self, path):
        with open(path, 'rb') as f:
            dict_ = pickle.load(f)
            self.vectorizer = dict_['vectorizer']
            self.tokenizer = dict_['tokenizer']
            self.model = dict_['model']
        return self

    def load(self, path):
        return self.load_model(path)
