#!/usr/bin/env python3
import random

import codefast as cf
import jieba
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from datasets import load_dataset
from pytorch_lightning.callbacks import ModelCheckpoint
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score, precision_score, recall_score
from torch.utils.data import DataLoader, Dataset

from premium.lightning.callbacks import AccLossCallback

random.seed(42)


class LSTMClassifier(pl.LightningModule):

    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_classes):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim,
                            hidden_dim,
                            batch_first=True,
                            bidirectional=True)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        # TODO: use pad_packed_sequence to speed up
        x = self.embedding(x)
        x = self.dropout(x)
        _, (h_n, c_n) = self.lstm(x)
        # Concatenating the last forward and backward LSTM hidden states
        x = torch.cat((h_n[-2, :, :], h_n[-1, :, :]), dim=1)
        x = self.fc(x)
        return x

    def common_step(self, batch, batch_idx):
        x, y = batch
        out = self(x)
        loss = F.cross_entropy(out, y)
        from premium.classifiers.bases import calculate_metrics
        output = calculate_metrics(y.cpu(), out.argmax(dim=1).cpu())
        if 'confusion_matrix' in output:
            del output['confusion_matrix']
        output['acc'] = output['accuracy']
        output['loss'] = loss
        return output

    def training_step(self, batch, batch_idx):
        output = self.common_step(batch, batch_idx)
        train_output = {'train_{}'.format(k): v for k, v in output.items()}
        self.log_dict(train_output)
        return output['loss']

    def validation_step(self, batch, batch_idx):
        output = self.common_step(batch, batch_idx)
        val_output = {'val_{}'.format(k): v for k, v in output.items()}
        self.log_dict(val_output)
        return output['loss']

    def test_step(self, batch, batch_idx):
        output = self.common_step(batch, batch_idx)
        self.log_dict(output, on_epoch=True)
        return output['loss']

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        x, y = batch
        out = self(x)
        return out.argmax(dim=1)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)


class TextDataset(Dataset):

    def __init__(self, X, y, max_len=1024, padding=True):
        self.X = X
        self.y = y
        self.padding = padding
        self.max_len = max_len

    def __getitem__(self, idx):
        x = self.X[idx]
        if self.padding:
            x = x[:self.max_len]
            x = x + [0] * (self.max_len - len(x))
        return torch.LongTensor(x), self.y[idx]

    def __len__(self):
        return len(self.y)


class Vectorizer(BaseEstimator, TransformerMixin):

    def __init__(self, max_features=40000, tokenizer=None):
        self.max_features = max_features
        self.vocab = None
        self.vocab_size = max_features
        self.tokenizer = tokenizer
        if self.tokenizer is None:
            self.tokenizer = lambda x: x.split(' ')

    def fit(self, X, y=None):
        self.vocab = {'<UNK>': 0}
        word_counts = {}
        for x in X:
            for w in self.tokenizer(x):
                word_counts[w] = word_counts.get(w, 0) + 1

        sorted_words = sorted(word_counts.items(),
                              key=lambda x: x[1],
                              reverse=True)
        top_words = sorted_words[:self.max_features -
                                 1]     # Exclude the <UNK> token

        for idx, (word, _count) in enumerate(top_words, 1):
            self.vocab[word] = idx

        cf.info({'vocab_size': len(self.vocab)})
        self.vocab_size = len(self.vocab)
        return self

    def transform(self, X, y=None):
        X = [[self.vocab.get(w, 0) for w in self.tokenizer(x)] for x in X]
        return X


""" S-LSTM 2018 accuracy=0.8715, distilBERT=0.9282
My own BiLSTM best acc=0.8793, vocab_size=40000, max_len=2000, layer=3, date=20230816
https://paperswithcode.com/sota/sentiment-analysis-on-imdb
"""


class AbstractReader(object):

    def __init__(self, max_features=50000, max_len=1024):
        self.max_features = max_features
        self.max_len = max_len

    def process(self):
        raise NotImplementedError


