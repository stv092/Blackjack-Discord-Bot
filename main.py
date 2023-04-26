import discord
import random


import random


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

def check_blackjack(player_hand, dealer_hand):
    if player_hand.value == BLACKJACK:
        return True
    elif dealer_hand.value == BLACKJACK:
        return True
    else:
        return False

def check_busted(hand):
    if hand.value > BLACKJACK:
        return True
    else:
        return False

async def play_blackjack(message):
    await message.channel.send("Welcome to Blackjack!")
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
        await message.channel.send(f"Player's hand: {player_hand} ({player_hand.value})")
        await message.channel.send(f"Dealer's hand: {dealer_hand.cards[0]}")
        await message.channel.send("Blackjack! Game over.")
        return

    # Show player's hand and dealer's up card
    await message.channel.send(f"Player's hand: {player_hand} ({player_hand.value})")
    await message.channel.send(f"Dealer's up card: {dealer_hand.cards[0]}")

    # Player's turn
    while True:
        # Ask player to hit or stand
        await message.channel.send("Do you want to hit or stand? (type 'hit' or 'stand')")
        response = await client.wait_for('message', check=lambda m: m.author == message.author)
        if response.content.lower() == 'hit':
            player_hand.add_card(deck.draw_card())
            await message.channel.send(f"Player's hand: {player_hand} ({player_hand.value})")
            if check_busted(player_hand):
                await message.channel.send("Busted! Dealer wins. gn")
                return
        else:
            break

    # Dealer's turn
    await message.channel.send(f"Dealer's hand: {dealer_hand} ({dealer_hand.value})")
    while dealer_hand.value < DEALER_STAND:
        dealer_hand.add_card(deck.draw_card())
        await message.channel.send(f"Dealer's hand: {dealer_hand} ({dealer_hand.value})")
        if check_busted(dealer_hand):
            await message.channel.send("Dealer busted! Player wins.")
            return

    # Compare hands and determine winner
    if player_hand.value > dealer_hand.value:
        await message.channel.send("Player wins!")
    elif player_hand.value < dealer_hand.value:
        await message.channel.send("Dealer wins! gn")
    else:
        await message.channel.send("It's a tie!")

    return


intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    
    if message.author.bot:
        return


    if message.content.startswith('!play'):
        
        await message.channel.send("Blackjack game started!")
        await play_blackjack(message)  
       
    elif message.content.startswith('!help'):
        
        await message.channel.send("Welcome to Blackjack! Use !play to start a game.")


#Replace BOT_TOKEN with the token of your Discord bot
client.run('BOT_TOKEN')  
