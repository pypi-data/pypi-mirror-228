#!/usr/bin/env python3
from typing import Any, Dict,Tuple

import codefast as cf
import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset

from premium.classifiers.bases import NNModel, calculate_metrics
from premium.lightning.callbacks import AccLossCallback, ModelSaveCallback
from premium.pytorch.tokenizer import VocabVectorizer


class MultiClassDataset(Dataset):

    def __init__(self, df: pd.DataFrame, vectorizer: VocabVectorizer = None):
        self.texts = df.text
        self.labels = df.label
        self.vectorizer = vectorizer

    @property
    def vocab_size(self):
        return len(self.vectorizer) + 1

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts.iloc[idx]
        label = self.labels.iloc[idx]
        padded_text = self.vectorizer.transform(text)[0]
        tensors = torch.Tensor(padded_text).long()
        return {'text': tensors, 'label': label}


class LSTMClassifier(pl.LightningModule):

    def __init__(self, vocab_size, embedding_dim, hidden_size, num_classes):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
        # save_hyperparameters() is important for load_from_checkpoint
        # https://lightning.ai/docs/pytorch/stable/common/checkpointing_basic.html
        self.save_hyperparameters()

    def forward(self, x):
        embedded = self.embedding(x)
        output, _ = self.lstm(embedded)
        output = self.fc(output[:, -1, :])
        return output

    def common_step(self, batch, batch_idx)->Tuple:
        inputs = batch['text']
        targets = batch['label']
        outputs = self(inputs)
        loss = F.cross_entropy(outputs, targets)
        return loss, outputs, targets

    def training_step(self, batch, batch_idx):
        loss, _outputs, _targets = self.common_step(batch, batch_idx)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, outputs, targets = self.common_step(batch, batch_idx)
        val_acc = (outputs.argmax(1) == targets).float().mean()
        self.log_dict({'val_loss': loss, 'val_acc': val_acc})

    def predict_step(self,
                     batch: Any,
                     batch_idx: int,
                     dataloader_idx: int = 0) -> Any:
        inputs = batch['text']
        outputs = self(inputs)
        return outputs.argmax(1)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=0.001)


class MultiClassLSTM(NNModel):

    def __init__(self,
                 max_len: int = 256,
                 embedding_dim: int = 128,
                 hidden_size: int = 128,
                 max_epochs: int = 10,
                 tokenizer=lambda x: list(x)):
        super().__init__()
        self.vectorizer = VocabVectorizer(max_length=max_len,
                                          padding='post',
                                          tokenizer=tokenizer)
        self.embedding_dim = embedding_dim
        self.hidden_size = hidden_size
        self.max_epochs = max_epochs
        self.name = 'lstm:multiclass'
        self.best_model_path = '/tmp/{}.ckpt'.format(cf.uuid())
        cf.info({
            'max_len': max_len,
            'embedding_dim': embedding_dim,
            'hidden_size': hidden_size,
            'max_epochs': max_epochs,
            'tokenizer': tokenizer,
            'best_model_path': self.best_model_path,
        })

    def fit(self, X):
        self.vectorizer.fit(X.text.tolist())
        dset = MultiClassDataset(X, self.vectorizer)
        X, Xt = train_test_split(dset, test_size=0.1)
        X = DataLoader(X, batch_size=32, num_workers=3)
        Xt = DataLoader(Xt, batch_size=32, num_workers=3)
        self.vocab_size = dset.vocab_size
        self.num_classes = len(dset.labels.unique())

        self.model = LSTMClassifier(self.vocab_size, self.embedding_dim,
                                    self.hidden_size, self.num_classes)
        self.trainer = pl.Trainer(
            accelerator='gpu' if torch.cuda.is_available() else 'cpu',
            max_epochs=self.max_epochs,
            callbacks=[
                AccLossCallback(),
                ModelSaveCallback(self.best_model_path)
            ])
        self.trainer.fit(self.model, X, Xt)

    def evaluate(self, Xt: pd.DataFrame) -> Dict:
        Xt = DataLoader(MultiClassDataset(Xt, self.vectorizer),
                        batch_size=16,
                        num_workers=3)
        model = LSTMClassifier.load_from_checkpoint(self.best_model_path)
        preds = self.trainer.predict(model, Xt)
        preds_flatten = np.concatenate(preds)
        metrics = calculate_metrics(preds_flatten, Xt.dataset.labels)
        return metrics

    def run(self, X, Xt):
        return self.inner_run(X, Xt)


if __name__ == '__main__':
    mcl = MultiClassLSTM(max_epochs=10)
    df = pd.read_csv('data/10cats.csv')
    df['text'] = df['text'].astype(str)
    X, Xt = train_test_split(df, test_size=0.2)
    mcl.run(X, Xt)