class IMDBReader(AbstractReader):

    def __init__(self, max_features=50000, max_len=1024):
        super().__init__(max_features=max_features, max_len=max_len)
        self.vectorizer = Vectorizer(max_features=max_features)

    def _fetch_data(self):
        dataset = load_dataset('imdb')
        print(dataset)

        dataset['train'] = dataset['train'].shuffle()
        dataset['test'] = dataset['test'].shuffle()
        X = dataset['train']['text']
        y = dataset['train']['label']
        Xv = dataset['test']['text']
        yv = dataset['test']['label']
        return X, y, Xv, yv

    def process(self):
        X, y, Xv, yv = self._fetch_data()
        X = self.vectorizer.fit_transform(X)
        Xv = self.vectorizer.transform(Xv)

        train_dataset = TextDataset(X, y, max_len=self.max_len)
        val_dataset = TextDataset(Xv, yv, max_len=self.max_len)
        test_dataset = val_dataset
        train_dataloader = DataLoader(train_dataset,
                                      batch_size=32,
                                      shuffle=True)
        val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        return train_dataloader, val_dataloader, test_dataloader


class CSVTextReader(AbstractReader):

    def __init__(self,
                 max_features=50000,
                 max_len=1024,
                 tokenizer=None,
                 train_path: str = None,
                 test_path: str = None):
        super().__init__(max_features=max_features, max_len=max_len)
        self.vectorizer = Vectorizer(max_features=max_features,
                                     tokenizer=tokenizer)
        self.train_path = train_path
        self.test_path = test_path
        assert train_path is not None, "train_path is None"
        assert test_path is not None, "test_path is None"

    def _fetch_data(self):
        import pandas as pd
        X = pd.read_csv(self.train_path)
        Xt = pd.read_csv(self.test_path)
        y = X['label'].tolist()
        X = X['text'].tolist()
        yv = Xt['label'].tolist()
        Xv = Xt['text'].tolist()
        return X, y, Xv, yv

    def process(self):
        X, y, Xv, yv = self._fetch_data()
        X = self.vectorizer.fit_transform(X)
        Xv = self.vectorizer.transform(Xv)

        train_dataset = TextDataset(X, y, max_len=self.max_len)
        val_dataset = TextDataset(Xv, yv, max_len=self.max_len)
        test_dataset = val_dataset
        train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
        val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        return train_dataloader, val_dataloader, test_dataloader


def fast_prototyping(embedding_dim=128,
                     hidden_dim=128,
                     num_classes=2,
                     max_features=10000,
                     max_len=512,
                     epoch=10):
    tokenizer = lambda x: list(x)
    reader = IMDBReader(max_features=max_features, max_len=max_len)
    # reader = CSVTextReader(max_features=max_features,
    #                        max_len=max_len,
    #                        tokenizer=tokenizer,
    #                        train_path='data/binary/train.csv',
    #                        test_path='data/binary/test.csv')
    train_dataloader, val_dataloader, test_dataloader = reader.process()

    model = LSTMClassifier(reader.vectorizer.vocab_size, embedding_dim,
                           hidden_dim, num_classes)
    checkpoint = ModelCheckpoint(
        dirpath='lightning_logs',
        filename='best-checkpoint-{epoch:02d}-{val_acc:.4f}',
        save_top_k=1,
        verbose=True,
        monitor='val_acc',
        mode='max')

    trainer = pl.Trainer(accelerator='auto',
                         max_epochs=epoch,
                         callbacks=[AccLossCallback(), checkpoint])
    trainer.fit(model, train_dataloader, val_dataloader)
    best_model = LSTMClassifier.load_from_checkpoint(
        checkpoint.best_model_path,
        vocab_size=reader.vectorizer.vocab_size,
        embedding_dim=embedding_dim,
        hidden_dim=hidden_dim,
        num_classes=num_classes)
    resp = trainer.test(best_model, test_dataloader)
    print(resp)
    return trainer


if __name__ == '__main__':
    fast_prototyping(embedding_dim=128,
                     hidden_dim=128,
                     num_classes=2,
                     max_features=10000,
                     max_len=512,
                     epoch=10)
