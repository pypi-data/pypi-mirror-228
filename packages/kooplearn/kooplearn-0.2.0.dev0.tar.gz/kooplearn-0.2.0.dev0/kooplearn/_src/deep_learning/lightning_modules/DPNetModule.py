from typing import Type

import torch
from lightning import LightningModule
from torch import nn


class DPNetModule(LightningModule):
    """Pytorch Lightning module for DPNet feature map.

    Organized as a classical LightningModule check the documentation of Pytorch Lightning for more details. Note that
    in case we do not specify the encoder for the output, we use the same model as the encoder for the input (with
    shared weights).

    Note: We split the class/functions from the keyword arguments to be able to easily save and load the model and
    log the hyperparameters.

    Parameters:
        encoder_input_class: Class of the encoder of the input. Can be any deep learning architecture (torch.nn.Module)
            that takes as input a dictionary containing the key 'x_value', a tensor of
            shape (..., n_features, temporal_dim), and encodes it into a tensor of shape (..., output_dim).
        encoder_input_hyperparameters: Hyperparameters of the encoder. Must be a dictionary containing as keys the
            names of the hyperparameters and as values the values of the hyperparameters of the encoder of the input.
        optimizer_fn: Optimizer function. Can be any torch.optim.Optimizer.
        optimizer_hyperparameters: Hyperparameters of the optimizer. Must be a dictionary containing as keys the names
            of the hyperparameters and as values the values of the hyperparameters of the optimizer.
        scheduler_fn: Scheduler function. Can be any torch.optim.lr_scheduler.LRScheduler.
        scheduler_hyperparameters: Hyperparameters of the scheduler. Must be a dictionary containing as keys the names
            of the hyperparameters and as values the values of the hyperparameters of the scheduler.
        scheduler_config: Configuration of the scheduler. Must be a dictionary containing as keys the names of
            the configuration parameters and as values the values of the configuration parameters of the scheduler.
            See https://lightning.ai/docs/pytorch/stable/common/lightning_module.html#configure-optimizers for more
            information on how to configure the scheduler configuration (lr_scheduler_config in their documentation).
        encoder_output_class: Class of the encoder of the output. Can be any deep learning architecture
            (torch.nn.Module) that takes as input a dictionary containing the key 'x_value', a tensor of
            shape (..., n_features, temporal_dim), and encodes it into a tensor of shape (..., output_dim).
        encoder_output_hyperparameters: Hyperparameters of the encoder. Must be a dictionary containing as keys the
            names of the hyperparameters and as values the values of the hyperparameters of the encoder of the output.
    """
    def __init__(
            self,
            encoder_input_class: Type[nn.Module], encoder_input_hyperparameters: dict,
            optimizer_fn: Type[torch.optim.Optimizer], optimizer_hyperparameters: dict,
            loss_fn,
            scheduler_fn: Type[torch.optim.lr_scheduler.LRScheduler], scheduler_hyperparameters: dict,
            scheduler_config: dict,
            encoder_output_class: Type[nn.Module] = None, encoder_output_hyperparameters: dict = None,
    ):
        super().__init__()
        for k, v in encoder_input_hyperparameters.items():
            self.hparams[f'encoder_input_{k}'] = v
        for k, v in encoder_output_hyperparameters.items():
            self.hparams[f'encoder_output_{k}'] = v
        for k, v in optimizer_hyperparameters.items():
            self.hparams[f'optim_{k}'] = v
        for k, v in scheduler_hyperparameters.items():
            self.hparams[f'sched_{k}'] = v
        for k, v in scheduler_config.items():
            self.hparams[f'sched_{k}'] = v
        self.save_hyperparameters()
        self.encoder_input = encoder_input_class(**encoder_input_hyperparameters)
        # If encoder_output_class is None, the encoder_output is the same as model (with shared weights)
        if encoder_output_class is not None:
            self.encoder_output = encoder_output_class(**encoder_output_hyperparameters)
        else:
            self.encoder_output = self.encoder_input
        self.optimizer_fn = optimizer_fn
        self.scheduler_fn = scheduler_fn
        self.optimizer_hyperparameters = optimizer_hyperparameters
        self.scheduler_hyperparameters = scheduler_hyperparameters
        self.scheduler_config = scheduler_config
        self.loss_fn = loss_fn

    def configure_optimizers(self):
        optimizer = self.optimizer_fn(self.parameters(), **self.optimizer_hyperparameters)
        if self.scheduler_fn is not None:
            scheduler = self.scheduler_fn(optimizer, **self.scheduler_hyperparameters)
            lr_scheduler_config = self.scheduler_config.copy()
            lr_scheduler_config['scheduler'] = scheduler
            return [optimizer], [lr_scheduler_config]
        return optimizer

    def training_step(self, train_batch, batch_idx):
        outputs = self.base_step(train_batch, batch_idx)
        return outputs

    def validation_step(self, valid_batch, batch_idx):
        outputs = self.base_step(valid_batch, batch_idx)
        return outputs

    def forward(self, x_value):
        # dimensions convention (..., channels, temporal_dim)
        return self.encoder_input({'x_value': x_value})

    def base_step(self, batch, batch_idx):
        """Default step (train loop) used for training and validation."""
        # dimensions convention (..., channels, temporal_dim)
        # if any y is out of series, we do not use the sample from the batch
        mask_out_of_series_left = batch['mask_out_of_series_left']
        mask_out_of_series_right = batch['mask_out_of_series_right']
        mask_out_of_series = mask_out_of_series_left | mask_out_of_series_right
        batch_out_of_series = mask_out_of_series.any(dim=-1).any(dim=-1)
        batch_in_series = ~batch_out_of_series
        x_value = batch['x_value'][batch_in_series]
        y_value = batch['y_value'][batch_in_series]
        data_x = {'x_value': x_value}
        data_y = {'x_value': y_value}
        x_encoded = self.encoder_input(data_x)
        # Note that encoder_output is the same as model in case we have not defined a second model
        y_encoded = self.encoder_output(data_y)
        loss = self.loss_fn(x_encoded, y_encoded)
        outputs = {
            'loss': loss,
        }
        return outputs
