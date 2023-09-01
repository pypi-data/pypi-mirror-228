#!/usr/bin/env python3

from typing import Tuple

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader, random_split
from premium.pytorch.data import TextDataset
from premium.pytorch.tokenizer import VocabVectorizer

class TextDataModule(pl.LightningDataModule):

    def __init__(self, text_data: TextDataset, batch_size: int, seq_len: int):
        """ 
        Args:
            data_file: path to csv file
            batch_size: batch size
            seq_len: maximum sequence length
        """
        super().__init__()
        self.dta = text_data
        self.batch_size = batch_size
        self.seq_len = seq_len
        self.vectorizer = None

    def reset_data(self, text_data: TextDataset):
        self.dta = text_data

    @property
    def vocab_size(self):
        return len(self.vectorizer)

    def setup(self, stage=None):
        dta = self.dta
        if not self.vectorizer:
            self.vectorizer = VocabVectorizer()
            self.vectorizer.fit(dta.text)

        if stage == 'fit':
            xsize = int(0.8 * len(dta))
            self.Xt, self.Xv = random_split(dta, [xsize, len(dta) - xsize])
        if stage == 'test':
            self.Xe = dta
        assert stage in ['fit', 'test'], "stage must be 'fit' or 'test'"

    def train_dataloader(self):
        return DataLoader(self.Xt,
                          batch_size=self.batch_size,
                          shuffle=True,
                          num_workers=4,
                          collate_fn=self.collate_fn)

    def val_dataloader(self):
        return DataLoader(self.Xv,
                          batch_size=self.batch_size,
                          shuffle=False,
                          num_workers=4,
                          collate_fn=self.collate_fn)

    def test_dataloader(self):
        return DataLoader(self.Xe,
                          batch_size=self.batch_size,
                          shuffle=False,
                          num_workers=4,
                          collate_fn=self.collate_fn)

    def collate_fn(self,
                   batch) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        batch.sort(key=lambda x: len(x['text']), reverse=True)
        label = torch.tensor([b['label'] for b in batch])
        text = self.vectorizer.transform([b['text'] for b in batch])
        text_lens = torch.tensor([min(len(t), self.seq_len) for t in text])
        text = [(t + [0] * (self.seq_len - len(t)))[:self.seq_len] for t in text]
        text = torch.tensor(text)
        return text, label, text_lens

