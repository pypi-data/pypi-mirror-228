#!/usr/bin/env python

from typing import Dict, List, Tuple

import codefast as cf
import jieba
import pandas as pd
from classifiercluster import Classifiers
from codefast.utils import timeit_decorator
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

from premium.classifiers.bases import Benchmark, TreeModel
from premium.classifiers.multi.lstm import MultiClassLSTM
from premium.classifiers.multi.macbert import Macbert
from premium.classifiers.multi.nb import NaiveBayesMulti
from premium.classifiers.multi.textfast import (FastTextMulti,
                                                PretrainedFastTextMulti)
from premium.classifiers.tree_models import Catboost, Xgboost
from premium.data.datasets import downloader, word2vec

# from premium.classifiers.voting import VotingBoostBinary


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
            'Running concurrent benchmarks with {} workers'.format(max_workers),
            'X size':
            len(X),
        })

        def _submit():
            from concurrent.futures import ProcessPoolExecutor
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                for name, runner in self.runners:
                    yield name, executor.submit(runner.run, X.copy(), Xt.copy())

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
    jieba_tok=jieba.lcut
    runners = [
        ('lstm', MultiClassLSTM(max_epochs=1)),
      ('naive bayes', NaiveBayesMulti(jieba_tok)),
      ('fasttext', FastTextMulti(jieba_tok)),
    #  ('macbert', Macbert(max_length=128, max_epochs=3))
     # ('xgboost count', Xgboost(vectorizer='count')),
     # ('xgboost tfidf', Xgboost()),
     # ('ligthgbm tfidf', Lightgbm()),
     # ('voteboost count', VotingBoostBinary(vectorizer='count')),
     # ('ligthgbm count', Lightgbm('count')),
     # ('catboost tfidf', Catboost()),
     # ('catboost count', Catboost(vectorizer='count')),
     # ('fasttext pretrained', PretrainedFastTextMulti(word2vec.pull('tencent-embedding-200'), jieba_tok)),
    ]

    df = downloader.ten_cats().sample(1000)
    df['text'] = df['text'].astype(str)
    manager = Manager(runners, df)
    metrics = manager.run(max_workers=1)
    metrics = manager.rank(metrics)
    print('-' * 20)
    for m in metrics:
        print(m)


if __name__ == '__main__':
    main()

    