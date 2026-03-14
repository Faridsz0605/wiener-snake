# import libs
import os

# pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Linear_Q(nn.Module):
    def __init__(self, input_size, hidden_size, output_size) -> None:
        """defs properties to learn"""
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(input_size, hidden_size)

    def forward(self,x):
        """uses Relu model to learn"""
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        return x

    def save(self, file_name='model.pth'):
