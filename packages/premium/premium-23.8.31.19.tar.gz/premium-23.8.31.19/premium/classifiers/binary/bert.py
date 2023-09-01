#!/usr/bin/env python3

from functools import cached_property
from typing import Dict,List

import codefast as cf
import pandas as pd
import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset, random_split
from transformers import (AutoModelForSequenceClassification, AutoTokenizer, 
                          BertForSequenceClassification, BertTokenizer)

import premium as pm
from premium.classifiers.bases import NNModel
from premium.lightning.callbacks import AccLossCallback
from premium.models.bert import BERTChineseModels, BERTEnglishModels
from premium.metrics import calculate_metrics

try:
    from rich import print
except:
    pass


class TextDataset(Dataset):

    def __init__(self,
                 df: pd.DataFrame,
                 tokenizer: BertTokenizer,
                 max_len: int = 512):
        self.df = df
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.contain_label = 'label' in self.df.columns

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        text = self.df['text'].iloc[idx]
        if self.contain_label:
            label = self.df['label'].iloc[idx]
        else:
            label = 0
        encoded = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        input_ids = encoded['input_ids']
        attention_mask = encoded['attention_mask']
        return {
            'input_ids': input_ids.flatten(),
            'attention_mask': attention_mask.flatten(),
            'label': torch.tensor(label),
        }


class BERTClassifier(pl.LightningModule):

    def __init__(self,
                 model_name=None,
                 num_labels=2,
                 freeze_layer_count: int = None,
                 **kwargs
                 ):
        super().__init__()
        assert model_name is not None, 'model_name must be specified'
        self.save_hyperparameters()
        self.num_labels = num_labels
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=num_labels)
        for k, v in kwargs.items():
            setattr(self, k, v)

        if freeze_layer_count:
            for param in self.model.bert.embeddings.parameters():
                param.requires_grad = False

            for layer in self.model.bert.encoder.layer[:freeze_layer_count]:
                for param in layer.parameters():
                    param.requires_grad = False

        self.predictions = []
        self.references = []
        self.losses = []

    def forward(self, batch):
        input_ids, attention_mask, = batch['input_ids'], batch['attention_mask']
        outputs = self.model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        return logits

    def training_step(self, batch, batch_idx):
        logits = self(batch)
        labels = batch['label']
        loss = F.cross_entropy(logits, labels)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        logits = self(batch)
        labels = batch['label']
        preds = torch.argmax(logits, dim=1)
        # append the second of logis
        self.losses.append(F.cross_entropy(logits, labels))
        self.predictions.append(preds)
        self.references.append(labels)

    def common_epoch_end(self, prefix: str = None):
        predictions = torch.concat(self.predictions).view(-1)
        references = torch.concat(self.references).view(-1)

        yt = predictions.cpu().numpy()
        yp = references.cpu().numpy()
        
        average=self.average if self.average else 'binary'
        outputs = calculate_metrics(yt, yp, average,prefix=prefix)
        outputs['loss'] = torch.stack(self.losses).mean()
        self.losses.clear()
        self.predictions.clear()
        self.references.clear()
        return outputs

    def on_validation_epoch_end(self):
        outputs = self.common_epoch_end(prefix='val')
        outputs['val_loss'] = outputs['loss']
        self.log_dict(outputs, sync_dist=True)
        print(outputs)
        return outputs

    def test_step(self, batch, batch_idx):
        logits, labels = self(batch), batch['label']
        self.losses.append(F.cross_entropy(logits, labels))
        preds = torch.argmax(logits, dim=1)
        self.predictions.append(preds)
        self.references.append(labels)

    def on_test_epoch_end(self):
        outputs = self.common_epoch_end(prefix='test')
        outputs['val_loss'] = outputs['loss']
        self.log_dict(outputs, sync_dist=True)
        return outputs

    def predict_step(self, batch, batch_idx, dataloader_idx=None):
        logits = self(batch)
        preds = torch.argmax(logits, dim=1)
        return preds

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=5e-5, weight_decay=0.005)


