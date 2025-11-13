import torch
import torch.nn as nn
import pytorch_lightning as pl

from architecture import  MaxModelBase,AddModelBase, MaxNumericModelValues, AddNumericModelValues, MeanNumericModelValues, SmoothMaxNumericModelValues , AddNumericActionsModelValues
from architecture import supervised_optimal_loss, selfsupervised_optimal_loss, selfsupervised_suboptimal_loss, selfsupervised_suboptimal2_loss, unsupervised_optimal_loss, unsupervised_suboptimal_loss, l1_regularization
#from architecture.attention_base import AttentionModelBase
#from generators.plan import policy_search

_max_trace_length = 4

def set_max_trace_length(max_length: int):
    global _max_trace_length
    _max_trace_length = max_length

def _create_optimizer(model: nn.Module, learning_rate: float, weight_decay: float):
    return torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

def _create_supervised_model_class(base: pl.LightningModule, loss):
    """Create a model class for supervised training that inherits from 'base' and uses 'loss' for training and validation."""
    class Model(base):
        def __init__(self, predicates: list, hidden_size: int, iterations: int, learning_rate: float, l1_factor: float, weight_decay: float, **kwargs):
            super().__init__(predicates, hidden_size, iterations)
            self.save_hyperparameters('learning_rate', 'l1_factor', 'weight_decay')
            self.learning_rate = learning_rate
            self.l1_factor = l1_factor
            self.weight_decay = weight_decay

        def configure_optimizers(self):
            return _create_optimizer(self, self.learning_rate, self.weight_decay)

        def training_step(self, train_batch, batch_index):
            states, target = train_batch
            output = self(states)
            train = loss(output, target)
            self.log('train_loss', train)
            l1 = l1_regularization(self, self.l1_factor)
            self.log('l1_loss', l1)
            total = train + l1
            self.log('total_loss', total)
            return total

        def validation_step(self, validation_batch, batch_index):
            states, target = validation_batch
            output = self(states)
            validation = loss(output, target)
            self.log('validation_loss', validation)

    return Model

def _create_supervised_model_class_actions_readout(base: pl.LightningModule, loss):
    """Create a model class for supervised training with multiple action outputs that inherits from 'base' and uses 'loss' for training and validation."""
    class Model(base):
        def __init__(self, predicates: tuple, hidden_size: int, iterations: int, learning_rate: float, l1_factor: float, weight_decay: float, **kwargs):
            super().__init__(predicates, hidden_size, iterations)
            self.save_hyperparameters('learning_rate', 'l1_factor', 'weight_decay')
            self.learning_rate = learning_rate
            self.l1_factor = l1_factor
            self.weight_decay = weight_decay

        def configure_optimizers(self):
            return _create_optimizer(self, self.learning_rate, self.weight_decay)

        def training_step(self, train_batch, batch_index):
            states, target = train_batch
            output = self(states)
            # Calculate loss for each action output
            train = torch.mean(torch.stack([loss(output[:, i], target[:, i]) for i in range(output.shape[1])]))
            self.log('train_loss', train)
            l1 = l1_regularization(self, self.l1_factor)
            self.log('l1_loss', l1)
            total = train + l1
            self.log('total_loss', total)
            return total

        def validation_step(self, validation_batch, batch_index):
            states, target = validation_batch
            output = self(states)
            # Calculate validation loss for each action output
            validation = torch.mean(torch.stack([loss(output[:, i], target[:, i]) for i in range(output.shape[1])]))
            self.log('validation_loss', validation)

    return Model

SupervisedOptimalAddModel = _create_supervised_model_class(AddModelBase, supervised_optimal_loss)
SupervisedOptimalMaxModel = _create_supervised_model_class(MaxModelBase, supervised_optimal_loss)
SupervisedOptimalMaxNumericValuesModel = _create_supervised_model_class(MaxNumericModelValues, supervised_optimal_loss)
SupervisedOptimalAddNumericValuesModel = _create_supervised_model_class(AddNumericModelValues, supervised_optimal_loss)
SupervisedOptimalMeanNumerciValuesModel = _create_supervised_model_class(MeanNumericModelValues, supervised_optimal_loss)
SupervisedOptimalSmoothMaxNumericValuesModel = _create_supervised_model_class(SmoothMaxNumericModelValues, supervised_optimal_loss)
SupervisedOptimalAddNumericValuesActionsReadoutModel = _create_supervised_model_class_actions_readout(AddNumericActionsModelValues, supervised_optimal_loss)


