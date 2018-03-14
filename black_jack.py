import time #time.sleep used frequently to slow gameplay to prevent rapid-fire text
import random
import sys
from IPython.display import clear_output

# Creates Player class to keep track of and easily manipulate player attributes
class Player(object):

  def __init__(self, name, cards, chips, bet):
    self.name = name
    self.cards = cards
    self.chips = chips
    self.bet = bet

#Asks player to place bet. Sys.stdout.write  used to space out the timing of text-appearance
#for aesthetic reasons. Input of bet_question used to check if player is able to bet the entered
#amount, and to increase self.bet and decrease self.chip attributes.
  def place_bet(self):
    sys.stdout.write (self.name + ", chips to spend: "); time.sleep(2)
    sys.stdout.write (str(self.chips))
    print()
    time.sleep(2)
    while True:
        try:
            bet_question = int(input("How much would you like to wager?  "))
            print()
        except:
            print()
            print("You can't bet that.  Please try again.")
            time.sleep(3)
        else:
            if bet_question > self.chips or bet_question < 1:
                print ("You can't bet that. Please try again.")
                time.sleep(2)
            elif 0 < bet_question <= self.chips:
                self.bet += bet_question
                self.chips -= bet_question
                print("{} bets {}.".format(self.name, self.bet))
                time.sleep(3)
                clear_output()
                break

# appends first two cards to player.cards and prints both under player-name
  def dealt_hand(self):
    count = 0
    while count < 2:
      card = random.choice(deck.cards)
      self.cards.append(card)
      count += 1
    print(self.name + ":\n" + str(self.cards))
    time.sleep(3)

#checks if player's dealt-hand is blackjack.  If so, rewards player and resets their bet amount and hand
  def black_jack_check(self):
    if deck.card_value(self) == 21:
      time.sleep(2)
      print("That's blackjack. \nYou win " + str(int(self.bet * 1.5)) + " chips, {}.".format(self.name))
      self.chips += (int(self.bet * 1.5))
      self.bet = 0
      self.cards = []
      time.sleep(5)

#returns if hand-value is over 21
  def hand_loss_check(self):
      return deck.card_value(self) > 21

#iterates through asking player to hit, stand, fold or double-down until they choose to stand or bust.
#player can only fold or double-down while they have first hand.  If player attempts to double-down again,
#double_down counter prevents player from doubling again.
  def hit_stand_fold_double(self):
    double_down = 0
    while True:
      #if player hit blackjack on dealt hand, this skips this portion of the round for them
      if self.cards == []:
        break
      #all options are open to player first time through the loop
      elif len(self.cards) == 2 and double_down == 0:
        choice = input("{}, would you like to (h)it, (s)tand, (f)old or (d)ouble-down?:  ".format(self.name))
        while choice != "h" and choice != "hit" and choice != "s" and choice != "stand" and choice != "f" \
        and choice != "fold" and choice != "d" and choice != "double-down":
          choice = input("That's not how you play blackjack. Would you like to (h)it, (s)tand, (f)old or (d)ouble-down?  ")
          time.sleep(3)
      elif len(self.cards) == 2 and double_down > 0:
        choice = input("\nWould you like to (h)it, (s)tand or (f)old?  ")
        while choice != "h" and choice != "hit" and choice != "s" and choice != "stand" and choice != "f" \
        and choice != "fold":
          choice = input("That's not how you play blackjack. Would you like to (h)it, (s)tand or (f)old?")
          time.sleep(3)
      else:
        choice = input("\nWould you like to (h)it or (s)tand?  ")
        while choice != "h" and choice != "hit" and choice != "s" and choice != "stand":
          choice = input("That's not how you play blackjack. Would you like to (h)it or (s)tand? ")
          time.sleep(3)
      #appends random card to player.cards and prints string of player name and cards.
      #calls hand_loss_check() to check if hand-value is over limit.  If so, resets player bet and cards.
      if choice == "h" or choice == "hit":
        card = random.choice(deck.cards)
        self.cards.append(card)
        print("\n{}: Hit".format(self.name))
        print("\n" + str(self.cards))
        time.sleep(3)
        if self.hand_loss_check() == True:
          print("\n" + self.name + ": Bust")
          self.bet = 0
          self.cards = []
          time.sleep(3)
          break
      #returns half of bet to player's chips and resets bet and cards of player
      elif choice == "f" or choice == "fold":
        self.chips += int(self.bet / 2)
        print("\n{}: Fold ".format(self.name))
        self.bet = 0
        self.cards = []
        print()
        time.sleep(3)
        break
        #checks if player has enough chips to double-down and removes additional chips equal to bet
        # and doubles player bet.  Activates double_down counter to prevent additional doubling.
      elif choice == "d" or choice == "double-down":
        if self.chips >= self.bet:
          self.chips -= self.bet
          self.bet *= 2
          print("\n{}: Double-down".format(self.name))
          double_down += 1
          time.sleep(2)
        else:
          print("\n{}: not enough chips to double-down.".format(self.name))
          double_down += 1
          time.sleep(2)
        #player stands and the active portion of their turn ends
      else:
        print("\n{} stands.".format(self.name))
        time.sleep(2)
        break

