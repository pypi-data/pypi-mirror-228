import os
from tempfile import NamedTemporaryFile as tmpfile
import pandas as pd 
import fasttext

from premium.classifiers.bases import Benchmark, NNModel, calculate_metrics


class FastTextBinary(NNModel):
    """ FastText Binary Classifier
    """
    def __init__(self, tokenizer=None, autotune_duration=120, dim=300):
        super().__init__()
        self.name += ':fasttext'
        self.tokenizer = tokenizer
        self.autotune_duration = autotune_duration
        self.dim=dim 

    def load_model(self, model_path):
        self.model = fasttext.load_model(model_path)

    def fit(self, X):
        X['label'] = '__label__' + X['label'].astype(str)
        X['text'] = X['text'].apply(lambda x: x.replace('\n', ' '))
        X, Xv = X[:int(len(X) * 0.85)], X[int(len(X) * 0.85):]
        with tmpfile() as f:
            X[['label', 'text']].to_csv(f.name, sep='\t', index=False)
            with tmpfile() as fv:
                Xv[['label', 'text']].to_csv(fv.name, sep='\t', index=False)
                parmas = {
                    'input': f.name,
                    'thread': 1,
                    'epoch': 100,
                    'dim': self.dim,
                    'autotuneDuration': self.autotune_duration,
                    'autotuneValidationFile': fv.name,
                }
                self.model = fasttext.train_supervised(**parmas)

    def predict(self, X: list):
        if isinstance(X, pd.DataFrame):
            X = X.text.tolist()
        assert isinstance(X, list), 'X must be a list of texts'
        texts = [x.replace('\n', ' ') for x in X]
        preds = [self.model.predict(x)[0][0] for x in texts]
        preds = [int(x.replace('__label__', '')) for x in preds]
        return preds

    def evaluate(self, Xt):
        texts = [x.replace('\n', ' ') for x in Xt['text']]
        preds = [self.model.predict(x)[0][0] for x in texts]
        preds = [int(x.replace('__label__', '')) for x in preds]
        return calculate_metrics(Xt['label'], preds)

    def preprocess(self, X):
        X['text'] = X['text'].apply(lambda x: ' '.join(self.tokenizer(x))
                                    if self.tokenizer else x)
        return X

    def run(self, X, Xt):
        X, Xt = self.preprocess(X), self.preprocess(Xt)
        return self.inner_run(X, Xt)

    def save(self, path):
        self.model.save_model(path)


class PretrainedFastTextBinary(NNModel):
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
        if pretrained_vector and os.path.exists(pretrained_vector):
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

    def predict(self, X: list):
        assert isinstance(X, list), 'X must be a list of texts'
        texts = [str(x).replace('\n', ' ') for x in X]
        preds = [self.model.predict(x)[0][0] for x in texts]
        preds = [int(x.replace('__label__', '')) for x in preds]
        return preds

    def save(self, path):
        self.model.save_model(path)

    def load_model(self, model_path):
        self.model = fasttext.load_model(model_path)
