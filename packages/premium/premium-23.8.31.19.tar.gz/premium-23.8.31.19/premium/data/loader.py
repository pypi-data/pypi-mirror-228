#!/usr/bin/env python
import codefast as cf
import pandas as pd

from premium.data.utils import DataGetterFactory, make_obj

try:
    import yaml
except ImportError:
    print('Please install yaml')

from .utils import DataRetriver, Struct, make_obj


def load_yaml(path) -> Struct:
    with open(path) as f:
        return make_obj(yaml.safe_load(f))


def imdb_sentiment() -> Struct:
    """imdb sentiment dataset"""
    x = DataRetriver('https://host.ddot.cc/imdb_sentiment.csv',
                     'sentiment.csv', 'imdb')
    return make_obj(dict(train=x.df))


def spam_en() -> Struct:
    x = DataRetriver('https://host.ddot.cc/spam_en.csv', 'spam_en.csv', 'spam')
    return make_obj(dict(train=x.df))


def loader(dataset_name: str) -> str:
    cli = DataGetterFactory.init(dataset_name)
    if cli:
        cli.exec()
        return cli.get_file_path()
