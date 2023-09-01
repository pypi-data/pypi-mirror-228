from sklearn.model_selection import train_test_split
import torch
from torch import nn
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from sklearn.datasets import load_iris

from premium.lightning.callbacks import AccLossCallback


class IrisData(pl.LightningDataModule):
    def __init__(self):
        super().__init__()
        self.data = load_iris()
        X, y = self.data.data, self.data.target
        X, Xt, y, yt = train_test_split(X, y, test_size=0.2, random_state=42)
        self.x = X
        self.y = y
        self.xt = Xt
        self.yt = yt

    def setup(self, stage=None):
        self.x = torch.tensor(self.x, dtype=torch.float32)
        self.y = torch.tensor(self.y, dtype=torch.int64)
        self.xt = torch.tensor(self.xt, dtype=torch.float32)
        self.yt = torch.tensor(self.yt, dtype=torch.int64)

    def train_dataloader(self):
        return DataLoader(list(zip(self.x, self.y)), batch_size=32)

    def val_dataloader(self):
        return DataLoader(list(zip(self.xt, self.yt)), batch_size=32)


class MLP(pl.LightningModule):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 3)
        )
        self.ce = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.layers(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        y_hat = self.layers(x)
        loss = self.ce(y_hat, y)
        self.log('train_loss', loss)
        return {'train_loss': loss, 'loss': loss}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-4)
        return optimizer

    def validation_step(self, batch, batch_idx):
        x, y = batch
        x = x.view(x.size(0), -1)
        y_hat = self.layers(x)
        loss = self.ce(y_hat, y)
        accuracy = (y_hat.argmax(dim=1) == y).float().mean()
        metric = {'val_loss': loss, 'val_acc': accuracy}
        self.log_dict(metric)
        return metric


if __name__ == '__main__':
	model = MLP()
	data = IrisData()
	callbacks = [AccLossCallback()]
	trainer = pl.Trainer(gpus=1, max_epochs=20, callbacks=callbacks)
	trainer.fit(model, data)
