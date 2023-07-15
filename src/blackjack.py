#!/usr/bin/env python3

from enum import Enum
from random import shuffle


class Suits(Enum):
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3


class Faces(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    Ace = 13


class Action(Enum):
    Hit = 1
    Stand = 2
    DoubleDown = 3
    Split = 4


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def hard_value(self):
        return 11 if self.face == Faces.Ace else min(self.face.value, 10)

    def long_name(self):
        return f'{self.face.name} of {self.suit.name}'

    def short_name(self):
        suit = self.suit.name[0]
        val = self.face.value if self.face.value <= 10 else self.face.name[0]
        return f'{val}{suit}'


def hand_value(cards):
    value = 0
    n_aces = 0

    for c in cards:
        if c.face == Faces.Ace:
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
