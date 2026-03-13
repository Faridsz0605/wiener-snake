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
