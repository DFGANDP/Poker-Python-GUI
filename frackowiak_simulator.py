# -*- coding: utf-8 -*-
"""Pokerv4

    https://colab.research.google.com/drive/14aZwMwR77tScp2jqVhkEagAZ1tx2FMYE

~DFGANDP
"""


import numpy as np
from frackowiak_player import Player
from frackowiak_table import Table
from frackowiak_CardDeck import CardDeck
from tqdm import tqdm


class PokerGame():
  '''
  Glowne zmiany do wprowadzenia
  Operowanie na obiektach glownych z klas chodzi o Player a nie rekach
  zwracanie 5 kart z 7 posortowanych tworzacych najlepszy uklad
  '''
  def __init__(self):
    self.figure_dict = {
      1 : "A",
      2 : "K",
      3 : "Q",
      4 : "J",
      5 : "10",
      6 : "9",
      7 : "8",
      8 : "7",
      9 : "6",
      10 : "5",
      11 : "4",
      12 : "3",
      13 : "2",
    }

    self.color_dict =  {
      14 : "Dzwonek",
      15 : "Serce",
      16 : "Pik",
      17 : "Trefl"
    }
    self.poker_hands = {
      28 : 'kolor_frackowiaka',
      22 : "kolor",
      29 : 'strit_frackowiaka',
      23 : "strit",
      30 : 'poker_frackowiaka',
      19 : "poker",
      20 : "kareta",
      21 : "full",
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

  def show_cards(self, cards):
    '''
    Dla danej zakodowanej reki kart podaje ich nazwy
    '''
    for card in cards:
      print("{}  {}".format(self.figure_dict[card[0]], self.color_dict[card[1]]))
    print("\n")

  def give_cards(self, object, deck):
    '''
    object - table or player
    '''
    index = []
    for i in range(len(object)):
      object[i] = deck[i]
      index.append(i)
    deck = np.delete(deck, index, 0) # TRZEBA PODAC OS
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
    card_to_check = self.sort_cards(card_to_check)

    # Sprawdz kolor oraz strita oraz zwroc czy jest frackowiaka czy nie !
    color_value, card_tab = self.is_color_and_frackowiak(card_to_check) # sprawdz kolor i zwroc karty ktore go daja (card_tab)
    strit_value, first_card = self.is_strit_and_frackowiak(card_to_check)
    poker_value, color_cards = self.is_poker_and_frackowiak(card_to_check)
    
    if color_value is not False: 
      player.uklad.append(color_value)
      
    if strit_value is not False: 
      player.uklad.append(strit_value)

    # Poker frackowiaka
    if poker_value == 30:
      player.uklad.append(30)

    # POKER
    if poker_value == 19:
      # karte najwyzsza tworzaca
      player.uklad.append(19)

    # KARETA
    hand, kareta_figure, cards_kareta = self.is_fourth(card_to_check)
    if hand == 20:
      player.uklad.append(20)

    # FULL
    hand, hand_figures, player_hand = self.is_full(card_to_check)
    if hand == 21:
      player.uklad.append(21)

    #TROJKA
    hand, trojka_figure, cards_trojka = self.is_trojka(card_to_check)
    if hand == 24:
      player.uklad.append(24)
      
    #DWIE PARY
    hand, hand_figures, player_hand = self.is_two_pairs(card_to_check)
    if hand == 25:
      player.uklad.append(25)


    #PARA
    hand, para_figure, cards_para = self.para(card_to_check)
    if hand == 26:
      player.uklad.append(26)

    #WYSOKA KARTA
    if not player.uklad:
      player.uklad.append(27)

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

  def is_color_and_frackowiak(self, cards_array):
    '''
    Sprawdza czy jest kolor jesli tak zwraca wartosc ze slownika dla koloru
    oraz podaje indeksy kart w tablicy ktore na kolor sie skladaja
    dlatego lepiej wczesniej posegregowac
    '''
    frackowiak = False
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
        if color_count == 4: # FRACKOWIAK CHECK
          card_tab = card_tab[:-1] # usuwa 1 karte z 6 i zwraca 5 najlepszych
          frackowiak = True
        elif color_count == 5:
          card_tab = card_tab[:-1] # Usuwa 2 najnizsze karty z 7
          # Zakladam ze zwraca posortowane
          frackowiak = False
          return 22, card_tab
    if frackowiak == True:
      return 28, card_tab
    return False, False
  
  def is_color_and_frackowiak(self, cards_array):
      for kolor in CardDeck().color_dict:
          card_tab = []  # Inicjalizacja pustej listy dla każdego koloru
          for card in cards_array:
              card_color = card[1]
              if kolor == card_color:
                  card_tab.append(card)  # Dodawanie karty do listy

          if len(card_tab) == 4:  # Sprawdzanie czy jest 4 karty koloru (Frackowiak)
              return 28, np.array(card_tab)  # Konwersja listy z powrotem do numpy array
          elif len(card_tab) == 5:  # Sprawdzanie czy jest 5 kart koloru
              return 22, np.array(card_tab)

      return False, False


  def is_strit_and_frackowiak(self, cards_array):
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
      if count == 3:
        return 29, fcard_strit
      elif count == 4:
        # print("Jest strit")
        # print(fcard_strit)
        return 23 , fcard_strit
    return False, False

  def is_poker_and_frackowiak(self, cards_array):
    color_value, color_cards = self.is_color_and_frackowiak(cards_array)
    strit_value, strit_card = self.is_strit_and_frackowiak(cards_array)

    # Sprawdź, czy istnieje zarówno strit jak i kolor
    if color_value and strit_value:
        # Stwórz zestaw kart tworzących kolor
        color_set = set([tuple(card) for card in color_cards])

        # Sprawdź, czy karty tworzące strita są w tym samym kolorze
        for card in cards_array:
            if card[0] == strit_card and tuple(card) in color_set:
                # Jest to poker Frackowiaka, jeśli jest to 4 karty
                if color_value == 28 and strit_value == 29:
                    return 30, color_cards  # Poker Frackowiak

                # Jest to zwykły poker, jeśli jest to 5 kart
                if color_value == 22 and strit_value == 23:
                    return 19, color_cards  # Zwykły poker

    return False, False



  def debug_mass(self):
    games_data = []
    uklad_counts = {name: 0 for name in self.poker_hands.values()}  # Inicjalizacja liczników dla każdego układu
    
    for i in tqdm(range(1000)): # bo 20 leveli
      # Tasuj karty
      deck_instance = CardDeck()
      deck = deck_instance.deck

      frackowiak_1 = Player(1)
      frackowiak_2 = Player(2)
      frackowiak_3 = Player(3)
      frackowiak_4 = Player(4)
      frackowiak_5 = Player(5)
      frackowiak_6 = Player(6)


      # Give cards to players
      frackowiak_1.hand, deck = self.give_cards(frackowiak_1.hand, deck)
      frackowiak_2.hand, deck = self.give_cards(frackowiak_2.hand, deck)
      frackowiak_3.hand, deck = self.give_cards(frackowiak_3.hand, deck)
      frackowiak_4.hand, deck = self.give_cards(frackowiak_4.hand, deck)
      frackowiak_5.hand, deck = self.give_cards(frackowiak_5.hand, deck)
      frackowiak_6.hand, deck = self.give_cards(frackowiak_6.hand, deck)
      
      #print(f"Dla frackowiak_1 mamy karty: ")
      #print(self.show_cards(frackowiak_1.hand))
      #print(f"Reszta kart w deku: ")
      #print(self.show_cards(deck))

      table_instance = Table()
      table_cards = table_instance.hand

      table_cards, deck = self.give_cards(table_cards, deck) # Zmienic zeby 3 pokazywalo
      #print(f"Na stole mamy: ")
      #print(self.show_cards(table_cards))

      # Check hands
      self.check_hand(frackowiak_1, table_instance)
      self.check_hand(frackowiak_2, table_instance)
      self.check_hand(frackowiak_3, table_instance)
      self.check_hand(frackowiak_4, table_instance)
      self.check_hand(frackowiak_5, table_instance)
      self.check_hand(frackowiak_6, table_instance)
      
      '''
      if len(frackowiak_1.uklad) >1:
        print("UKLAD 1 gracza :")
        for uklad in frackowiak_1.uklad:
          print(self.poker_hands[uklad])
      '''
      game_result = {
          'game_id': i,
          'player_hands': [],
          'player_uklads': []
      }

      for player in [frackowiak_1, frackowiak_2, frackowiak_3, frackowiak_4, frackowiak_5, frackowiak_6]:
          self.check_hand(player, table_instance)
          game_result['player_hands'].append(player.hand)
          game_result['player_uklads'].append([self.poker_hands[uklad] for uklad in player.uklad])

          for uklad in player.uklad:
              uklad_name = self.poker_hands[uklad]
              uklad_counts[uklad_name] += 1

      games_data.append(game_result)

    # Podsumowanie prawdopodobieństw układów
    total_hands = 1000 * 6  # Liczba wszystkich rąk (6 graczy na grę)
    for uklad_name, count in uklad_counts.items():
        print(f"Układ {uklad_name}: {count/total_hands:.2f}%")



def main():
    simulation = PokerGame()
    simulation.debug_mass()
    

if __name__ == "__main__":
    main()