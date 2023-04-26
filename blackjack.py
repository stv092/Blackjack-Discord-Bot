import random

# Define constants
SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
BLACKJACK = 21
DEALER_STAND = 17

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.rank]

    def adjust_for_ace(self):
        while self.value > BLACKJACK and 'A' in [card.rank for card in self.cards]:
            for card in self.cards:
                if card.rank == 'A' and self.value > BLACKJACK:
                    self.value -= 10
                    break

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])

def print_game_state(player_hand, dealer_hand, player_busted=False, dealer_busted=False):
    print(f"Player hand: {player_hand} ({player_hand.value}{' (Busted)' if player_busted else ''})")
    print(f"Dealer hand: {dealer_hand.cards[0]} and [Hidden Card]")
    if dealer_busted:
        print("Dealer busted!")
    print()

def check_blackjack(player_hand, dealer_hand):
    if player_hand.value == BLACKJACK:
        print_game_state(player_hand, dealer_hand)
        print("Congratulations! You got a Blackjack!")
        return True
    elif dealer_hand.value == BLACKJACK:
        print_game_state(player_hand, dealer_hand)
        print("Dealer got a Blackjack. You lose!")
        return True
    else:
        return False

def check_busted(hand):
    if hand.value > BLACKJACK:
        return True
    else:
        return False

def play_blackjack():
    print("Welcome to Blackjack!")
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    # Deal initial cards
    player_hand.add_card(deck.draw_card())
    player_hand.add_card(deck.draw_card())
    dealer_hand.add_card(deck.draw_card())
    dealer_hand.add_card(deck.draw_card())

    # Check for blackjack
    if check_blackjack(player_hand, dealer_hand):
        return

    # Player's turn
    while True:
        print_game_state(player_hand, dealer_hand)
        choice = input("Do you want to hit or stand? ").lower()
        if choice == 'hit':
            player_hand.add_card(deck.draw_card())
            if check_busted(player_hand):
                print_game_state(player_hand, dealer_hand, player_busted=True)
                print("You busted! You lose.")
                return False
        elif choice == 'stand':
            print("Player stands.")
            break
        else:
            print("Invalid choice. Please enter 'hit' or 'stand'.")

    # Dealer's turn
    print("\nDealer's turn.")
    print(f"Dealer's hand: {dealer_hand}")
    while dealer_hand.value < DEALER_STAND:
        dealer_hand.add_card(deck.draw_card())
        print(f"Dealer draws a card: {dealer_hand.cards[-1]}")
        if check_busted(dealer_hand):
            print_game_state(player_hand, dealer_hand, dealer_busted=True)
            print("Dealer busted! You win!")
            return True

    # Compare hands and determine winner
    print_game_state(player_hand, dealer_hand)
    if player_hand.value > dealer_hand.value:
        print("You win!")
        return True
    elif player_hand.value < dealer_hand.value:
        print("You lose!")
        return False
    else:
        print("It's a tie!")
        return False

#This starts the game :)
play_blackjack()

