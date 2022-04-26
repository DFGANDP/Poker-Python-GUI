
import numpy as np

class Player():
  def __init__(self, id=0, credits=0):
    '''
    Potem przypisac mu finkcje check call itd
    hand - 2 karty przypisywane z decku
    winner - przypisywane przez check_winner: True or False
    chips - zetony
    uklad - domyslnie 27 (High card)
    sorted_hand - 5 najlepszych kart wybranych z 7

    uklad_card - np. jesli sa dwie pary K oraz Q  to beda te dwie karty
    od najwyzszej jako pierwszej czyli krola.
    Dla kolorow i stritow wogole tego nie ustawiac
    shape 2 a nie (2,2) bo liczy sie tylko figura

    To jest wazne dla ukladów:
    + kareta
    + full
    + trojka
    + dwie pary
    + para
    '''
    self.id = 0
    self.hand = np.zeros((2,2))
    self.winner = False
    self.credits = credits
    self.uklad = 27
    self.sorted_hand = np.zeros((5,2))
    self.hand_figure = np.zeros(2)
    self.blind = None # False - small / True - big
    self.actionp = None
    self.bet = 0

# player_1 = Player()
# reka = player_1.hand
