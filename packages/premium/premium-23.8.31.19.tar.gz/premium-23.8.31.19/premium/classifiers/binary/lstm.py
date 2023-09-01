#!/usr/bin/env python3
import random
from typing import Dict

import codefast as cf
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from premium.classifiers.bases import NNModel
from premium.lightning.callbacks import AccLossCallback

from .rnn import LSTMClassifier, TextDataset, Vectorizer

random.seed(42)

# For fast benchmarking specifically


class LSTMClassifierForPrototyping(NNModel):

    def __init__(self,
                 embedding_dim=128,
                 hidden_dim=128,
                 num_classes=2,
                 max_features=10000,
                 max_len=512,
                 epoch=10,
                 tokenizer=None):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        self.max_features = max_features
        self.max_len = max_len
        self.epoch = epoch
        self.tokenizer = tokenizer
        self.name = 'BiLSTM'
        self.vectorizer=None
        assert self.tokenizer is not None, "none tokenizer, use list(x) for chinese and s.split() for English"
        
    def fit(self, X: pd.DataFrame):
        X, Xv = train_test_split(X, test_size=0.2)
        y, yv = X['label'].tolist(), Xv['label'].tolist()
        vectorizer = Vectorizer(max_features=self.max_features,
                                tokenizer=self.tokenizer)
        X = vectorizer.fit_transform(X['text'])
        Xv = vectorizer.transform(Xv['text'])
        self.vectorizer=vectorizer
        vocab_size=vectorizer.vocab_size
        
        X_set = TextDataset(X, y, max_len=self.max_len)
        Xv_set = TextDataset(Xv, yv, max_len=self.max_len)
        X_loader = DataLoader(X_set, batch_size=8, shuffle=True)
        Xv_loader = DataLoader(Xv_set, batch_size=32, shuffle=False)
        checkpoint = ModelCheckpoint(
            dirpath='lightning_logs',
            filename='bilstm_{epoch:02d}_{val_f1:.4f}',
            save_top_k=1,
            verbose=True,
            monitor='val_f1',
            mode='max')

        model = LSTMClassifier(vocab_size, self.embedding_dim,
                               self.hidden_dim, self.num_classes)
        trainer = pl.Trainer(accelerator='auto',
                             max_epochs=self.epoch,
                             callbacks=[AccLossCallback(), checkpoint])
        trainer.fit(model, X_loader, Xv_loader)

        best_model = LSTMClassifier.load_from_checkpoint(
            checkpoint.best_model_path,
            vocab_size=vocab_size,
            embedding_dim=self.embedding_dim,
            hidden_dim=self.hidden_dim,
            num_classes=self.num_classes)

        self.trainer = trainer
        self.best_model = best_model

    def evaluate(self, Xt: pd.DataFrame) -> Dict:
        yv = Xt['label'].tolist()
        Xt = self.vectorizer.transform(Xt['text'])
        Xt_set = TextDataset(Xt, yv, max_len=self.max_len)
        Xt_loader = DataLoader(Xt_set, batch_size=32, shuffle=False)
        preds = self.trainer.predict(self.best_model, Xt_loader)
        preds = [x for b in preds for x in b]
        from premium.classifiers.bases import calculate_metrics
        return calculate_metrics(yv, preds)

    def run(self, X: pd.DataFrame, Xt: pd.DataFrame) -> Dict:
        return self.inner_run(X, Xt)


if __name__ == '__main__':
    from premium import lds 
    imdb = lds('imdb')
    print(imdb)
    df = imdb['train'].to_pandas()
    df.to_csv('/tmp/imdb.csv', index=False)
    lstm = LSTMClassifierForPrototyping(
        embedding_dim=128,
        hidden_dim=128,
        num_classes=2,
        max_features=10000,
        max_len=512,
        epoch=10,
        tokenizer=lambda x: x.split(),
    )
    df = pd.read_csv('/tmp/imdb.csv')
    lstm.fit(df)
