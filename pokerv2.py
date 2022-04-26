# -*- coding: utf-8 -*-
"""Pokerv4

    https://colab.research.google.com/drive/14aZwMwR77tScp2jqVhkEagAZ1tx2FMYE

~DFGANDP
"""


import numpy as np
import pandas as pd
from io import StringIO
import random
from player import Player
from table import Table
from CardDeck import CardDeck


class PokerGame():
  '''
  Glowne zmiany do wprowadzenia
  Operowanie na obiektach glownych z klas chodzi o Player a nie rekach
  zwracanie 5 kart z 7 posortowanych tworzacych najlepszy uklad
  '''
  def __init__(self):
    self.player_1 = Player(1,5000)
    self.player_2 = Player(2,5000)
    self.table = Table()
    self.poker_hands = {
        18 : "royal_poker",
        19 : "poker",
        20 : "kareta",
        21 : "full",
        22 : "kolor",
        23 : "strit",
        24 : "trojka",
        25 : "dwie pary",
        26 : "para",
        27 : "wysoka karta"
    }

    # For Debugging
    self.color_hand = np.array([[2,14],[3,15],[5,14],[10,14],[5,16],[11,14],[12,14]]) # DZWONEK KOLOR

    self.strit_hand = np.array([[6,14],[3,15],[5,16],[10,14],[7,16],[11,15],[4,14]]) #  OD Q do 8 STRIT

    self.royal_poker_table = np.array([[1,15],[3,15],[10,14],[4,15],[11,14]]) # ROYAL POKER SERCE
    self.royal_poker_player = np.array([[2,15],[5,15]]) # ROYAL POKER SERCE

    self.poker_table = np.array([[3,15],[4,15],[10,14],[4,17],[7,15]]) #  POKER SERCE
    self.poker_player = np.array([[5,15],[6,15]]) #  POKER SERCE

    self.kareta_table = np.array([[2, 17],[2, 16],[5, 17],[2, 15],[10, 17]])
    self.kareta_player = np.array([[2, 14],[1, 17]])

    self.full_table = np.array([[2, 17],[2, 16],[5, 17],[9, 15],[10, 17]])
    self.full_player = np.array([[2, 14],[9, 17]])

    self.three_table = np.array([[2, 17],[2, 16],[1, 17],[10, 15],[10, 17]])
    self.three_player = np.array([[2, 14],[9, 17]])

    self.twopair_table = np.array([[1, 17],[2, 16],[2, 17],[4, 15],[5, 17]]) # dwie Pary
    self.twopair_player = np.array([[5, 14],[13, 17]]) #  dwie Pary

    self.pair_table = np.array([[6, 17],[3, 16],[5, 17],[10, 15],[10, 17]]) # Para i dwie Pary
    self.pair_player = np.array([[6, 14],[9, 17]]) # Para i dwie Pary

  def give_cards(self, object, deck):
    '''
    object - table or player
    '''
    index = []
    #print(deck.shape)
    for i in range(len(object)):
      #print(i)
      #print(object[i])
      #print(deck[i])
      object[i] = deck[i]
      #print(object[i])
      index.append(i)
    #print(index)
    deck = np.delete(deck, index, 0) # TRZEBA PODAC OS
    #print(deck.shape)
    return object, deck

  def sort_cards(self, cards_array):
    '''
    [ 1. 14.]
    [ 7. 15.]
    [ 3. 15.]
    [ 8. 14.]
    [ 5. 17.]
    1 liczba - figura
    2 liczba - kolor
    1 - 13 figury IM NIZSZA LICZBA TYM SLABSZA FIGURA
    14 - 17 kolory

    bierze cards_array[0][0] im wieksze tym bardziej pierwsze w ciagu

    '''

    new_order = np.zeros(shape=(cards_array.shape))
    new_index = 0
    for figure in CardDeck().figure_dict:
      for card in cards_array:
        card_figure = card[0]
        if figure == card_figure:
          #print("ZNALAZLEM {} DLA {}".format(figure, card_figure))
          new_order[new_index] = card
          new_index += 1
    #new_order = new_order[::-1] # Czemu to sie w odwrotnej zapisuje ?
    return new_order

  def check_hand(self, player, table):
    '''
    IN: player, table(cards)
    OUT: uklad(numer), card_tab, player_hand
    przypisuje odrazu do klasy te atrybuty
    '''
    table_cards = table.hand
    player_cards = player.hand
    card_to_check = np.concatenate((table_cards, player_cards), axis=0)
    sorted = self.sort_cards(card_to_check)
    #print(sorted)

    color_value, card_tab = self.is_color(card_to_check) # sprawdz kolor i zwroc karty ktore go daja (card_tab)

    '''
    Wyzej 2 liniki ! is_color
    sprawdzic czy jak dam 6 kart
     to zwroci tylko jedno miejsce zerowe !
    '''
    if color_value != False and type(card_tab) != bool: # To jest bardziej wydajne niz odrazu sprawdzac Strit !
      strit_value, first_card = self.is_strit(card_tab) # Wrzucam card-tab bo to karty ktore moga utworzyc pokera (z 1 koloru)
    else:
      pass

    # ROYAL POKER
    if color_value == 22 and strit_value == 23 and first_card == 1.:
      player.uklad = 18
      player.sorted_hand = card_tab
      player.hand_figure[0] = card_tab[0][0]
      return hand, card_tab[0], card_tab

    # POKER
    if color_value == 22 and strit_value == 23 and first_card != 1.:
      # karte najwyzsza tworzaca
      player.uklad = 19
      player.sorted_hand = card_tab
      player.hand_figure[0] = card_tab[0][0]
      return hand, card_tab[0], card_tab

    # KARETA
    hand, kareta_figure, cards_kareta = self.is_fourth(sorted)
    if hand == 20:
      player.uklad = 20
      player.sorted_hand = cards_kareta
      player.hand_figure[0] = kareta_figure
      return 20, kareta_figure, cards_kareta

    # FULL
    hand, hand_figures, player_hand = self.is_full(sorted)
    if hand == 21:
      player.uklad = 21
      player.sorted_hand = player_hand
      player.hand_figure[0] = hand_figures[0]
      player.hand_figure[1] = hand_figures[1]
      return 21, hand_figures, player_hand

    # KOLOR
    if color_value == 22:
      player.uklad = 21
      player.sorted_hand = card_tab
      return 22, card_tab[0], card_tab

    #STRIT
    strit_value, first_card = self.is_strit(sorted) # jeszcze raz bo z 7 kart a nie 2 ! (roznokolorowy)
    if strit_value == 23:
      player.uklad = 23
      player.hand_figure[0] = first_card
      return 23, first_card
    elif strit_value == False:
      pass

    #TROJKA
    hand, trojka_figure, cards_trojka = self.is_trojka(sorted)
    if hand == 24:
      player.uklad = 24
      player.sorted_hand = cards_trojka
      print(trojka_figure)
      player.hand_figure[0] = trojka_figure
      return 24, trojka_figure, cards_trojka

    #DWIE PARY
    hand, hand_figures, player_hand = self.is_two_pairs(sorted)
    if hand == 25:
      player.uklad = 25
      player.sorted_hand = player_hand
      player.hand_figure[0] = hand_figures[0]
      player.hand_figure[1] = hand_figures[1]
      return 25, hand_figures, player_hand

    #PARA
    hand, para_figure, cards_para = self.para(sorted)
    if hand == 26:
      player.uklad = 26
      player.sorted_hand = cards_para
      player.hand_figure[0] = para_figure[0]
      hand = 26
      return 26, para_figure, cards_para

    #WYSOKA KARTA
    player.uklad = 27
    player.sorted_hand = sorted[:5]
    return 27, False # musza byc 2 zmienne bo printuje na podstawie zwrot[0]

  def is_fourth(self, cards_array):
    cards_figures = cards_array[:,0]
    # print(cards_figures)
    # Wyupluwa w posortowanej kolejnosci (unique, counts)
    unique, counts = np.unique(cards_figures, return_counts=True)
    wynik = dict(zip(unique, counts))

    # Kareta
    # print(cards_array.shape)
    for element in wynik: # element to figura !!
      szukaj = wynik[element]
      if szukaj == 4:
        indexy_karety = np.where(cards_figures == element)
        cards_kareta = np.take(cards_array, indexy_karety, axis=0) # 4 karty do karety
        kareta_figure = cards_kareta[0][0]
        cards_kareta = cards_kareta[0,:,:]

        cards_array = np.delete(cards_array, indexy_karety, axis=0) # Usuwam z array
        y = np.expand_dims(cards_array[0], axis=0)

        cards_kareta = np.concatenate((cards_kareta, y), axis=0)
        cards_kareta = self.sort_cards(cards_kareta)
    # Przypisac to do Gracza
        return 20, kareta_figure, cards_kareta
    return False, False, False

  def is_trojka(self, cards_array):
    '''
    Taki sam schemat dzialania jak w karecie tylko zmienione na trojke
    Czyli dodanie 2 najlepszych kart z cards_array do trojki
    '''
    cards_figures = cards_array[:,0]
    # print(cards_figures)
    # Wyupluwa w posortowanej kolejnosci (unique, counts)
    unique, counts = np.unique(cards_figures, return_counts=True)
    wynik = dict(zip(unique, counts))
    for element in wynik: # element to figura !!
      szukaj = wynik[element]
      if szukaj == 3: # sprawdzic czy zwroci 5 kart bo nie powinno
        indexy_trojki = np.where(cards_figures == element)
        cards_trojka = np.take(cards_array, indexy_trojki, axis=0) # 3 karty do trojki
        cards_trojka = cards_trojka[0,:,:] # usun 3 WYMIAR
        # print(cards_trojka)
        trojka_figure = cards_trojka[0][0]
        # print(trojka_figure)

        cards_array = np.delete(cards_array, indexy_trojki, axis=0) # Usuwam z array
        y = cards_array[:2]

        cards_trojka = np.concatenate((cards_trojka, y), axis=0)
        cards_trojka = self.sort_cards(cards_trojka)
        # print(cards_trojka.shape)
        return 24, trojka_figure, cards_trojka
    return False, False, False

  def para(self, cards_array):
    '''
    Taki sam schemat dzialania jak w karecie tylko zmienione na pare
    Czyli dodanie 3 najlepszych kart z cards_array do pary
    '''
    cards_figures = cards_array[:,0]
    # print(cards_figures)
    # Wyupluwa w posortowanej kolejnosci (unique, counts)
    unique, counts = np.unique(cards_figures, return_counts=True)
    wynik = dict(zip(unique, counts))
    #print("wynik {}".format(wynik))
    #print(len(wynik))
    for element in wynik: # element to figura !!
      szukaj = wynik[element]
      #print("szukaj {}".format(szukaj))
      if szukaj == 2: # sprawdzic czy zwroci 5 kart bo nie powinno
        #print("ZNALAZLEM SE 2 KURWA")
        indexy_dwojki = np.where(cards_figures == element)
        cards_dwojka = np.take(cards_array, indexy_dwojki, axis=0) # 2 karty do dwojki
        dwojka_figure = cards_dwojka[0][0]
        cards_dwojka = cards_dwojka[0,:,:]
        cards_array = np.delete(cards_array, indexy_dwojki, axis=0) # Usuwam z array
        y = cards_array[:3] # Bo 3 karty dodaje

        cards_dwojka = np.concatenate((cards_dwojka, y), axis=0)
        cards_dwojka = self.sort_cards(cards_dwojka)
        #print(cards_dwojka.shape)
        return 26, dwojka_figure, cards_dwojka
    return False, False, False

  def is_two_pairs(self, cards_array):
    cards_figures = cards_array[:,0]
    # Sprawdza ile razy pojawia sie jaki element
    unique, counts = np.unique(cards_figures, return_counts=True)
    card_dict = dict(zip(unique, counts))
    # znajdz klucze ktore maja wartosc
    # print(card_dict)
    # print(type(card_dict))
    pairs = [k for k,v in card_dict.items() if v == 2] # Rozkminic i zrozumiec ten zapis
    if len(pairs) == 2:
      hand_figure_1 = pairs[0]
      hand_figure_2 = pairs[1]
      hand_figures = hand_figure_1, hand_figure_2
      player_hand = np.zeros((5,2))
      player_hand[0][0] = pairs[0]
      player_hand[1][0] = pairs[0]
      player_hand[2][0] = pairs[1]
      player_hand[3][0] = pairs[1]
      cards_figures = cards_figures[cards_figures != pairs[0]]
      cards_figures = cards_figures[cards_figures != pairs[1]]
      player_hand[4][0] = cards_figures[0]
      player_hand = np.sort(player_hand, axis=0) # sortowanie
      return 25, hand_figures, player_hand
    return False, False, False

  def is_full(self, cards_array):
    '''
    kolory trzeba dodac bo maja znaczenie w reifnorcment learning jako typ danych
    '''
    cards_figures = cards_array[:,0]
    # Sprawdza ile razy pojawia sie jaki element
    unique, counts = np.unique(cards_figures, return_counts=True)
    card_dict = dict(zip(unique, counts))
    # znajdz klucze ktore maja wartosc
    # print(card_dict)
    # print(type(card_dict))
    pairs = [k for k,v in card_dict.items() if v == 2] # Rozkminic i zrozumiec ten zapis
    triple = [k for k,v in card_dict.items() if v == 3]
    if len(pairs) >= 1 and len(triple) >= 1:
      hand_figure_1 = triple[0]
      hand_figure_2 = pairs[0]
      hand_figures = hand_figure_1, hand_figure_2
      player_hand = np.zeros((5,2))
      player_hand[0][0] = pairs[0]
      player_hand[1][0] = pairs[0]
      player_hand[2][0] = triple[0]
      player_hand[3][0] = triple[0]
      player_hand[4][0] = triple[0]
      player_hand = np.sort(player_hand, axis=0) # sortowanie
      return 21, hand_figures, player_hand
    else:
      return False, False, False

  def is_color(self, cards_array):
    '''
    Sprawdza czy jest kolor jesli tak zwraca wartosc ze slownika dla koloru
    oraz podaje indeksy kart w tablicy ktore na kolor sie skladaja
    dlatego lepiej wczesniej posegregowac
    '''
    for kolor in CardDeck().color_dict:
      color_count=0
      card_index = 0
      card_tab = np.zeros(shape=(cards_array.shape))
      for card in cards_array:
        card_color = card[1]
        if kolor == card_color:
          color_count +=1
          card_tab[card_index] = card
        else:
          pass
        card_index +=1
        if color_count == 5:
          # print("Jest kolor {}!".format(CardDeck().color_dict[kolor]))
          #print(card_tab)
          # Usun 2 ostatnie miejsca
          card_tab = card_tab[:-2] # Usuwa 2 najnizsze karty z 7
          # Zakladam ze zwraca posortowane
          return 22, card_tab
    return False, False

  def is_strit(self, cards_array):
    '''
    W testowym jest strit 7 6 5 4 3
    [[11. 15.]
    [10. 14.]
    [ 7. 16.]
    [ 6. 14.]
    [ 5. 16.]
    [ 4. 14.]
    [ 3. 15.]]

    Sprawdza czy jest strit
    Zwraca 23 czyli numer strita i najwiesza karte w stricie
    '''
    # sorted = self.sort_cards(cards_array) W CHECK HAND WRZUCILEM SORTOWANIE JUZ
    strit = cards_array[:,0]
    # print(strit) # [11. 10.  7.  6.  5.  4.  3.]
    count = 0
    first_element = 0
    for i in range(len(strit)-1): # float 64
      if strit[i] - strit[i+1] == -1: # Dlatego ze As ma 1 Krol ma 2 wiec A-K = -1
        count += 1
        first_element += 1
        if first_element == 1:
          fcard_strit = strit[i]
      else:
        count = 0
        first_element = 0
        fcard_strit = 0
      if count == 4:
        # print("Jest strit")
        # print(fcard_strit)
        return 23 , fcard_strit
    return False, False

  def check_winner(self):
    '''
    wyjebac to do innego folderu wogole i chuj
    Dla wiekszej ilosci graczy bedzie trzeba to przestrukturyzowac
    '''
    player_1 = self.player_1
    player_2 = self.player_2

    if player_1.uklad < player_2.uklad:
      player_1.winner = True

    if player_1.uklad > player_2.uklad:
      player_2.winner = True

    if player_1.uklad == player_2.uklad:
      uklad = player_1.uklad

      if uklad == 18: # Royal Poker
        player_1.winner = True
        player_2.winner = True

      if uklad == 19: # Poker
        if player_1.hand_figure[0] < player_2.hand_figure[0]:
          player_1.winner = True
        if player_1.hand_figure[0] > player_2.hand_figure[0]:
          player_2.winner = True
        if player_1.hand_figure[0] == player_2.hand_figure[0]:
          player_1.winner = True
          player_2.winner = True

      if uklad ==20: # Kareta
        if player_1.hand_figure[0] < player_2.hand_figure[0]:
          player_1.winner = True
        if player_1.hand_figure[0] > player_2.hand_figure[0]:
          player_2.winner = True
        if player_1.hand_figure[0] == player_2.hand_figure[0]: # takie same karety
          player_1_card = np.unique(player_1.sorted_hand[:,0])
          player_2_card = np.unique(player_2.sorted_hand[:,0])
          kareta_card_1 = player_1.hand_figure[0]
          indicies_1 = np.where(player_1_card == kareta_card_1)
          kareta_card_2 = player_1.hand_figure[0]
          indicies_2 = np.where(player_1_card == kareta_card_2)
          player_1_card = np.delete(player_1_card, indicies_1)
          player_2_card = np.delete(player_2_card, indicies_2)

          if player_1_card < player_2_card:
            player_1.winner = True
          if player_1_card > player_2_card:
            player_2.winner = True
          if player_1_card == player_2_card:
            player_1.winner = True
            player_2.winner = True

      if uklad == 21: # Full
        if player_1.hand_figure[0] < player_2.hand_figure[0]:
          player_1.winner = True
        if player_1.hand_figure[0] > player_2.hand_figure[0]:
          player_2.winner = True
        if player_1.hand_figure[0] == player_2.hand_figure[0]: # takie same trojki w fullu
          if player_1.hand_figure[1] < player_2.hand_figure[1]:
            player_1.winner = True
          if player_1.hand_figure[1] > player_2.hand_figure[1]:
            player_2.winner = True
          if player_1.hand_figure[1] == player_2.hand_figure[1]: # takie same trojki i para w fullu
            player_1.winner = True
            player_2.winner = True

      if uklad == 22: # Kolor
        '''
        sprawdzac karty pokolei kto ma wyzsza ten ma esse
        zzipowac 2 arrays
        '''
        player_1_card_figures = player_1.sorted_hand [:,0]
        player_2_card_figures = player_2.sorted_hand [:,0]
        i = 0
        for f, b in zip(player_1_card_figures, player_2_card_figures):
          if f < b:
            player_1.winner = True
            return
          if f > b:
            player_2.winner = True
            return
          if f == b:
            i += 1
            if i == 5:
              player_1.winner = True
              player_2.winner = True

      if uklad == 23: # strit
        player_1_card_figures = player_1.sorted_hand [:,0]
        player_2_card_figures = player_2.sorted_hand [:,0]
        i = 0
        for f, b in zip(player_1_card_figures, player_2_card_figures):
          if f < b:
            player_1.winner = True
            return
          if f > b:
            player_2.winner = True
            return
          if f == b:
            i += 1
            if i == 5:
              player_1.winner = True
              player_2.winner = True

      if uklad == 24: # trojka
        if player_1.hand_figure[0] < player_2.hand_figure[0]:
          player_1.winner = True
        if player_1.hand_figure[0] > player_2.hand_figure[0]:
          player_2.winner = True
        if player_1.hand_figure[0] == player_2.hand_figure[0]: # takie same trojki
          player_1_card = np.unique(player_1.sorted_hand[:,0])
          player_2_card = np.unique(player_2.sorted_hand[:,0])
          trojka_card = player_1.hand_figure[0]
          indicies_1 = np.where(player_1_card == trojka_card)
          indicies_2 = np.where(player_2_card == trojka_card)
          player_1_card = np.delete(player_1_card, indicies_1)
          player_2_card = np.delete(player_2_card, indicies_2)
          i = 0
          for f, b in zip(player_1_card, player_2_card):
            if f < b:
              player_1.winner = True
              return
            if f > b:
              player_2.winner = True
              return
            if f == b:
              i += 1
              if i == 2:
                player_1.winner = True
                player_2.winner = True

      if uklad == 25: # dwie pary
        if player_1.hand_figure[0] < player_2.hand_figure[0]:
          player_1.winner = True
        if player_1.hand_figure[0] > player_2.hand_figure[0]:
          player_2.winner = True
        if player_1.hand_figure[0] == player_2.hand_figure[0]: # taka sama para
          if player_1.hand_figure[1] < player_2.hand_figure[1]:
            player_1.winner = True
          if player_1.hand_figure[1] > player_2.hand_figure[1]:
            player_2.winner = True
          if player_1.hand_figure[1] == player_2.hand_figure[1]: # taka sama druga para
            player_1_card = np.unique(player_1.sorted_hand[:,0])
            player_2_card = np.unique(player_2.sorted_hand[:,0])
            pierwsza_para = player_1.hand_figure[0]
            indicies_1 = np.where(player_1_card == pierwsza_para)
            indicies_2 = np.where(player_2_card == pierwsza_para)
            player_1_card = np.delete(player_1_card, indicies_1)
            player_2_card = np.delete(player_2_card, indicies_2)
            druga_para = player_1.hand_figure[0]
            indicies_1 = np.where(player_1_card == druga_para)
            indicies_2 = np.where(player_2_card == druga_para)
            player_1_card = np.delete(player_1_card, indicies_1)
            player_2_card = np.delete(player_2_card, indicies_2)
            player_1_card[:,0] # XHYBA XD ----------------------------------------------------------------------
            player_2_card[:,0] # CHYBA XD
            if player_1_card < player_2_card:
              player_1.winner = True
            if player_1_card > player_2_card:
              player_2.winner = True
            if player_1_card == player_2_card: # taka sama 5 karta
              player_1.winner = True
              player_2.winner = True

      if uklad == 26: # para
        if player_1.hand_figure[0] < player_2.hand_figure[0]:
          player_1.winner = True
        if player_1.hand_figure[0] > player_2.hand_figure[0]:
          player_2.winner = True
        if player_1.hand_figure[0] == player_2.hand_figure[0]: # taka sama para
          player_1_card = np.unique(player_1.sorted_hand[:,0])
          player_2_card = np.unique(player_2.sorted_hand[:,0])
          dwojka_card = player_1.hand_figure[0]
          indicies_1 = np.where(player_1_card == dwojka_card)
          indicies_2 = np.where(player_1_card == dwojka_card)
          player_1_card = np.delete(player_1_card, indicies_1)
          player_2_card = np.delete(player_2_card, indicies_2)
          i = 0
          for f, b in zip(player_1_card, player_2_card):
            if f < b:
              player_1.winner = True
              return
            if f > b:
              player_2.winner = True
              return
            if f == b:
              i += 1
              if i == 2:
                player_1.winner = True
                player_2.winner = True

      if uklad == 27: # wysoka karta
          i = 0
          player_1_card = player_1.sorted_hand[:,0]
          player_2_card = player_2.sorted_hand[:,0]
          for f, b in zip(player_1_card, player_2_card):
            if f < b:
              player_1.winner = True
              return
            if f > b:
              player_2.winner = True
              return
            if f == b:
              i += 1
              if i == 2:
                player_1.winner = True
                player_2.winner = True


  def play_game(self):
    '''
    Zrobic z playera bardziej istotny TYP? danych w ktorym bede zapisywal check_hand i jego atrybuty a potem check_winner i jego atrybuty

    '''
    # Variables and class
    deck_option = CardDeck()
    player_1_cards = self.player_1.hand
    player_2_cards = self.player_2.hand
    table_cards = self.table.hand
    deck = self.deck

    # Give cards
    player_1_cards, deck = self.give_cards(player_1_cards, deck)
    player_2_cards, deck = self.give_cards(player_2_cards, deck)
    table_cards, deck = self.give_cards(table_cards, deck)
    print("PLAYER 1: \n")
    deck_option.show_cards(player_1_cards)
    print("STÓŁ: \n")
    deck_option.show_cards(table_cards)
    print("PLAYER 2: \n")
    deck_option.show_cards(player_2_cards)


    # Check hands
    player_1_hand = self.check_hand(self.player_1, self.table)[0]
    #print("PLAYER_HAND_1: {}".format(player_1_hand))
    player_2_hand = self.check_hand(self.player_2, self.table)[0]
    #print("PLAYER_HAND_2: {}".format(player_2_hand))

    print("UKLAD 1 gracza :")
    print(self.poker_hands[player_1_hand])
    print("\n")
    print("UKLAD 2 gracza :")
    print(self.poker_hands[player_2_hand])
    print("\n")
    print("\n")

    self.check_winner()

    print("PLAYER 1 Winner:")
    print(self.player_1.winner)
    print("\n")
    print("PLAYER 2 Winner:")
    print(self.player_2.winner)
    #print(self.player_1.uklad)

  def set_blind(self):
    '''
    Ustala big/small blind
    Poczatkowo losuje
    Gracze domyslnie maja None
    small = 28
    big = 29
    '''
    level = self.table.level
    index = level - 1
    self.table.small_blind =  self.table.blinds_table['Small blind'].iloc[index]
    self.table.big_blind = self.table.blinds_table['Big blind'].iloc[index]

    if self.player_1.blind == None and self.player_2.blind == None:
      randombool = bool(random.getrandbits(1))
      if randombool is True: # USTAW LOSOW NA START
        self.player_1.blind = 28
        self.player_2.blind = 29
      else:
        self.player_1.blind = 29
        self.player_2.blind = 28
    elif self.player_1.blind == 28: # ZAMIEN MIEJSCAMI
      self.player_1.blind == 29
      self.player_2.blind == 28
    elif self.player_1.blind == 29:
      self.player_1.blind == 28
      self.player_2.blind == 29

    self.table.level += 1 # UP level after round


  def take_blinds(self, player):
    '''
    Bierze blind od gracza
    '''

    # ustal kto ma big a kto ma small
    # wez hajs
    if player.blind == 28:
      player.credits -= self.table.small_blind
      # Raise error czy inne sprawdzenie ogolne wymyslic moze klasowe?
      self.table.pot += self.table.small_blind
      player.bet += self.table.small_blind
    if player.blind == 29:
      player.credits -= self.table.big_blind
      self.table.pot += self.table.big_blind
      player.bet += self.table.big_blind
    if player.credits < 0:
      print("NO GOSC HAJSU NIE MA XD: {}".format(player))

  def game_round(self):
    '''
    Daj hajs graczom ✓
    Kiedy i jak podnosic blindy ✓

    Wez small blind, big blind, rozdaj po 2 karty graczom
    Czekaj czy wejda
    Daj 3 na stol
    Czekaj czy podbija
    Daj 1 na stol
    Czekaj czy podbija
    Daj 1 na stol
    Czekaj czy podbija
    Sprawdz kto wygral
    do until one player credits == 0

    Bedzie trzeba zrobic cos w stylu player_n Action...
    '''
    # while petle trzeba bedzie napisac
    while self.player_1.credits > 0 or self.player_2.credits > 0:
      # Tasuj karty
      self.deck = CardDeck().init_deck()
      # SMALL/BIG blind and level of blinds
      self.set_blind()
      # TAKE BLINDS
      self.take_blinds(self.player_1)
      self.take_blinds(self.player_2)
      # Variables and class
      deck_option = CardDeck()
      player_1_cards = self.player_1.hand
      player_2_cards = self.player_2.hand
      table_cards = self.table.hand
      deck = self.deck

      # Give cards to players
      player_1_cards, deck = self.give_cards(player_1_cards, deck)
      player_2_cards, deck = self.give_cards(player_2_cards, deck)

      print("PLAYER 1: \n")
      deck_option.show_cards(player_1_cards)

      print("PLAYER 2: \n")
      deck_option.show_cards(player_2_cards)

      # Teraz Preflop mozna podbijac
      # Przydaloby sie zrobic interfejs jak w cmd

      table_cards, deck = self.give_cards(table_cards, deck) # Zmienic zeby 3 pokazywalo
      print("STÓŁ: \n")
      deck_option.show_cards(table_cards)

      # Check hands
      player_1_hand = self.check_hand(self.player_1, self.table)[0]
      #print("PLAYER_HAND_1: {}".format(player_1_hand))
      player_2_hand = self.check_hand(self.player_2, self.table)[0]
      #print("PLAYER_HAND_2: {}".format(player_2_hand))

      print("UKLAD 1 gracza :")
      print(self.poker_hands[player_1_hand])
      print("\n")
      print("UKLAD 2 gracza :")
      print(self.poker_hands[player_2_hand])
      print("\n")
      print("\n")

      self.check_winner()

      print("PLAYER 1 Winner:")
      print(self.player_1.winner)
      print("\n")
      print("PLAYER 2 Winner:")
      print(self.player_2.winner)
      #print(self.player_1.uklad)



      self.player_1.winner = False
      self.player_2.winner = False
      print(self.table.pot)


      self.table.level += 1

  def debug_mass(self):
    for i in range(19): # bo 20 leveli
      # Tasuj karty
      self.deck = CardDeck().init_deck()
      # SMALL/BIG blind and level of blinds
      self.set_blind()
      # TAKE BLINDS
      self.take_blinds(self.player_1)
      self.take_blinds(self.player_2)
      # Variables and class
      deck_option = CardDeck()
      player_1_cards = self.player_1.hand
      player_2_cards = self.player_2.hand
      table_cards = self.table.hand
      deck = self.deck

      # Give cards to players
      player_1_cards, deck = self.give_cards(player_1_cards, deck)
      player_2_cards, deck = self.give_cards(player_2_cards, deck)

      print("PLAYER 1 cards: \n")
      deck_option.show_cards(player_1_cards)
      print("PLAYER 1 cards_code: \n")
      print(player_1_cards)


      print("PLAYER 2 cards: \n")
      deck_option.show_cards(player_2_cards)
      print("PLAYER 2 cards_code: \n")
      print(player_2_cards)


      table_cards, deck = self.give_cards(table_cards, deck) # Zmienic zeby 3 pokazywalo
      print("STÓŁ: \n")
      deck_option.show_cards(table_cards)
      print("TABLE cards_code: \n {}".format(table_cards))

      # Check hands
      player_1_hand = self.check_hand(self.player_1, self.table)[0]
      #print("PLAYER_HAND_1: {}".format(player_1_hand))
      player_2_hand = self.check_hand(self.player_2, self.table)[0]
      #print("PLAYER_HAND_2: {}".format(player_2_hand))

      print("UKLAD 1 gracza :")
      print(self.poker_hands[player_1_hand])
      print("\n")
      print("UKLAD 2 gracza :")
      print(self.poker_hands[player_2_hand])
      print("\n")
      print("\n")

      self.check_winner()

      print("PLAYER 1 Winner:")
      print(self.player_1.winner)
      print("\n")
      print("PLAYER 2 Winner:")
      print(self.player_2.winner)
      self.player_1.winner = False
      self.player_2.winner = False
      print(self.table.pot)
      #print(self.player_1.uklad)
      if self.player_1.credits < 0:
        print("KONIEC GRY")
        return
      print(self.table.level)
      self.table.level += 1


  def debug(self):
    #value = self.is_color(self.color_hand)
    #hand_value = self.check_hand(self.full_player, self.full_table)
    #print(self.poker_hands[hand_value])
    #return value
    #card_to_check = np.concatenate((table_card, player_card), axis=0)
    #sorted = self.sort_cards(card_to_check)
    '''
    Blad z trojka
    '''
    player_card = np.array(([[ 9., 14.],[ 9., 17.]]))
    table_card = np.array(([[ 2., 17.],[10., 16.],[ 8., 17.],[ 3., 14.],[ 9., 16.]]))
    player_test = Player(5000)
    table = Table()
    player_test.hand = player_card
    table.hand = table_card
    data = self.check_hand(player_test, table)
    return data


#game = PokerGame().debug(PokerGame().full_player, PokerGame().full_table)
#print(game[0])
#print(game[1])
#print(game[2])

start_game = PokerGame()
# check_color.game_round()
# TU MASZ game = check_color.debug_mass()
#game = check_color.debug()
# TRZEBA KLASE DECK PRZEBUDOWAC

# check_color.table.pot
