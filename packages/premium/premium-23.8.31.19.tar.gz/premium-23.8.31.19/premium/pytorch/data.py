from abc import ABC, abstractmethod
from typing import Callable

import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset


class BaseDataset(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self):
        pass


class TextDataset(BaseDataset):

    def __init__(self,
                 csv_file: str = None,
                 df: pd.DataFrame = None,
                 tokenizer: Callable = None):
        """ if df is not None, csv_file is ignored 
        otherwise, csv_file is used to load the data
        """
        super().__init__()
        if csv_file is not None:
            self.df = pd.read_csv(csv_file)
        if df is not None:
            self.df = df
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        text = row['text']
        label = row['label']
        if self.tokenizer is None:
            return {'text': text, 'label': label}
        else:
            return {'text': self.tokenizer(text)[0], 'label': label}

    @property
    def text(self):
        return self.df['text']

    @property
    def label(self):
        return self.df['label']


class TrainData(Dataset):

    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return len(self.X_data)


def train_test_val_split(df, test_size=0.2, val_size=0.2, random_state=42):
    X, P = train_test_split(df, test_size=test_size, random_state=random_state)
    V, T = train_test_split(P, test_size=val_size, random_state=random_state)
    return X, V, T


class AbstractLoader(ABC):

    def __init__(self) -> None:
        super().__init__()


class TextLoader(AbstractLoader):

    def __init__(self, dataset, **kargs):
        self._DataSet = dataset
        self.kargs = kargs

    def __call__(self, df: pd.DataFrame, **kargs) -> DataLoader:
        self.kargs.update(kargs)
        return DataLoader(self._DataSet(df), **self.kargs)
