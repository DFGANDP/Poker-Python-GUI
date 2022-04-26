
import numpy as np

class CardDeck(): # to bedzie chyba Class Deck a nie Card
  '''
  DOPISAC TUTAJ FUNKCJE SPECJALNA __STR__ DO ODCZYTYWANIA KART
  oraz __lt__ https://docs.python.org/2/reference/datamodel.html#object.__lt__
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


  def init_deck(self, tasuj=True):
    '''
    Tworzy deck
    Korzysta z danych liczbowych:
    1-13 FIGURY
    14-17 KOLORY
    Kazda figure laczy z kazdym kolorem i zapisuje jako np array
    '''
    deck = np.zeros((52,2)) # np array
    count = 0
    for figura in self.figure_dict:
      for color in self.color_dict:
        deck[count] = figura, color
        count +=1
    if tasuj == True:
      np.random.shuffle(deck)
    return deck

  def show_cards(self, cards):
    '''
    Dla danej zakodowanej reki kart podaje ich nazwy
    '''
    for card in cards:
      print("{}  {}".format(self.figure_dict[card[0]], self.color_dict[card[1]]))
    print("\n")


#deck = CardDeck().init_deck()
#print(deck)
#CardDeck().show_cards(deck)
