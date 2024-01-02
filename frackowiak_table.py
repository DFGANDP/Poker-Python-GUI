
import numpy as np

class Table():
  def __init__(self):
    self.hand = np.zeros((4,2))
    self.turn = 0 # CHODZI O GRACZA =1 player 1 | =2 player 2
    self.round = 0 # pre-flop 0 flop 1 turn 2
