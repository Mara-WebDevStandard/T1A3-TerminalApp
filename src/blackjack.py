#!/usr/bin/env python3

from enum import Enum
from random import shuffle
from utilities import *
from argparse import ArgumentParser


class Suits(Enum):
    clubs = 0
    diamonds = 1
    hearts = 2
    spades = 3


class Faces(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    ace = 13


class Action(Enum):
    hit = 1
    stand = 2


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def hard_value(self):
        return 11 if self.face == Faces.ace else min(self.face.value, 10)

    def long_name(self):
        return f'{self.face.name.capitalize()} of {self.suit.name.capitalize()}'

    def short_name(self):
        suit = self.suit.name[0].upper()
        val = self.face.value if self.face.value <= 10 else self.face.name[0].upper()
        return f'{val}{suit}'
    
def hand_to_str(cards):
    return "".join([f'[{c.short_name()}]' for c in cards])

def hand_value(cards):
    value = 0
    n_aces = 0

    for c in cards:
        if c.face == Faces.ace:
            n_aces += 1
        value += c.hard_value()

    while n_aces > 0 and value > 21:
        value -= 10
        n_aces -= 1

    return value

def make_decks(count):
    cards = []

    for i in range(count):
        for s in Suits:
            for f in Faces:
                cards.append(Card(s, f))

    return cards

class Player:
    def __init__(self, funds):
        self.funds = funds
        self.stood = False

    def bet(self):
        while True:
            bet = read_num("Please enter a wager")

            if bet < 0:
                print("Unable to place a negative bet!")
            elif bet > self.funds:
                print("Not enough funds!")
            else:
                return bet  

    def choice(self, pcards, dcards):
        while True:
            act = read_enum("Enter a choice", Action)
            if act == Action.stand:
                self.stood = True
            return act
        
class Dealer:
    def __init__(self, funds):
        self.funds = funds
        self.stood = False

    def choice(self, pcards, dcards):
        if hand_value(dcards) >= 17:
            self.stood = True
            return Action.stand
        else:
            return Action.hit

# returns winnings amount to player (negative for a loss)
def blackjack_round(deck, dealer, player, bet):

    d_cards = [deck.pop(), deck.pop()]
    p_cards = [deck.pop(), deck.pop()]

    d_bjack = hand_value(d_cards) == 21
    p_bjack = hand_value(p_cards) == 21
    push = d_bjack and p_bjack

    if d_bjack or p_bjack:
        print(f'Dealer cards: {hand_to_str(d_cards)}')
        print(f'Player cards: {hand_to_str(p_cards)}')  

    if push: # break even
       print('Player and dealer got blackjack')
       return 0
    elif p_bjack: # 3:2 payout for blackjack
        print('Player got blackjack!')
        return bet * 1.5
    elif d_bjack:
        print('Dealer got blackjack')
        return -bet # lose bet
        
    #special case for hidden card on first round
    print(f'Dealer cards: [{d_cards[0].short_name()}][**]')
    print(f'Player cards: {hand_to_str(p_cards)}')

    #give player option to double down
    if (read_yn("Double down")):
        bet *= 2
        p_cards.append(deck.pop())

        while not dealer.stood:
            if dealer.choice(p_cards, d_cards) == Action.hit:
                d_cards.append(deck.pop())
        
        print(f'Dealer cards: {hand_to_str(d_cards)}')
        print(f'Player cards: {hand_to_str(p_cards)}')

        p_val = hand_value(p_cards)
        d_val = hand_value(d_cards)

        if p_val > 21: # player always loses if bust - even if dealer busts too
            print('Player went bust!')
            return -bet
        elif d_val > 21:
            print('Dealer went bust!')
            return bet
        elif p_val > d_val:
            return bet
        elif p_val < d_val:
            return -bet
        else: # p_val == d_val
            return 0

    while True:

        if not player.stood:
            if player.choice(p_cards, d_cards) == Action.hit:
                p_cards.append(deck.pop())
                if hand_value(p_cards) > 21:
                    print(f'Player cards: {hand_to_str(p_cards)}')
                    print('Player went bust!')
                    return -bet
        

        if not dealer.stood:
            if dealer.choice(p_cards, d_cards) == Action.hit:
                d_cards.append(deck.pop())
                if hand_value(d_cards) > 21:
                    print(f'Dealer cards: {hand_to_str(d_cards)}')
                    print('Dealer went bust!')
                    return bet

        print(f'Dealer cards: {hand_to_str(d_cards)}')
        print(f'Player cards: {hand_to_str(p_cards)}')

        if dealer.stood and player.stood:
            p_val = hand_value(p_cards)
            d_val = hand_value(d_cards)

            print(f'Player score: {p_val} | Dealer score: {d_val}')

            if p_val > d_val:
                return bet
            elif p_val < d_val:
                return -bet
            else: # p_val == d_val
                return 0
                


def blackjack_main(max_rounds, deck_size, dealer_funds, player_funds):

    #TODO - what happens when cards run out mid round?
    deck = make_decks(deck_size)
    shuffle(deck)

    dealer = Dealer(dealer_funds)
    player = Player(player_funds)

    rounds_left = max_rounds

    while rounds_left > 0 and dealer.funds > 0 and player.funds > 0:

        try:
            print(f'Player funds = ${player.funds} | Dealer funds = ${dealer.funds}')
            bet = player.bet()
            winnings = blackjack_round(deck, dealer, player, bet)
            player.funds += winnings
            dealer.funds -= winnings

            if (winnings > 0):
                print(f'Player won! Winnings = ${winnings:.2f}')
            elif winnings == 0:
                print('Player tied! Winnings = $0.00')
            else:
                print(f'Player lost! Losses = ${-winnings:.2f}')

            rounds_left -= 1

        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Unknown error: {e}")
            break

        
    print(f'Player funds = ${player.funds} | Dealer funds = ${dealer.funds}')

    if rounds_left == 0:
        print('Enough rounds for you! Time to do something more productive!')
    elif dealer.funds <= 0:
        print('Looks like you cleared out the house... Congratulations!')
    elif dealer.funds <= 0:
        print('Looks like you''ve emptied your pockets. Better luck next time.')
    else:
        print(f'Had enough? Come back soon!')        

if __name__ == "__main__":

    parser = ArgumentParser(prog='BlackJack', description='The timeless game of blackjack brought to the terminal')

    parser.add_argument('-r', '--rounds', type=int, default=100, help="Maximum number of rounds before game ends")
    parser.add_argument('-d', '--dealer-funds', type=float, default=10000, help="Initial amount of dealer funds")
    parser.add_argument('-p', '--player-funds', type=float, default=500, help="Initial amount of player funds")
    parser.add_argument('-D', '--deck-size', type=int, default=5, help="Number of standard 52 card decks in use")

    args = parser.parse_args()

    blackjack_main(args.rounds, args.deck_size, args.dealer_funds, args.player_funds)
