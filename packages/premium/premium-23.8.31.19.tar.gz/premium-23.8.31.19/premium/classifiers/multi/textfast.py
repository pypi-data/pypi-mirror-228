#!/usr/bin/env python3
import os
from tempfile import NamedTemporaryFile as tmpfile

import fasttext

from premium.classifiers.bases import NNModel, calculate_metrics


class FastTextMulti(NNModel):
    """ FastText Binary Classifier
    """

    def __init__(self, tokenizer=None):
        super().__init__()
        self.name += ':fasttext'
        self.tokenizer = tokenizer

    def fit(self, X):
        X['label'] = '__label__' + X['label'].astype(str)
        with tmpfile() as f:
            X[['label', 'text']].to_csv(f.name, sep='\t', index=False)
            parmas = {
                'input': f.name,
                'thread': 12,
                'autotuneDuration': 300,
            }
            self.model = fasttext.train_supervised(**parmas)

    def evaluate(self, Xt):
        texts = [x.replace('\n', ' ') for x in Xt['text']]
        preds = [self.model.predict(x)[0][0] for x in texts]
        preds = [int(x.replace('__label__', '')) for x in preds]
        return calculate_metrics(Xt['label'], preds)

    def preprocess(self, X):
        X['text'] = X['text'].apply(lambda x: ' '.join(self.tokenizer(str(x)))
                                    if self.tokenizer else x)
        return X

    def run(self, X, Xt):
        X, Xt = self.preprocess(X), self.preprocess(Xt)
        return self.inner_run(X, Xt)


class PretrainedFastTextMulti(NNModel):
    """ FastText with pretrained vector
    """

    def __init__(self, pretrained_vector: str, tokenizer=None):
        """ 
        Args:
            pretrained_vector(str): path to pretrained vector
            dim(int): dimension of pretrained vector
        """
        super().__init__()
        self.pretrained_vector = pretrained_vector
        assert os.path.exists(pretrained_vector), 'pretrained vector not found'
        with open(pretrained_vector) as f:
            self.dim = int(f.readline().split()[1])
        self.tokenizer = tokenizer

    def fit(self, X):
        X['label'] = '__label__' + X['label'].astype(str)
        with tmpfile() as f:
            X[['label', 'text']].to_csv(f.name, sep='\t', index=False)
            parmas = {
                'input': f.name,
                'thread': 12,
                'dim': self.dim,
                'pretrainedVectors': self.pretrained_vector,
            }
            self.model = fasttext.train_supervised(**parmas)

    def evaluate(self, Xt):
        texts = [str(x).replace('\n', ' ') for x in Xt['text']]
        preds = [self.model.predict(x)[0][0] for x in texts]
        preds = [int(x.replace('__label__', '')) for x in preds]
        return calculate_metrics(Xt['label'], preds)

    def preprocess(self, X):
        X['text'] = X['text'].apply(lambda x: ' '.join(self.tokenizer(str(x)))
                                    if self.tokenizer else x)
        return X

    def run(self, X, Xt):
        X, Xt = self.preprocess(X), self.preprocess(Xt)
        self.name += ':fasttext_pretrained'
        return self.inner_run(X, Xt)
