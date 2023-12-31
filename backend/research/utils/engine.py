from pathlib import Path
from typing import Dict, Optional, Union
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
import torch
from torch.utils.data import DataLoader, Dataset
from tqdm.notebook import tqdm


class Trainer:

    best_val_loss: float

    def __init__(self,
            model: torch.nn.Module,
            optimizer: torch.optim.Optimizer,
            criterion: torch.nn.modules.loss._Loss,
            train_dataset: Dataset,
            val_dataset: Optional[Dataset] = None,
            scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
            batch_size: int = 128,
            path: Union[str, Path] = None
            ):
        """Класс для обучение PyTorch моделей

        Parameters
        ----------
        model : torch.nn.Module
            Модель
        optimizer : torch.optim.Optimizer
            Оптимизатор
        criterion : torch.nn.modules.loss._Loss
            Класс ошибки
        train_dataset : Dataset
            Датасет для обучения
        val_dataset : Optional[Dataset], optional
            Датасет для валидации, при наличии будет считаться лосс на нем, и сохраняться модель с лучшим лоссом, by default None
        scheduler : Optional[torch.optim.lr_scheduler.LRScheduler], optional
            Планировщик learning rate, by default None
        batch_size : int, optional
            Размер батча, by default 128
        """
        self.model = model

        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion

        self.train_dataset = train_dataset
        self.val_dataset = val_dataset

        self.batch_size = batch_size

        self.path = path

        self.device = 'cuda:0'
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            self.model = self.model.to(self.device)

        self.global_step = 0
        # self.writer = SummaryWriter()

    def train(self, num_epochs) -> None:
        train_loader = DataLoader(self.train_dataset, shuffle=True, pin_memory=True, batch_size=self.batch_size)

        # валидационный датасет не стоит перемешивать
        val_loader = None
        if self.val_dataset:
            val_loader = DataLoader(self.val_dataset, shuffle=False, pin_memory=True, batch_size=self.batch_size)

        self.best_val_loss = float('inf')

        for epoch in tqdm(range(num_epochs), desc='Training:'):

            self.model.train()
            for batch in tqdm(train_loader, desc=f'Epoch {epoch}'):
                self.training_step(batch)

            if val_loader is not None:
                self.validate(val_loader)

    def training_step(self, batch) -> None:
        self.optimizer.zero_grad()
        loss = self.compute_loss_on_batch(batch).to(self.device)
        loss.backward()
        loss_for_log = loss.item()
        self.optimizer.step()
        if self.scheduler is not None:
            self.scheduler.step()

        # Запись логов
        # Необходима оптимизация, поэтому закомменчено
        """self.writer.add_scalar(
            "loss",
            loss_for_log,
            global_step=self.global_step,
        )

        self.writer.add_scalar(
            "lr",
            torch.tensor(*self.scheduler.get_last_lr()),
            global_step=self.global_step,
        )"""

        self.global_step += 1

    def validate(self, val_loader: DataLoader) -> None:
        self.model.eval()

        val_losses = []
        for batch in tqdm(val_loader, desc='Validating'):
            loss = self.compute_loss_on_batch(batch).to(self.device)
            val_losses.append(loss.item())

        val_loss = np.mean(val_losses)
        if val_loss < self.best_val_loss:
            self.save_checkpoint(self.path)
            self.best_val_loss = val_loss

        """ 
        self.writer.add_scalar(
                "val_loss",
                self.best_val_loss,
                global_step=self.global_step,
            )
        """

    def save_checkpoint(self, path: Union[str, Path]) -> None:
        torch.save(self.model, path)

    def compute_loss_on_batch(self, batch) -> torch.Tensor:
        inputs = batch['input_ids'].to(self.device)
        mask = batch['attention_mask'].to(self.device)
        targets = batch['targets'].to(self.device) 
        outputs = self.model(inputs, mask).to(self.device) 
        loss = self.criterion(outputs, targets).to(self.device)
        return loss


def evaluate_loader(loader: DataLoader, model: torch.nn.Module) -> Dict[str, float]:
    
    with torch.no_grad():
        model.eval()
        N = 0
        total_loss = 0.0
        target_epoch = []
        predicted_epoch = []
        for i, input_ in enumerate(loader):
            inputs = input_['input_ids']
            mask = input_['attention_mask']
            targets = input_['targets']
            outputs = model(inputs, mask).to('cuda')
            N += inputs.shape[0]
            predicted_targets = outputs.argmax(dim=1)
            target_epoch.append(targets.detach().cpu().numpy())
            predicted_epoch.append(predicted_targets.detach().cpu().numpy())
        f1 = f1_score(
            np.concatenate(target_epoch),
            np.concatenate(predicted_epoch),
            average='macro'
        )
        acc = accuracy_score(np.concatenate(target_epoch),
            np.concatenate(predicted_epoch))
        
  
        return {
            'acc': acc,
            'f1': f1,
        }
