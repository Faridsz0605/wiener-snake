# import necessary libs

import random

import numpy as np
import torch
from collection import deque
from game import Direction, Point, SnakeGameAI

MAX_MEM = 100_000
BARCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0 # parameter to control randomness
        self.memory = deque(max len=MAX_MEMORY)
        # TO DO 
        pass

    def get_state(self, game):
        pass

    def remeber(self, state, action, reward, next_state, done):
        pass

    def long_mem(self):
        pass

    def short_mem(self):
        pass

    def get_action(self):
        pass

def train():
  plot_score = []
  plot_mean_score = []
  tot_score = []
  record = 0
  agent = Agent()
  game = SnakeGameAI()
  while True:
    state_old = agent.get_state(game)
    
                                final_move = agent.get_action(state_old)
  pass
