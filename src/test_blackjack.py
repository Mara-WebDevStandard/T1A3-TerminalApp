#!/usr/bin/env python3

from blackjack import *
import pytest

def test_hand_value():
    # autopep8: off

    # No aces
    assert hand_value([Card(Suits.Clubs, Faces.Three),Card(Suits.Clubs, Faces.Jack)]) == 13
    # One hard ace
    assert hand_value([Card(Suits.Clubs, Faces.Ace),Card(Suits.Clubs, Faces.Jack)]) == 21
    # One soft ace
    assert hand_value([Card(Suits.Clubs, Faces.Ace),Card(Suits.Clubs, Faces.Jack), Card(Suits.Clubs, Faces.Two)]) == 13

    # One soft and one hard ace
    assert hand_value([Card(Suits.Clubs, Faces.Ace),Card(Suits.Clubs, Faces.Ace), Card(Suits.Clubs, Faces.Four)]) == 16

    # Two soft aces
    assert hand_value([Card(Suits.Clubs, Faces.Ace), Card(Suits.Clubs, Faces.Ace), Card(Suits.Clubs, Faces.Ten)]) == 12

    # autopep8: off