#checks if player has already busted, folded or gotten blackjack.  If not, continues.  Checks for win,
#draw or loss and rewards appropriately.
  def hand_win_check(self):
    global dealer
    if self.cards != []:
      if dealer.cards == [] or deck.card_value(dealer) < deck.card_value(self):
        self.chips += (self.bet * 2)
        print("\nYou win {} chips, {}.".format(self.bet*2, self.name))
        self.bet = 0
        self.cards = []
        time.sleep(3)
        print()
      elif deck.card_value(dealer) == deck.card_value(self):
        self.chips += self.bet
        self.bet = 0
        self.cards = []
        print("\nDraw.  Your chips back, {}".format(self.name))
        time.sleep(3)
        print()
      elif deck.card_value(dealer) > deck.card_value(self):
        self.bet = 0
        self.cards = []
        print("\nDealer wins.  Better luck next hand, {}".format(self.name))
        time.sleep(3)
        print()

#checks if player's chips are 0.  If so, their name is removed from total_player list.
  def chip_check(self):
    global total_players
    if self.chips < 1:
      total_players.remove(self)
      print("\nLooks like you're luck has run out.  See you next game, {}.".format(self.name))
      time.sleep(5)

#resets players' attributes if player chooses to play again
  def player_reset(self):
    self.chips = 50

#inherited Player class for the "dealer" computer player to follow adapted function calls
class Computer_Player(Player):

  def __init__(self, name, cards, chips, bet):
        Player.__init__(self, name, cards, chips, bet)

#for aesthetic reasons computer player clears screen when reached in iteration of total_players
  def place_bet(self):
    clear_output()

#computer player receives first hand of two cards, but only first card is printed.  The second is presented
#as a question mark.
  def dealt_hand(self):
    count = 0
    while count < 2:
      card = random.choice(deck.cards)
      self.cards.append(card)
      count += 1
    print("\n" + dealer.name + " : \n[" + str(dealer.cards[0]) + " ?]\n" )
    time.sleep(3)

  def black_jack_check(self):
    pass

#function for computer player to check if all other players have already folded or busted
# so as to not continue playing round when it is the only player.
  def hand_skip(self):
    global total_players
    bust_count = 0
    for player in total_players:
      if player.cards == []:
        bust_count += 1
    return bust_count == len(total_players) - 1

#checks and breaks if computer is only player.  Sets computer to hit if hand-total is less than 17.
#Checks for computer loss after 'hit' and resets cards if so.  Otherwises, stands and passes to next function.
  def hit_stand_fold_double(self):
    clear_output()
    while True:
      if self.hand_skip() == True:
        break
      if len(self.cards) == 2:
        print("\n" + self.name + " :\n" + str(self.cards))
      if deck.card_value(self) < 17:
        time.sleep(3)
        print("\nDealer: Hit")
        time.sleep(2)
        card = random.choice(deck.cards)
        self.cards.append(card)
        print()
        print(self.name + ":" + str(self.cards))
        time.sleep(2)
        if self.hand_loss_check() == True:
          print("\n"+ self.name + ": Bust")
          self.cards = []
          time.sleep(2)
          break
      else:
        print("\n" + self.name + ": Stand")
        time.sleep(2)
        break

#after all players have checked to recieve winnings, computer resets hand.
  def hand_win_check(self):
    self.cards = []

  def chip_check(self):
    pass

  def player_reset(self):
    pass

#A deck class to allow for the creation of a deck object and interpretation of card values
class Full_Deck(object):

    def __init__(self, cards):
        self.cards = cards

#interprets card values and returns a total
    def card_value(self, player):
      total = 0
      for card in player.cards:
        if card == "Ace":
            card = player.cards.append(card)
            player.cards.remove("Ace")
      for card in player.cards:
        if card == "Jack" or card == "Queen" or card == "King":
          total += 10
        elif card == "Ace":
          if total < 11:
            total += 11
          else:
            total += 1
        else:
          total += card
      return total

