from blackjack import *
import pytest

# tests the score calculation of a given hand in Blackjack
# Numbered cards are worth their face value
# Face cards excluding aces are worth 10
# Aces can be worth 1 or 11 depending on whether the ace's value would cause the hand to bust (value > 21)
# Multiple aces can have different values - e.g 2 aces can be treated as 2 or 12 (11 + 1) depending on overall hand value


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


def blackjack_with_deck(bet, deck):

    funds = bet * 100
    player = CPUPlayer(funds)
    dealer = Dealer(funds)

    round = Round(0, deck, dealer, player, bet, silent=True)
    round.play()
    # check if round ended after blackjack
    assert len(round.pcards) == 2
    assert len(round.dcards) == 2
    return round.winnings

# test rounds correctly end when dealer or player draws blackjack (when two initial cards dealt == 21) and that payout is correct
# expected payouts: dealer blackjack = lose bet, player blackjack = win 1.5x bet, both blackjack = break-even
def test_blackjack():

    # test based on implementation detail - that first two cards dealt consecutively , first to dealer and then to player.
    # cards are pulled from the back of the deck in order
    # e.g if deck is [A,B,C,D] then starting cards will be: Player [B,A], Dealer [D,C]

    bet = 50

    # dealer will draw a blackjack initially and player won't - player should lose bet to dealer
    deck = [Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.nine), Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.ten)]
    assert blackjack_with_deck(bet, deck) == -bet

    # player will draw a blackjack initially and dealer won't - player should win 1.5x bet
    deck = [Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.ten), Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.nine)]
    assert blackjack_with_deck(bet, deck) == bet * 1.5

    # player and dealer will both draw a blackjack initially - player should break/even
    deck = [Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.ten), Card(Suits.clubs, Faces.ace), Card(Suits.clubs, Faces.ten)]
    assert blackjack_with_deck(bet, deck) == 0

