# TO SA MOJE
from pokerv2 import PokerGame
from table import Table
from CardDeck import CardDeck


import tkinter as tk
from tkinter import ttk # style
from tkinter import font as tkFont # FONT
from PIL import ImageTk, Image
import time

figure_dict = {
     0 : "NO CARD",
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


color_dict =  {
         0  : "NO CARD",
         14 : "Dzwonek",
         15 : "Serce",
         16 : "Pik",
         17 : "Trefl"
    }

LARGE_FONT = ("Verdana", 15)

class MainPoker(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) # init inheritance ?
        tk.Tk.iconbitmap(self, default="Icon.ico")
        tk.Tk.wm_title(self, "POKEREK")

        container = tk.Frame(self) # edge of window
        container.pack(side="top", fill="both", expand = True) # fill fill space , expand if there is space expand beyond the limit
        container.grid_rowconfigure(0, weight=1) # weight is priority tzn?
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PlayPage): # dodaje strony

            frame = F(container, self) # initial page (chyba jednak nie xD)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew") # sticky -  nourth south east west



        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont] # container - cont
        frame.tkraise() # raise it to the front   front page idea

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # parent is MainPoker class
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)


        self.configure(background='black')

        INFO_TEST = tk.Label(self, text="POKER GUI v2", font=("Arial Bold", 50))
        INFO_TEST.pack(side=tk.TOP)
        # PLAY
        button_play = tk.Button(self,
                           text="PLAY GAME",
                           bg="#856ff8",
                           fg="black",
                           command=lambda: controller.show_frame(PlayPage))
        button_play.pack(side=tk.TOP)
        # BLIND INFO
        INFO_BLIND = tk.Label(self, text='''
CREDITS: 5000
2 PLAYERS GAME
Level     Small blind     Big blind
1         50              100
2         100             200
3         150             300
4         200             400
5         250             500
6         300             600
7         350             700
8         400             800
9         450             900
10        500             1000
11        550             1100
12        600             1200
13        700             1400
14        800             1600
15        900             1800
16        1000            2000
17        1100             2200
18        1200             2400
19        1300             2600
20        1400             2800
    ''', font=("Arial Bold", 10))
        INFO_BLIND.pack(side=tk.TOP)
        # QUIT
        buttonq = tk.Button(self,
                           text="QUIT",
                           fg="black",
                           command=quit)
        buttonq.pack(side=tk.BOTTOM)
        '''
        I teraz do command trzeba przypisac otwieranie drugiego okna juz z gra
        '''