#offers chance for instructions to player.  time.sleep() used to space out appearance of text
def instructions_query():
  print("Welcome to Blackjack!")
  instruct = input("Would you like to see the rules for Blackjack?  Enter (y)es or (n)o.  ")
  while instruct != "y" and instruct != "yes" and instruct != "n" and instruct !="no":
    instruct = input("Sorry, I did not understand. Would you like to see the rules for Blackjack?  Enter (y)es or (n)o.")
  if instruct == "y" or instruct == "yes":
    clear_output()
    print("The goal of blackjack is to get higher card total than the dealer without going over the limit of 21.")
    time.sleep(2)
    print("""Each player begins with 50 chips and begins each round by placing a bet.  Each player begins with two cards and
can choose to: \n""")
    time.sleep(2)
    print("Hit - recieve a random card from the deck")
    time.sleep(3)
    print("Stand - take no action and let the game proceed to the next player")
    time.sleep(3)
    print("Fold - quit the round and receive half of their initial bet back")
    time.sleep(3)
    print("Double-down - double the investment of chips for the round \n")
    time.sleep(4)
    print("""A player may only choose to Fold or Double-down while they have their first hand.
Face cards are worth 10 points each, and aces can be worth 1 or 11 points.
If a player's dealt-hand is worth 21, they have 'Blackjack,' and instantly recieve 1.5 times their initial bet.
If a player exceeds a hand-value of 21, they forfeit their bet amount.
If a player's hand-value is higher than the hand-value of the dealer, they receive double their bet in chips back.
If a player's hand-value is equal to the hand-value of the dealer, or both the player and dealer have busted,
the player recieves their bet back.    \n""")
    time.sleep(3)
    instruct = input("Would you like to continue?")
  else:
    time.sleep(2)
    pass

#asks for total number of players.  .appends total players to total_player list with dealer as last item.
def ask_for_players():
    clear_output()
    global total_players
    question = input("How many players this game?  Choose 1 - 4: ")
    while question != "1" and question != "2" and question != "3" and question != "4":
        question = input("Sorry, please choose how many players there will be this game from 1 - 4: ")
    if question == "1":
      total_players = [player_1, dealer]
      print("Welcome, Player 1!")
      time.sleep(3)
      clear_output()
    elif question == "2":
      total_players = [player_1, player_2, dealer]
      print("Welcome, Player 1 and Player 2!")
      time.sleep(3)
      clear_output()
    elif question == "3":
      total_players = [player_1, player_2, player_3, dealer]
      print("Welcome, Player 1, Player 2 and Player 3!")
      time.sleep(3)
      clear_output()
    elif question == "4":
      total_players = [player_1, player_2, player_3, player_4, dealer]
      print("Welcome, Player 1, Player 2, Player 3 and Player 4!")
      time.sleep(3)
      clear_output()

#checks if all players but dealer have been removed from game.  If so, offers chance to play again by
#calling ask_for_players() function, repopulating the total_players list and resetting player attributes.
def game_over_check():
  clear_output()
  global total_players
  if len(total_players) == 1:
    print("Game over.  The house wins.")
    time.sleep(3)
    play_again = input("Would you like to play again? Please enter (y)es or (n)o.  ")
    while play_again != "y" and play_again != "yes" and play_again != "n" and play_again != "no":
      play_again = input("Would you like to play again? Please enter (y)es or (n)o.")
    if play_again == "y" or play_again == "yes":
      total_players = []
      clear_output()
      ask_for_players()
      for player in total_players:
        player.player_reset()
    else:
      time.sleep(2)
      print("\nCome back anytime.")


deck = Full_Deck([2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"])

dealer = Computer_Player("Dealer", [], 2000, 0)
player_1 = Player("Player 1", [], 50, 0 )
player_2 = Player("Player 2", [], 50, 0 )
player_3 = Player("Player 3", [], 50, 0 )
player_4 = Player("Player 4", [], 50, 0 )

total_players = []


if __name__=="__main__":
  instructions_query()
  ask_for_players()
  while len(total_players) > 1:
    for player in total_players:
      player.place_bet()
    for player in total_players:
      player.dealt_hand()
      player.black_jack_check()
    for player in total_players:
      player.hit_stand_fold_double()
    for player in total_players:
      player.hand_win_check()
    for player in total_players:
      player.chip_check()
    game_over_check()


