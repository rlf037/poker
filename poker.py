import random
from collections import Counter

from data import *


def main():
    
    deck = Deck()
    
    deck.shuffle()
    deck.deal(3)
    
    print()
    
    print(f"Player 1's hand: {deck.current_hands[0]}")
    print(f"Player 2's hand: {deck.current_hands[1]}")
    print(f"Player 3's hand: {deck.current_hands[2]}")
    
    print()
    
    deck.flop()
    deck.turn()
    deck.river()
    deck.poker_hand()
    
    print(f"The shared cards are {deck.shared_cards} and the deck has {deck.size()} cards left")
    
    print()
    
    deck.judge()
    print(f"Winning player is {deck.winning_player} with rank {deck.winning_rank}\n\nCards: {deck.winning_hand}\n")
    
class Deck():
    def __init__(self):
        
        deck = []
        
        for suit in SUITS:
            for k in CARDS.keys():
                card = (k, suit)
                deck.append(card)
            
        self.deck = deck
        self.current_players = 0
        self.current_hands = []
        self.flopped = False
        self.turned = False
        self.rivered = False
        self.winning_hand = None
        
    @staticmethod
    def is_straight(cards):

        count = 0
        
        ranks = [CARDS[card[0]] for card in cards]
        ranks.sort()
        
        for i in range(1, len(ranks)):
            if ranks[i] - ranks[i-1] == 1:
                count += 1
            else:
                if count == 5:
                    break
                count = 0
        
        return count > 4
      
    def shuffle(self):
        
        random.shuffle(self.deck)
        
    def deal(self, players: int):
        
        self.current_players = players
        
        for _ in range(self.current_players):
            
            self.current_hands.append((self.deck.pop(), self.deck.pop()))
            
    def flop(self):
        
        self.flop = (self.deck.pop(), self.deck.pop(), self.deck.pop())
        self.flopped = True
        
    def turn(self):
        
        self.turn = self.deck.pop()
        self.turned = True
        
    def river(self):
        
        self.river = self.deck.pop()
        self.rivered = True
        
    def poker_hand(self):
        
        self.shared_cards = (*self.flop, self.turn, self.river)
        return self.shared_cards
            
    def size(self):
        return len(self.deck)
    
    def judge(self):
        
        self.player_data = []
        
        for player in range(self.current_players):
            
            cards = *self.shared_cards, *self.current_hands[player]
            # print(cards)
            
            card_count = Counter([card[0] for card in cards])
            pairs = list(filter(lambda x: x>1, card_count.values()))
            suit_count = Counter([card[1] for card in cards])
            
            # print(pairs)
            # print(card_count)
            # print(suit_count)
            match = False
            for hand in HANDS.keys():
                
                if hand == "Royal Flush":
                    if 5 in suit_count.values():
                        if all([card[0] in ["A", "K", "Q", "J", "10"] for card in cards]):
                            match = hand
                elif hand == "Straight Flush":
                    if 5 in suit_count.values():
                        if Deck.is_straight(cards):
                            match = hand
                elif hand == "Four of a Kind": 
                    if 4 in card_count.values():
                        match = hand
                elif hand == "Full House":
                    if 3 in card_count.values() and 2 in card_count.values():
                        match = hand
                elif hand == "Flush":
                    if 5 in suit_count.values():
                        match = hand
                elif hand == "Straight":
                    if Deck.is_straight(cards):
                        match = hand
                elif hand == "Three of a Kind":
                    if 3 in card_count.values():
                        match = hand
                elif hand == "Two Pair":
                    if len(pairs) > 1:
                        match = hand
                elif hand == "Pair":
                    if 2 in card_count.values():
                        match = hand
                else:
                    match = hand
                    
                if match:
                    break
                    
            self.player_data.append((cards, match))
            
        highest = 0
        for player in self.player_data:
            rank = HANDS[player[1]]
            if rank > highest:
                highest = rank
                
        ties = list(filter(lambda x: HANDS[x[1]]==highest, self.player_data))
        
        
        
        if len(ties) > 1:
            print(ties)
            tie_data = []
            for index, tie in enumerate(ties):
                if tie[1] == "Flush":
                    suit_count = Counter([card[1] for card in tie[0]])
                    suit = {k for (k, v) in suit_count.items() if v > 4}
                    suit = list(suit.keys())[0]
                    x_sum = sum(CARDS[item[0]] for item in tie if item[1] == suit)
                    tie_data.append((index, x_sum))
                elif tie[1] == "Two Pair":
                    card_count = Counter([card[0] for card in tie[0]])
                    pairs = {k for (k, v) in card_count.items() if v == 2}
                    x_sum = [CARDS[x] for x in pairs]
                    tie_data.append((index, max(x_sum)))
                elif tie[1] == "Three of a Kind":
                    card_count = Counter([card[0] for card in tie[0]])
                    pairs = {k for (k, v) in card_count.items() if v == 3}
                    x_sum = [CARDS[x] for x in pairs]
                    tie_data.append((index, max(x_sum)))
                elif tie[1] == "Pair":
                    card_count = Counter([card[0] for card in tie[0]])
                    pairs = {k for (k, v) in card_count.items() if v == 2}
                    x_sum = [CARDS[x] for x in pairs]
                    tie_data.append((index, max(x_sum)))
                elif tie[1] == "Full House":
                    card_count = Counter([card[0] for card in tie[0]])
                    pairs = {k for (k, v) in card_count.items() if v == 2 or v==3}
                    x_sum = [CARDS[x] for x in pairs]
                    tie_data.append((index, max(x_sum)))
            
            winner = max(tie_data, key=lambda x: x[1])
            winner = self.player_data.index(ties[winner[0]])
        else:     

            winner = max(self.player_data, key=lambda x: HANDS[x[1]])
            winner = self.player_data.index(winner)
            print(winner)
    
        
        self.winning_player = winner + 1
        self.winning_hand = self.player_data[winner][0]
        self.winning_rank = self.player_data[winner][1]
    
            
if __name__ == "__main__":
    main()
    
    
