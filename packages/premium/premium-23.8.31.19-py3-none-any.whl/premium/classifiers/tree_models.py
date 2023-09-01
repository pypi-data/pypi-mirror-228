#!/usr/bin/env python3
from typing import Dict, List, Tuple

from classifiercluster import Classifiers

from premium.classifiers.bases import TreeModel


class Xgboost(TreeModel):

    def __init__(self, vectorizer='tfidf'):
        super().__init__(vectorizer)
        self.model = Classifiers().xgb
        self.name = 'xgboost:{}'.format(vectorizer)

    def run(self, train, test):
        return self.inner_run(train, test)


class Catboost(TreeModel):

    def __init__(self, vectorizer='tfidf'):
        super().__init__(vectorizer)
        self.model = Classifiers().cat
        self.name = 'catboost:{}'.format(vectorizer)

    def run(self, train, test):
        return self.inner_run(train, test)


class Lightgbm(TreeModel):

    def __init__(self, vectorizer='tfidf'):
        super().__init__(vectorizer)
        self.model = Classifiers().gbm
        self.name = 'lightgbm:{}'.format(vectorizer)

    def run(self, train, test):
        return self.inner_run(train, test)
