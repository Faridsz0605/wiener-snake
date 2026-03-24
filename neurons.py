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
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """uses Relu model to learn"""
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name="model.pth"):
        """helper func to save model"""
        mod_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        if not os.path.exists(mod_folder):
            os.makedirs(mod_folder)

        file_name = os.path.join(mod_folder, file_name)
        torch.save(self.state_dict(), file_name)


class Trainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        # 1: predicted Q values with current state
        pred = self.model(state)

        # 2: Q_new = r + y * max(next_predicted Q value) -> only if not done
        # vectorized: single forward pass for ALL next_states at once
        target = pred.clone()
        with torch.no_grad():
            next_pred = self.model(next_state)
            next_max = torch.max(next_pred, dim=1)[0]

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * next_max[idx]

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(pred, target)
        loss.backward()

        self.optimizer.step()