class PlayPage(tk.Frame):

    def __init__(self, parent, controller):


        '''
        https://www.pythontutorial.net/tkinter/tkinter-photoimage/
        DLACZEGO ZDJECIA NIE DZIALAJA KURWAAAA DLACZEGO
        '''
        tk.Frame.__init__(self, parent)
        self.game = PokerGame()

        cards_dir = "cards_images/"
        button_dir = "buttons/"
        '''
        WSZYTSKO MA SIE WYSWIETLIC TYLKO ODKRYWAC SIE BEDZIE SPOD JAKIEJS WARSTWY JESLI CHODZI O karty
        JESLI IDZIE O ZMIENIAJACY SIE TEKST TO DO OGARNIECIA
        '''



        # INFO ABOUT GAME

        self.text = tk.StringVar()
        self.text.set("Game info: essa")

        label = tk.Label(self, textvariable=self.text, font=LARGE_FONT)
        label.config(bg="gray")
        label.grid(row=0, column=0, sticky="nw")

        buttonp = tk.Button(self, text="PLAY GAME", # CALL
                command=self.play_v2)
        buttonp.grid(row=1, column=0, sticky="nsew")


        vertical = tk.Scale(self, from_=0, to=200, orient=tk.HORIZONTAL)
        vertical.grid(row=1, column=6, sticky="nw") # DAC jeszcze back to menu
        vertical.set(50) # TEST

        # IMG test
        img_dir = cards_dir+"0_0.png"
        self.img0 = tk.PhotoImage(file=img_dir)

        # SHOW TABLE CARDS
        labelc1 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc1.config(bg="gray")
        labelc1.grid(row=0, column=1, sticky="nw")

        labelc2 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc2.config(bg="gray")
        labelc2.grid(row=0, column=2, sticky="nw")

        labelc3 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc3.config(bg="gray")
        labelc3.grid(row=0, column=3, sticky="nw")

        labelc4 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc4.config(bg="gray")
        labelc4.grid(row=0, column=4, sticky="nw")

        labelc5 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc5.config(bg="gray")
        labelc5.grid(row=0, column=5, sticky="nw")

        #PLAYER CARDS
        labelp1 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelp1.config(bg="gray")
        labelp1.grid(row=1, column=1, sticky="nw")

        labelp2 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelp2.config(bg="gray")
        labelp2.grid(row=1, column=2, sticky="nw")

        '''
        BUTTONS

        ADD SLIDER FOR CALL/RAISE
        '''
        button_dirimg = button_dir+"button.png"
        self.imgb = tk.PhotoImage(file=button_dirimg)

        helv36 = tkFont.Font(family='Helvetica', size=18, weight='bold')

        button1 = tk.Button(self, text="CHECK", font=helv36, # CALL
                command=self.check)
        button1.grid(row=1, column=3, sticky="nsew")

        button2 = tk.Button(self, text="FOLD", font=helv36,
                command=self.fold)
        button2.grid(row=1, column=4, sticky="nsew")

        button3 = tk.Button(self, text="CALL/RAISE", font=helv36,
                command=self.call_raise)
        button3.grid(row=1, column=5, sticky="nsew")

        button4 = tk.Button(self, text="BACK TO MENU", font=helv36,
                command=lambda: controller.show_frame(StartPage))
        button4.grid(row=0, column=6, sticky="nsew")



        self.game = PokerGame()

    def extract_imgpth(self, array):
        '''
        INPUT - player_hand
        Output - File_path
        '''
        string = str(array)

        comps = string.partition(".")
        figure = comps[0][2:]
        if array[0] >= 10:
            figure = "1" + figure
        color = comps[2][1:3]
        #print(string)
        #print("FIGURA {}".format(figure))
        return ("cards_images/"+figure+"_"+color+".png")


    def preflop(self, level):
        '''
        IN: Level
        OUT:
        + PLAYERS CARDS
        + TAKE BLINDS

        '''
        game = self.game # self.game = PokerGame()
        player_1 = self.game.player_1
        player_2 = self.game.player_2
        deck = CardDeck().init_deck()
        game.set_blind() # TU LEVEL MA WEJSC -------------------------------------------<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        game.take_blinds(player_1)
        game.take_blinds(player_2)

        # Rozdaj po 2 karty
        player_1.hand, deck = game.give_cards(player_1.hand, deck)
        player_2.hand, deck = game.give_cards(player_2.hand, deck)
        game.table.hand , deck = self.game.give_cards(game.table.hand, deck)
        self.action()



    def flop(self):



        table_1card = self.extract_imgpth(self.game.table.hand[0])
        table_2card = self.extract_imgpth(self.game.table.hand[1])
        table_3card = self.extract_imgpth(self.game.table.hand[2])

        self.t1c = tk.PhotoImage(file=table_1card)
        self.t2c = tk.PhotoImage(file=table_2card)
        self.t3c = tk.PhotoImage(file=table_3card)



        labelc1 = tk.Label(self, image=self.t1c, font=LARGE_FONT)
        labelc1.config(bg="gray")
        labelc1.grid(row=0, column=1, sticky="nw")

        labelc2 = tk.Label(self, image=self.t2c, font=LARGE_FONT)
        labelc2.config(bg="gray")
        labelc2.grid(row=0, column=2, sticky="nw")

        labelc3 = tk.Label(self, image=self.t3c, font=LARGE_FONT)
        labelc3.config(bg="gray")
        labelc3.grid(row=0, column=3, sticky="nw")
        self.action()


        return

    def turn(self):
        table_4card = self.extract_imgpth(self.game.table.hand[3])
        self.t4c = tk.PhotoImage(file=table_4card)
        labelc4 = tk.Label(self, image=self.t4c, font=LARGE_FONT)
        labelc4.config(bg="gray")
        labelc4.grid(row=0, column=4, sticky="nw")
        self.action()

    def river(self):
        table_5card = self.extract_imgpth(self.game.table.hand[4])
        self.t5c = tk.PhotoImage(file=table_5card)
        labelc5 = tk.Label(self, image=self.t5c, font=LARGE_FONT)
        labelc5.config(bg="gray")
        labelc5.grid(row=0, column=5, sticky="nw")
        self.action()



    def player_turn(self):
        self.show_info_game()
        player = self.check_player()
        # SHOW PLAYERS CARDS
        player_1card = self.extract_imgpth(player.hand[0])
        player_2card = self.extract_imgpth(player.hand[1])
        self.p11c = tk.PhotoImage(file=player_1card)
        self.p12c = tk.PhotoImage(file=player_2card)

        labelp1 = tk.Label(self, image=self.p11c, font=LARGE_FONT)
        labelp1.config(bg="gray")
        labelp1.grid(row=1, column=1, sticky="nw")

        labelp2 = tk.Label(self, image=self.p12c, font=LARGE_FONT)
        labelp2.config(bg="gray")
        labelp2.grid(row=1, column=2, sticky="nw")

        call = self.slider_start()
        if call == None:
            print("nie ustalono start slider")
            call = 0
        vertical = tk.Scale(self, from_=call, to=player.credits, orient=tk.HORIZONTAL)
        vertical.grid(row=1, column=6, sticky="nw") # DAC jeszcze back to menu,

        button3 = tk.Button(self, text="CALL/RAISE",
                command=lambda: self.call_raise(vertical.get()))
        button3.grid(row=1, column=5, sticky="nsew")


        '''
        TUTAJ SIE KONCZY I CZEKA NA WCISNIECIE PRZYCISKU
        '''


        return

    def slider_start(self):
        '''
        1. bet oposite player
        2. big blind - small blind ✓
        3. check (0) ✓
        '''
        i = 0
        if self.game.table.round == 0 and i == 0:
            i += 1
            return self.game.table.big_blind - self.game.table.small_blind
        #else: # dobic do beta drugiego playera!!
            #return True




    def check_player(self):
        '''
        zwraca gracza ktorego jest kolej
        '''
        if self.game.table.turn == 1:
            return self.game.player_1
        elif self.game.table.turn == 2:
            return self.game.player_2
        else:
            print("BLAD NIE MA GRACZA")

    def fold(self):
        player = self.check_player()
        player.actionp = "fold"
        print("gracz {} folduje zaczynam nowa runde".format(player))
        self.check_action()
        return

    def check(self):
        # self.game.table.turn = 1
        player = self.check_player()
        player.actionp = "check"
        self.check_action()
        return

    def call_raise(self, count):
        '''
        Jesli jest wartosc liczbowa to sprawdz czy jest valid
        '''
        player = self.check_player()
        player.actionp = count
        player.bet += count
        player.credits -= count
        self.game.table.pot += count
        self.check_action()
        return

    def check_preflop_unique_requierments(self):
        '''
         !!!! DLA PREFLOPA  !!!!!   WARUNEK
        JESLI JEDNA OSOBA ZCALLUJE A DRUGA POCZEKA
        czyli
        betp1 = betp2 and actionp ktoregokolwiek jest == check

        INACZEJ JESLI NIE FOLD TO MOGA SIE RERAISOWAC W NIESKONCZONOSC
        '''
        count = 0
        if self.game.table.round == 0 and count == 0:
            count += 1
            if self.game.player_2.bet == self.game.player_1.bet:
                if self.game.player_1.actionp == "check" or self.game.player_2.actionp == "check":
                    pass
        return

    def check_round(self):
        if self.game.table.round == 1:
            '''
            trzeba jakis ogolny system wymyslic
            '''
            self.flop()
        elif self.game.table.round == 2:
            self.turn()
        elif self.game.table.round == 3:
            self.river()
        elif self.game.table.round == 4:
            self.end_round()
        else:
            self.action()

    def move_credits(self):
        '''
        Przesyla kredyty z table pot do gracza
        '''

        return

    def end_round(self):
        self.move_credits()
        self.game.table.round = 0
        self.beginning_view()

        # Jesli nie bylo folda znajdz kto wygral
        if self.game.player_1.winner == False and self.game.player_2.winner == False:
            # PRZYPISZ UKLADY KURWA
            player_1_hand = self.game.check_hand(self.game.player_1, self.game.table)[0]
            player_2_hand = self.game.check_hand(self.game.player_2, self.game.table)[0]
            print("UKLAD 1 gracza :")
            print(self.game.poker_hands[player_1_hand])
            print("\n")
            print("UKLAD 2 gracza :")
            print(self.game.poker_hands[player_2_hand])
            print("\n")
            print("\n")

            self.game.check_winner()

        print("Gracz pierwszy wygral: {}".format(self.game.player_1.winner))
        print("Gracz drugi wygral: {}".format(self.game.player_2.winner))
        self.play_v2()
        return

    def check_action(self):
        '''
        w kolko powtarzaj jesli nie bedzie warunkow albo daj flopa
        '''

        self.check_preflop_unique_requierments()

        if self.game.player_1.actionp == "check" and self.game.player_2.actionp == "check":
            '''
            dodac funkcje sprawdzajaca czy maja rowne bety
            '''
            print("OBOJE WCISNELI CHECK")
            self.game.table.round+=1
            # WYZERUJ AKCJE NA NASTEPNA RUNDE
            self.game.player_1.actionp = None
            self.game.player_2.actionp = None

        self.check_fold()

        self.check_raise()

        print("RUNDA NR {}".format(self.game.table.round))

        if self.game.player_1.bet == self.game.player_2.bet and self.game.player_1.actionp != None and self.game.player_2.actionp != None:
            '''
            ale big blind moze jeszcze rase wiec oraz actionp != None
            '''
            self.game.table.round += 1
            self.game.player_1.actionp = None
            self.game.player_2.actionp = None
            print("rowne bety ide dalej")

        self.check_round()
        return

    def check_raise(self):
        '''
        Sprawdza czy bet jest valid tzn:

        zalozmy ze callujemy small blind
        '''
        player_reader = {
        1 : self.game.player_1,
        2 : self.game.player_2
        }
         # Aktualny gracz
        opplayer = self.get_opponent_player() # opposite player
        if type(player_reader[self.game.table.turn].actionp) == int:
            '''
            Sprawdz czy wrzucil conajmniej lub wiecej;  tak duzo ile 2gi gracz
            '''
            if player_reader[self.game.table.turn].bet < opplayer.bet:
                print("NOT VALID OPTION !!! musisz zabetowac conajmniej tyle co przeciwnik")
                self.player_turn()
            elif player_reader[self.game.table.turn].bet >= opplayer.bet:
                pass


        return

    def get_opponent_player(self):
        '''
        OUT Player ktorego NIE JEST tura
        Bierze self.game.table.turn i oddaje 2 gracza niezaleznie od tego
        ktorego gracza aktuaklnie jest tura

        '''
        if self.game.table.turn == 1:
            return self.game.player_2
        elif self.game.table.turn == 2:
            return self.game.player_1

    def check_fold(self):
        '''
        SLOWNIK
        Jesli player zfoldowal dac 2giemu graczowi winner = True
        '''
        player_reader = {
        1 : self.game.player_1,
        2 : self.game.player_2
        }
        if player_reader[self.game.table.turn].actionp == "fold":
              self.change_player_turn()
              player_reader[self.game.table.turn].winner = True
              self.end_round()
        return

    def change_player_turn(self):
        if self.game.table.turn == 1:
            self.game.table.turn = 2

        # byla tura gracza 2 wiec teraz jest 1
        elif self.game.table.turn == 2:
            self.game.table.turn = 1

    def action(self):
        '''
        Sprawdza kto zaczyna i daje mu ture
        '''

        if self.game.table.turn == 0:
            if self.game.player_1.blind == 28: # 28
                self.game.table.turn = 1 # player 1 zaczyna
            elif self.game.player_2.blind == 28:
                self.game.table.turn = 2 # player 2 zaczyna
        else:
            self.change_player_turn()
        print("TURA gracza {}".format(self.game.table.turn))
        self.player_turn()

    def play_v2(self):

        dirc = "cards_images/"
        player_1 = self.game.player_1
        player_2 = self.game.player_2
        level = 0
        # Zresetuj stany wygrania
        player_1.winner = False
        player_2.winner = False

        self.preflop(level)
        # AKCJA GRACZY

    def show_info_game(self):
        '''
        Dla danego gracza wyswietla informacje o grze
        '''
        blinds = {28: "small blind", 29: "big blind"}
        table_cards = round # ZAraz to dopisze
        player_1 = self.game.player_1
        player_2 = self.game.player_2
        infoshow = ('''
        ----------------------------------
        TURN PLAYER {}
        PLAYER 1 CREDITS: {}  |  {}
        PLAYER 2 CREDITS: {}  |  {}
        TABLE POT:        {}
        TABLE CARDS: \n
        '''.format(self.game.table.turn,
                     player_1.credits,
                     blinds[player_1.blind],
                     player_2.credits,
                     blinds[player_2.blind],
                     self.game.table.pot))
        self.text.set(infoshow)

    def show_cards(self, cards, ile=2):
        '''
        Dla danej zakodowanej reki kart podaje ich nazwy
        '''
        i = 0
        for card in cards:
            print("{}  {}".format(figure_dict[card[0]], color_dict[card[1]]))
            i += 1
            if ile == i:
                print("\n")
                return

    def changeText(self):
        self.text.set("Text updated")

    def play_v3(self):
        '''

        programowac dla obiektow ogolnych

        Gra toczy sie az 1 gracz nie spadnie do 0
        1. Rozdaj karty
        ROUNDS:
        0 - PREFLOP
        1 - FLOP
        2 - TURN
        3 - RIVER

        DO NAPRAWY:
        *BLINDY SIE NIE ZMIENIAJA (BO RUNDA CALA NIE PRZECHODZI)
        *akcja gracza

        >>>>>>>>>DO TEGO WLASNIE SIE UZYWA LAMBDE<<<<<<<<<<<<<<<<<<<<<<<<<

        '''
        dirc = "cards_images/"
        player_1 = self.game.player_1
        player_2 = self.game.player_2
        level = 0
        while player_1.credits > 0 and player_2.credits > 0: # dopoki jeden albo drugi gracz ma



          self.preflop(level)
          # AKCJA GRACZY

          self.flop()
          # AKCJA GRACZY

          self.turn()
          # AKCJA GRACZY

          self.river()
          # AKCJA GRACZY
          print(" po riverze")
          # PODSUMOWANIE RUNDY
          level += 1  # TABLE ma atrybut level

          return
        else: print("KONIEC")


    def beginning_view(self):
        img_dir = "C:/Users/Wojtek/Desktop/wojtek/paper_implementation/Poker_GUI/cards_images/0_0.png"
        self.img0 = tk.PhotoImage(file=img_dir)

        # SHOW TABLE CARDS
        labelc1 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc1.config(bg="gray")
        labelc1.grid(row=0, column=1, sticky="nw")

        labelc2 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc2.config(bg="gray")
        labelc2.grid(row=0, column=2, sticky="nw")

        labelc3 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc3.config(bg="gray")
        labelc3.grid(row=0, column=3, sticky="nw")

        labelc4 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc4.config(bg="gray")
        labelc4.grid(row=0, column=4, sticky="nw")

        labelc5 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelc5.config(bg="gray")
        labelc5.grid(row=0, column=5, sticky="nw")

        #PLAYER CARDS
        labelp1 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelp1.config(bg="gray")
        labelp1.grid(row=1, column=1, sticky="nw")

        labelp2 = tk.Label(self, image=self.img0, font=LARGE_FONT)
        labelp2.config(bg="gray")
        labelp2.grid(row=1, column=2, sticky="nw")
        return

app = MainPoker()
app.mainloop()
#PlayPage().play
