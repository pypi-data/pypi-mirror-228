#!/usr/bin/env python
from sklearn.ensemble import VotingClassifier
import codefast as cf
from .bases import NNModel, Benchmark, calculate_metrics, TreeModel
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


class VotingBoostBinary(TreeModel):

    def __init__(self, vectorizer='count'):
        """ vote boost 三剑客
        """
        super().__init__(vectorizer)
        self.model = VotingClassifier(
            estimators=[('xgb', XGBClassifier()),
                        ('cat', CatBoostClassifier(verbose=False)),
                        ('gbm', LGBMClassifier())], voting='hard')
        self.name = 'votingboost:{}'.format(vectorizer)

    def run(self, train, test):
        return self.inner_run(train, test)
