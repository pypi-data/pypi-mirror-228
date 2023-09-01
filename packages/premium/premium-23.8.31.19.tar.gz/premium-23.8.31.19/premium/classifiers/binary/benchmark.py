#!/usr/bin/env python

from typing import Dict, List, Tuple

import codefast as cf
import pandas as pd
from classifiercluster import Classifiers
from codefast.utils import timeit_decorator
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

from premium.classifiers.bases import Benchmark, TreeModel
from premium.classifiers.binary.bert import BertBinary
from premium.classifiers.binary.lstm import LSTMBinaryClassifier, LSTMInput
from premium.classifiers.binary.nb import NaiveBayesBinary
from premium.classifiers.binary.textfast import (FastTextBinary,
                                                 PretrainedFastTextBinary)
from premium.classifiers.voting import VotingBoostBinary
from premium.data.datasets import downloader, word2vec
from premium.classifiers.tree_models import Lightgbm, Xgboost, Catboost


def format_results(results: Dict):
    # round to 4 decimal places
    return {k: round(v, 4) for k, v in results.items()}


class Metric(BaseModel):
    model: str
    f1: float
    precision: float
    recall: float
    accuracy: float

    def __str__(self) -> str:
        return 'model: {:<20} f1: {:<.4f} precision: {:<.4f} recall: {:<.4f} accuracy: {:<.4f}'.format(
            self.model, self.f1, self.precision, self.recall, self.accuracy)


class Manager(object):

    def __init__(self, runners: List[Tuple[str, Benchmark]], df: pd.DataFrame):
        self.runners = runners
        # df columns = ['text', 'label']
        self.df = df

    def rank(self, metrics: Dict) -> List[Metric]:
        """ Rank the results
        Args:
            metrics(Dict): the results of the benchmark
        Returns:
            Dict: the ranking of the results
        """

        def _rank(_metrics):
            for model, prf1 in _metrics.items():
                yield Metric(model=model, **prf1)

        xs = sorted([_ for _ in _rank(metrics)],
                    key=lambda x: x.f1,
                    reverse=True)
        return xs

    def concurrent_run(self, X, Xt, max_workers=8):
        cf.info({
            'message':
            'Running concurrent benchmarks with {} workers'.format(
                max_workers),
            'X size':
            len(X),
        })

        def _submit():
            from concurrent.futures import ProcessPoolExecutor
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                for name, runner in self.runners:
                    yield name, executor.submit(runner.run, X.copy(),
                                                Xt.copy())

        tasks = [_ for _ in _submit()]
        return {name: format_results(t.result()) for name, t in tasks}

    @timeit_decorator('manager.run')
    def run(self, max_workers=8):
        X, Xt = train_test_split(self.df, test_size=0.2, random_state=42)
        if max_workers > 1:
            return self.concurrent_run(X, Xt, max_workers)
        else:
            return {
                name: format_results(runner.run(X.copy(), Xt.copy()))
                for name, runner in self.runners
            }


def main():
    rinput = LSTMInput(embedding_dim=100,
                       hidden_dim=128,
                       seq_len=512,
                       epochs=3,
                       batch_size=32)
    import jieba
    tok = jieba.lcut
    runners = [
        ('naive bayes', NaiveBayesBinary(jieba.lcut)),
        ('fasttext', FastTextBinary(tok)),
        # ('fasttext pretrained', PretrainedFastTextBinary(word2vec.pull('glove-wiki-gigaword-100'))),
        # ('ligthgbm tfidf', LightgbmBinary()),
        # ('ligthgbm count', LightgbmBinary('count')),
        ('xgboost tfidf', Xgboost()),
        # ('xgboost count', XgboostBinary(vectorizer='count')),
        # ('catboost tfidf', CatboostBinary()),
        # ('voteboost count', VotingBoostBinary(vectorizer='count')),
        # ('catboost count', CatboostBinary(vectorizer='count')),
        # ('lstm', LSTMBinaryClassifier(rinput)),
        # ('bert', BertBinary(epochs=4, batch_size=16, max_len=200, model_name='bert-base-chinese'))
    ]
    # df = pd.read_csv(downloader.imdb()).sample(frac=0.1, random_state=2023)
    # df = pd.read_csv(downloader.twitter_disaster())
    df = pd.read_csv(downloader.chn_senti())
    # df = pd.read_csv(downloader.spam_en())
    manager = Manager(runners, df)
    metrics = manager.run(max_workers=1)
    metrics = manager.rank(metrics)
    print('-' * 20)
    for m in metrics:
        print(m)

