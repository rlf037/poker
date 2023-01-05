import random

CARD_RANK = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

SUITS = {"S", "H", "D", "C"}

HANDS = {"High Card": 0,
         "Pair": 1,
         "Two Pair": 2,
         "Three of a Kind": 3,
         "Straight": 4,
         "Flush": 5,
         "Full House": 6,
         "Four of a Kind": 7,
         "Straight Flush": 8,
         "Royal Flush": 9}

