
import numpy as np
from io import StringIO
import pandas as pd

class Table():
  def __init__(self):
    self.hand = np.zeros((5,2))
    self.level = 1
    self.small_blind = 0
    self.big_blind = 0
    self.turn = 0 # CHODZI O GRACZA =1 player 1 | =2 player 2
    self.pot = 0
    self.round = 0 # pre-flop 0 flop 1 turn 2 river 3 summary 4
    self.blind_string = StringIO('''Level.Small blind.Big blind
1.50.100
2.100.200
3.150.300
4.200.400
5.250.500
6.300.600
7.350.700
8.400.800
9.450.900
10.500.1000
11.550.1100
12.600.1200
13.700.1400
14.800.1600
15.900.1800
16.1000.2000
17.1100.2200
18.1200.2400
19.1300.2600
20.1400.2800
''')
    self.blinds_table = pd.read_csv(self.blind_string, sep =".", index_col=0)
