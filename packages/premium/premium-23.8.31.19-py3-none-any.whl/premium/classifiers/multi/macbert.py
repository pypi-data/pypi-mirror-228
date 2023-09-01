#!/usr/bin/env python3

import codefast as cf
import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
from pytorch_lightning import LightningModule
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from transformers import BertForSequenceClassification, BertTokenizer

from premium.classifiers.bases import NNModel, calculate_metrics
from premium.lightning.callbacks import (AccLossCallback, ModelSaveCallback,
                                         PretrainedSaveCallback)

MODEL = 'hfl/chinese-macbert-base'


class TextDataset(Dataset):

    def __init__(self, dataframe, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.text = dataframe['text'].tolist()
        self.labels = dataframe['label'].tolist()
        self.max_length = max_length

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        text = str(self.text[index])
        label = self.labels[index]
        encoding = self.tokenizer.encode_plus(text,
                                              add_special_tokens=True,
                                              max_length=self.max_length,
                                              return_token_type_ids=False,
                                              padding='max_length',
                                              return_attention_mask=True,
                                              return_tensors='pt',
                                              truncation=True)
        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }


class TextClassifier(LightningModule):

    def __init__(self, num_labels, learning_rate=2e-5):
        super().__init__()
        self.num_labels = num_labels
        self.learning_rate = learning_rate
        self.criterion = torch.nn.CrossEntropyLoss()
        self.pretrained = BertForSequenceClassification.from_pretrained(
            MODEL, num_labels=self.num_labels)
        self.save_hyperparameters()

    def forward(self, input_ids, attention_mask):
        outputs = self.pretrained(input_ids=input_ids,
                                  attention_mask=attention_mask)
        return outputs.logits

    def training_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['label']
        outputs = self(input_ids, attention_mask)
        loss = self.criterion(outputs, labels)
        self.log('train_loss', loss)
        return loss

    def _metrics(self, preds, labels):
        preds = np.argmax(preds, axis=1)
        return calculate_metrics(preds, labels)

    def validation_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['label']
        outputs = self(input_ids, attention_mask)
        loss = self.criterion(outputs, labels)
        metrics = self._metrics(outputs.detach().cpu().numpy(),
                                labels.cpu().numpy())
        self.log_dict({
            'val_loss': loss,
            'val_precision': metrics['precision'],
            'val_recall': metrics['recall'],
            'val_f1': metrics['f1']
        })
        return loss

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        outputs = self(input_ids, attention_mask)
        return outputs.argmax(dim=1).cpu().numpy()

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.learning_rate)


class Macbert(NNModel):

    def __init__(self,
                 max_length: int = 256,
                 max_epochs: int = 10,
                 batch_size: int = 32,
                 tokenizer=lambda x: list(x)):
        super().__init__()

        self.max_epochs = max_epochs
        self.name = 'macbert:multiclass'
        self.best_model_path = '/tmp/bert'
        self.max_length = max_length
        self.batch_size = batch_size
        self.tokenizer = BertTokenizer.from_pretrained(MODEL)
        self.trainer = pl.Trainer(
            accelerator='gpu' if torch.cuda.is_available() else 'cpu',
            max_epochs=self.max_epochs,
            callbacks=[
                AccLossCallback(),
                ModelSaveCallback(self.best_model_path)
            ])
        cf.info({
            'max_length': max_length,
            'max_epochs': max_epochs,
            'tokenizer': tokenizer,
            'batch_size': batch_size,
            'best_model_path': self.best_model_path,
        })

    def fit(self, X):
        X, Xv = train_test_split(X, test_size=0.1)
        Xd = TextDataset(X, self.tokenizer, max_length=self.max_length)
        Xvd = TextDataset(Xv, self.tokenizer, max_length=self.max_length)
        X = DataLoader(Xd,
                       batch_size=self.batch_size,
                       shuffle=True,
                       num_workers=1)
        Xv = DataLoader(Xvd, batch_size=self.batch_size, shuffle=False)

        # Initialize the classifier
        num_labels = len(set(Xd.labels))
        self.clf = TextClassifier(num_labels=num_labels)
        self.trainer.fit(self.clf, X, Xv)
        cf.info({
            'msg': 'bert training completed',
        })

    def evaluate(self, Xt: pd.DataFrame) -> dict:
        Xt = DataLoader(TextDataset(Xt,
                                    self.tokenizer,
                                    max_length=self.max_length),
                        batch_size=self.batch_size,
                        num_workers=3)
        self.clf = TextClassifier.load_from_checkpoint(self.best_model_path)
        preds = self.trainer.predict(self.clf, Xt)
        preds = np.concatenate(preds)
        metrics = calculate_metrics(preds, Xt.dataset.labels)
        return metrics

    def run(self, X, Xt):
        return self.inner_run(X, Xt)


if __name__ == '__main__':
    from premium.data.datasets import downloader
    fp = downloader.ten_cats()

    df = pd.read_csv(fp).sample(10000)
    X, Xt = train_test_split(df, test_size=0.2, random_state=42)

    mac = Macbert(max_length=128, max_epochs=5)
    # mac.evaluate(Xt)
    mac.run(X, Xt)
