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
        val = self.face.value if self.face.value <= 10 else self.face.name[0].upper(
        )
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

    for _ in range(count):
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

    def double_down(self, pcards, dcards):
        return read_yn("Double down")


class CPUPlayer:
    def __init__(self, funds):
        self.funds = funds
        self.init_funds = funds
        self.stood = False

    def bet(self):
        return min(self.init_funds / 20, self.funds)

    def choice(self, pcards, dcards):
        if hand_value(pcards) >= 17:
            self.stood = True
            return Action.stand
        return Action.hit

    def double_down(self, pcards, dcards):
        return False


class Dealer:
    def __init__(self, funds):
        self.funds = funds
        self.stood = False

    def choice(self, pcards, dcards):
        if hand_value(dcards) >= 17:
            self.stood = True
            return Action.stand
        return Action.hit


class Round:
    def __init__(self, round, deck, dealer, player, bet, silent=False):
        self.round = round
        self.deck = deck
        self.dealer = dealer
        self.player = player
        self.bet = bet
        self.dcards = []
        self.pcards = []
        self.silent = silent
        self.winnings = 0

    def result_str(self):
        if self.winnings < 0:
            return "Lost"
        elif self.winnings == 0:
            return "Tied"
        return "Won"

    def summarize(self):
        return f'#{self.round}. Dealer cards: {hand_to_str(self.dcards)} ({hand_value(self.dcards)}) | Player cards: {hand_to_str(self.pcards)} ({hand_value(self.pcards)}) | {self.result_str()} ${abs(self.winnings):.2f}'

    def print(self, msg):
        if not self.silent:
            print(f'#{self.round}. {msg}')

    def play(self):
        self.winnings = self.run_game()
        self.player.funds += self.winnings
        self.dealer.funds -= self.winnings
        # reset stood state for next round
        self.player.stood = False
        self.dealer.stood = False

        if hand_value(self.pcards) > 21:
            self.print("Player went bust!")
        elif hand_value(self.dcards) > 21:
            self.print("Dealer went bust!")

        if self.winnings > 0:
            self.print(f'Player won! Winnings = ${self.winnings:.2f}')
        elif self.winnings == 0:
            self.print(f'Player tied! Winnings = $0.00')
        else:
            self.print(f'Player lost! Losses = ${-self.winnings:.2f}')

        self.print(
            f'Player funds = ${self.player.funds:.2f} | Dealer funds = ${self.dealer.funds:.2f}')

    def run_game(self):
        self.dcards = [self.deck.pop(), self.deck.pop()]
        self.pcards = [self.deck.pop(), self.deck.pop()]

        d_bjack = hand_value(self.dcards) == 21
        p_bjack = hand_value(self.pcards) == 21

        if d_bjack or p_bjack:
            self.print(f'Dealer cards: {hand_to_str(self.dcards)}')
            self.print(f'Player cards: {hand_to_str(self.pcards)}')

        if d_bjack and p_bjack:  # break even
            self.print(f' Player and dealer got blackjack')
            return 0
        if p_bjack:  # 3:2 payout for blackjack
            self.print(f'Player got blackjack!')
            return self.bet * 1.5
        if d_bjack:
            self.print(f'Dealer got blackjack')
            return -self.bet  # lose bet

        # special case for hidden card on first round
        self.print(f'Dealer cards: [{self.dcards[0].short_name()}][**]')
        self.print(f'Player cards: {hand_to_str(self.pcards)}')

        # give player option to double down
        if self.player.double_down(self.pcards, self.dcards):
            self.bet *= 2
            self.pcards.append(self.deck.pop())
            self.player.stood = True

            self.print(f'Player cards: {hand_to_str(self.pcards)}')

            if hand_value(self.pcards) > 21:  # player bust
                return -self.bet

        while True:

            if not self.player.stood:
                if self.player.choice(self.pcards, self.dcards) == Action.hit:
                    self.pcards.append(self.deck.pop())
                    self.print(f'Player cards: {hand_to_str(self.pcards)}')
                    if hand_value(self.pcards) > 21:
                        return -self.bet

            if not self.dealer.stood:
                if self.dealer.choice(self.pcards, self.dcards) == Action.hit:
                    self.dcards.append(self.deck.pop())
                    self.print(f'Dealer cards: {hand_to_str(self.dcards)}')
                    if hand_value(self.dcards) > 21:
                        return self.bet

            if self.dealer.stood and self.player.stood:
                p_val = hand_value(self.pcards)
                d_val = hand_value(self.dcards)

                self.print(f'Player score: {p_val} | Dealer score: {d_val}')

                if p_val > d_val:
                    return self.bet
                elif p_val < d_val:
                    return -self.bet
                else:  # p_val == d_val
                    return 0


def blackjack_main(simulate, max_rounds, dealer_funds, player_funds, summarize):

    deck = make_decks(5)
    shuffle(deck)

    dealer = Dealer(dealer_funds)

    if simulate:
        player = CPUPlayer(player_funds)
    else:
        player = Player(player_funds)

    history = []

    cur_round = 0

    while cur_round < max_rounds and dealer.funds > 0 and player.funds > 0:

        try:
            bet = player.bet()
            round = Round(cur_round + 1, deck, dealer,
                          player, bet, silent=simulate)
            round.play()
            cur_round += 1
            history.append(round)

            # safe heuristic to avoid card exhaustion mid round
            if len(deck) < 20:
                addon = make_decks(1)
                shuffle(addon)
                deck = addon + deck

        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            print(f"Unknown error: {e}")
            break

    if simulate or summarize:
        for h in history:
            print(h.summarize())

    print(
        f'Player funds = ${player.funds:.2f} | Dealer funds = ${dealer.funds:.2f}')

    print(f'Rounds played: {cur_round}')

    if cur_round == max_rounds + 1:
        print('Enough rounds for you! Time to do something more productive!')
    elif dealer.funds <= 0:
        print('Looks like you cleared out the house... Congratulations!')
    elif player.funds <= 0:
        print('Looks like you\'ve emptied your pockets. Better luck next time.')
    else:
        print('Had enough? Come back soon!')


if __name__ == "__main__":

    parser = ArgumentParser(
        prog='BlackJack', description='The timeless game of blackjack brought to the terminal')

    parser.add_argument('-r', '--rounds', type=int, default=100,
                        help="Maximum number of rounds before game ends")
    parser.add_argument('-d', '--dealer-funds', type=float,
                        default=10000, help="Initial amount of dealer funds")
    parser.add_argument('-p', '--player-funds', type=float,
                        default=500, help="Initial amount of player funds")
    parser.add_argument('--simulation', action='store_true',
                        help="Watch the computer play.")
    parser.add_argument('--summarize', action='store_true',
                        help="Watch the computer play.")

    args = parser.parse_args()

    blackjack_main(args.simulation, args.rounds,
                   args.dealer_funds, args.player_funds, args.summarize)