class BERTForPrototyping(NNModel):
    """ For benchmarking binary classification with BERT
    """

    def __init__(self,
                 epochs=2,
                 batch_size=64,
                 max_len=200,
                 model_name=None,
                 monitor='val_f1',
                 dirpath=None,
                 checkpoint_prefix=None,
                 checkpoint_path=None,
                 freeze_layers: int = None,
                 num_labels: int = 2,
                    **kwargs
                 ):
        """
        :param epochs: number of epochs,
        :param batch_size: batch size,
        :param max_len: max length of the input text,
        :param model_name: model name of the bert model,
        :param monitor: monitor metric for checkpointing,
        :param dirpath: dirpath for checkpointing,
        :param checkpoint_prefix: prefix for checkpointing,
        """
        super().__init__()
        self.name += ':bert'
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_len = max_len
        self.model_name = model_name
        self.monitor = monitor
        self.dirpath = dirpath if dirpath else 'lightning_logs'
        self.checkpoint_prefix = checkpoint_prefix
        self._best_model = None     # for later offline prediction
        self.freeze_layers = freeze_layers
        self.num_labels = num_labels
        for k, v in kwargs.items():
            setattr(self, k, v)

        assert self.model_name is not None, 'model_name must be specified'

    @cached_property
    def bert_model(self):
        return BERTClassifier(self.model_name,
                              num_labels=self.num_labels,
                              freeze_layer_count=self.freeze_layers,
                              average=self.average)

    @cached_property
    def tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_name)

    def _monitor_filename(self, prefix: str):
        model_name=self.model_name.split('/').pop()
        prefix = '{}_{}'.format(prefix, model_name)
        if self.monitor == 'val_f1':
            return prefix + '_{epoch:02d}_{val_f1:.4f}'
        elif self.monitor == 'val_accuracy':
            return prefix + '_{epoch:02d}_{val_accuracy:.4f}'
        elif self.monitor == 'val_loss':
            return prefix + '_{epoch:02d}_{val_loss:.4f}'
        else:
            raise ValueError('invalid monitor {}'.format(self.monitor))

    @cached_property
    def trainer(self):
        from pytorch_lightning.callbacks import ModelCheckpoint
        f = self.checkpoint_prefix if self.checkpoint_prefix else 'bert'
        f = self._monitor_filename(f)

        checkpoint = ModelCheckpoint(dirpath=self.dirpath,
                                     filename=f,
                                     save_top_k=1,
                                     verbose=True,
                                     monitor=self.monitor,
                                     mode='max',
                                     save_weights_only=True)

        callbacks = [checkpoint]
        return pl.Trainer(accelerator='auto',
                          devices='auto',
                          max_epochs=self.epochs,
                        #   precision='16-mixed',
                          callbacks=callbacks,
                          default_root_dir='/tmp/lightning_logs')

    def create_dataloader(self, df, shuffle=True, batch_size=None):
        ds = TextDataset(df, self.tokenizer, self.max_len)
        if batch_size is None:
            batch_size = self.batch_size
        return DataLoader(ds,
                          batch_size=batch_size,
                          num_workers=4,
                          pin_memory=True,
                          shuffle=shuffle)

    def save(self, config_path: str):
        config = {}
        for k, v in self.__dict__.items():
            try:
                cf.js.write({k:v}, '/tmp/{}.json'.format(k))
                config[k] = v
            except:
                pass
        cf.js.write(config, config_path)

    @classmethod
    def load_from_checkpoint(cls, model_name:str,checkpoint_path:str):
        return cls.load_from_config({
            'epochs': 1,
            'batch_size': 8,
            'max_len': 512,
            'model_name': model_name,
            'monitor': 'val_accuracy',
            'best_checkpoint': checkpoint_path,
            'dirpath': '/tmp'
        })

    @classmethod
    def load_from_config(cls, config: Dict):
        obj = cls(**config)
        obj.best_checkpoint = config['best_checkpoint']
        obj.bert_model = BERTClassifier.load_from_checkpoint(
            checkpoint_path=obj.best_checkpoint, model_name=obj.model_name)
        return obj

    def fit(self, X):
        X, Xv = train_test_split(X, test_size=0.15, random_state=42)
        self.train_loader = self.create_dataloader(X)
        self.val_loader = self.create_dataloader(Xv, shuffle=False)
        self.trainer.fit(self.bert_model, self.train_loader, self.val_loader)
        self.best_checkpoint = self.trainer.checkpoint_callback.best_model_path

    def evaluate(self, Xt: pd.DataFrame) -> Dict:
        preds = self.predict(Xt)
        average=self.average if self.average else 'binary'
        return calculate_metrics(Xt['label'].tolist(), preds,average)

    def _load_best_model(self):
        if self._best_model is None:
            try:
                print({
                    'best checkpoint': self.best_checkpoint,
                    'model name': self.model_name
                })
                self._best_model = BERTClassifier.load_from_checkpoint(
                    checkpoint_path=self.best_checkpoint,
                    model_name=self.model_name)
            except Exception as e:
                cf.warning(e)
                return self.bert_model
        return self._best_model

    def predict(self, Xt: pd.DataFrame, batch_size: int = None) -> List[int]:
        Xt_loader = self.create_dataloader(Xt,
                                           shuffle=False,
                                           batch_size=batch_size)
        best_model = self._load_best_model()
        return [
            e.item()
            for b in self.trainer.predict(best_model, dataloaders=Xt_loader)
            for e in b
        ]

    def run(self, X, Xt):
        return self.inner_run(X, Xt)


if __name__ == '__main__':
    proto = BERTForPrototyping(epochs=1,
                               batch_size=8,
                               max_len=512,
                               model_name=BERTChineseModels.base.value,
                               monitor='val_accuracy',
                               dirpath='/data/tmp/checkpoints')
    textdata = pm.lds('ttxy/sentiment')
    textdata['train'] = textdata['train'].shuffle()
    textdata['test'] = textdata['test'].shuffle()
    df = pd.DataFrame(textdata['train'][:500])
    dv = pd.DataFrame(textdata['test'][:100])
    # X, Xt = train_test_split(df, test_size=0.2, random_state=42)
    x = proto.run(df, dv)
    print(x)
    proto.save('/tmp/model.json')
