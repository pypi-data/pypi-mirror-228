#!/usr/bin/env python3
import ast
from typing import Dict, List

import codefast as cf
import pandas as pd
import torch
from datasets import load_dataset
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, BertTokenizer

from premium.models.bert import BERTChineseModels
from premium.preprocessing.ner import TagValueFormer


class NerTextDataSet(torch.utils.data.Dataset):
    """NER text dataset.
    """

    def __init__(self,
                 texts: List[str],
                 labels: List[str],
                 tokenizer,
                 max_len: int = 512,
                 for_train: bool = True):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.for_train = for_train

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        input_ids, attention_mask, labels = [101], [1], [0]
        words = self.texts[idx]
        for i, t in enumerate(words[:self.max_len - 2]):
            # tokenize will convert a work to a list of subwords,
            # e.g., 'unimportant' -> ['un', '##im', '##port', '##ant']
            # Also, tokenize('\n') return [], be careful.
            if not self.tokenizer.tokenize(t):
                token_ids = [self.tokenizer.unk_token_id]
            else:
                token_ids = self.tokenizer.encode(t, add_special_tokens=False)

            for x in token_ids:
                input_ids.append(x)
                attention_mask.append(1)
                if self.for_train:
                    labels.append(self.labels[idx][i])

        input_ids.append(102)
        attention_mask.append(1)
        padding_len = self.max_len - len(input_ids)
        input_ids += [0] * padding_len
        attention_mask += [0] * padding_len
        if self.for_train:
            labels.append(0)
            labels += [0] * padding_len
            return {
                'input_ids': torch.tensor(input_ids),
                'attention_mask': torch.tensor(attention_mask),
                'labels': torch.tensor(labels),
            }
        else:
            return {
                'input_ids': torch.tensor(input_ids),
                'attention_mask': torch.tensor(attention_mask),
            }


class NerTextDataSetForPrediction(NerTextDataSet):

    def __init__(self, texts, tokenizer, max_len: int = 256):
        super().__init__(texts, None, tokenizer, max_len, False)


def parse_list(s: str):
    return ast.literal_eval(s)


def tostr(tags):
    return ''.join(tags)


def load_data(train_path, test_path):
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    X_train = list(map(parse_list, train['tokens']))
    y_train = list(map(parse_list, train['tags']))
    X_test = list(map(parse_list, test['tokens']))
    y_test = list(map(parse_list, test['tags']))
    return X_train, y_train, X_test, y_test


class DataCreator(object):

    @staticmethod
    def from_path(x_path: str,
                  xv_path: str = None,
                  model_name: str = 'bert-base-chinese',
                  max_len: int = 512,
                  batch_size: int = 8) -> Dict:
        X, y, Xv, yv = load_data(x_path, xv_path)
        return DataCreator.from_dataframe(X, y, Xv, yv, model_name, max_len,
                                          batch_size)

    @staticmethod
    def from_dataframe(X,
                       y,
                       Xv,
                       yv,
                       model_name: str = None,
                       max_len: int = 512,
                       batch_size: int = 8) -> Dict:
        tagformer = TagValueFormer(y + yv)
        y, yv = tagformer.transform(y), tagformer.transform(yv)
        num_classes = len(tagformer)

        tokenizer = BertTokenizer.from_pretrained(model_name)
        train_dataset = NerTextDataSet(X, y, tokenizer, max_len=max_len)
        train_loader = DataLoader(train_dataset,
                                  batch_size=batch_size,
                                  shuffle=True,
                                  num_workers=2)
        val_dataset = NerTextDataSet(Xv, yv, tokenizer, max_len=max_len)
        valid_loader = DataLoader(val_dataset,
                                  batch_size=batch_size,
                                  num_workers=2)
        return {
            'train': train_loader,
            'validation': valid_loader,
            'tagformer': tagformer,
            'num_classes': num_classes
        }


def resume_ner(model_name: str = BERTChineseModels.base.value,
               train_batch_size: int = 8,
               valid_batch_size: int = 4,
               slice: int = None) -> dict:
    """ https://www.huggingface.co/datasets/ttxy/resume_ner
    """
    ner = load_dataset('ttxy/resume_ner')
    train, test = ner['train'], ner['test']
    X = [x.split(' ') for x in train['text']]
    y = [x.split(',') for x in train['label']]
    Xv = [x.split(' ') for x in test['text']]
    yv = [x.split(',') for x in test['label']]
    cf.info({
        'len of X': len(X),
        'len of Xt': len(Xv),
        'message': 'Resume NER data'
    })
    if slice:
        X, y, Xv, yv = X[:slice], y[:slice], Xv, yv
    tagformer = TagValueFormer(y + yv)
    y_values, yv_values = tagformer.transform(y), tagformer.transform(yv)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    train_dataset = NerTextDataSet(X, y_values, tokenizer, max_len=512)
    train_loader = DataLoader(train_dataset,
                              batch_size=train_batch_size,
                              shuffle=True,
                              num_workers=4)
    val_dataset = NerTextDataSet(Xv, yv_values, tokenizer, max_len=512)
    val_loader = DataLoader(val_dataset,
                            batch_size=valid_batch_size,
                            shuffle=False,
                            num_workers=4)
    return {
        'train': train_loader,
        'validation': val_loader,
        'tagformer': tagformer,
        'X': X,
        'y': y,
        'Xv': Xv,
        'yv': yv,
    }
