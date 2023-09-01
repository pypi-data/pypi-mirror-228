import numpy as np
import pytorch_lightning as pl
import torch
from torch.optim.lr_scheduler import LambdaLR

class LightningBase(pl.LightningModule):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learning_rate = 1e-4
        self.warmup_steps = 100

    def on_epoch_start(self):
        print(
            f'progress: epoch {self.current_epoch+1}/{self.trainer.max_epochs}')

    def configure_optimizers(self):
        # refer: https://github.com/Lightning-AI/lightning/issues/328
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        
        def lr_lambda(current_step):
            if current_step < self.warmup_steps:
                return float(current_step) / float(max(1, self.warmup_steps))
            else:
                return 1.0
        
        scheduler = LambdaLR(optimizer, lr_lambda=lr_lambda)
        
        return [optimizer], [scheduler]

