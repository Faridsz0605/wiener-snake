# import necessary libs

import random
from collections import deque

import numpy as np
import torch

from adition import plot
from neurons import Linear_Q, Trainer
from snake import Direction, Point, SnakeGameAI

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.n_games = 0  # <- var to control games played
        self.epsilon = 0  # <- parameter to control randomness
        self.gamma = 0.95  # discount factor (castigo)
        self.memory = deque(maxlen=MAX_MEM)  # <- memory for agent
        self.model = Linear_Q(11, 256, 3)
        self.trainer = Trainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, snake):
        head = snake.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = snake.direction == Direction.LEFT
        dir_r = snake.direction == Direction.RIGHT
        dir_u = snake.direction == Direction.UP
        dir_d = snake.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and snake.is_collision(point_r))
            or (dir_l and snake.is_collision(point_l))
            or (dir_u and snake.is_collision(point_u))
            or (dir_d and snake.is_collision(point_d)),
            # Danger right
            (dir_u and snake.is_collision(point_r))
            or (dir_d and snake.is_collision(point_l))
            or (dir_l and snake.is_collision(point_u))
            or (dir_r and snake.is_collision(point_d)),
            # Danger left
            (dir_d and snake.is_collision(point_r))
            or (dir_u and snake.is_collision(point_l))
            or (dir_r and snake.is_collision(point_u))
            or (dir_l and snake.is_collision(point_d)),
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # Food location
            snake.food.x < snake.head.x,  # food left
            snake.food.x > snake.head.x,  # food right
            snake.food.y < snake.head.y,  # food up
            snake.food.y > snake.head.y,  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def long_mem(self):
        """func for training (long_term_mem)"""
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        # faster way with pytorch
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train(states, actions, rewards, next_states, dones)

    def short_mem(self, state, action, reward, next_state, done):
        """func for training (short_term_mem)"""
        self.trainer.train(state, action, reward, next_state, done)

    def get_action(self, state):
        # exploration/exploitation with exponential decay
        # starts at ~1.0, decays toward 0.01 over ~500 games
        self.epsilon = max(0.01, 1.0 - self.n_games / 500)
        final_move = [0, 0, 0]
        if random.random() < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


def train():
    plot_score = []
    plot_mean_score = []
    tot_score = 0
    record = 0
    agent = Agent()
    snake = SnakeGameAI()
    while True:
        # getting move
        state_old = agent.get_state(snake)
        final_move = agent.get_action(state_old)

        # agent actions
        reward, done, score = snake.play_step(final_move)
        state_new = agent.get_state(snake)
        # first training step
        agent.short_mem(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        if done:
            # training long mem (replay memories)
            snake.reset()
            agent.n_games += 1
            agent.long_mem()

            if score > record:
                record = score
                agent.model.save()

            print(
                f"Game: {agent.n_games} | Score: {score} | Record: {record} | Epsilon: {agent.epsilon:.3f}"
            )

            plot_score.append(score)
            tot_score += score
            mean = tot_score / agent.n_games
            plot_mean_score.append(mean)
            plot(plot_score, plot_mean_score)


if __name__ == "__main__":
    train()
