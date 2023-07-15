#!/usr/bin/env python3

from blackjack import *
import pytest

def test_hand_value():
    # autopep8: off

    # No aces
    assert hand_value([Card(Suits.clubs, Faces.three),Card(Suits.clubs, Faces.jack)]) == 13
    # One hard ace
    assert hand_value([Card(Suits.clubs, Faces.ace),Card(Suits.clubs, Faces.jack)]) == 21
    # One soft ace
    assert hand_value([Card(Suits.clubs, Faces.ace),Card(Suits.clubs, Faces.jack), Card(Suits.clubs, Faces.two)]) == 13
    # One soft and one hard ace
    assert hand_value([Card(Suits.clubs, Faces.ace),Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.four)]) == 16
    # Two soft aces
    assert hand_value([Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.ten)]) == 12

    # autopep8: off
