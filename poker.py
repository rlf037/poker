import random
from collections import Counter

CARDS = {
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

SDRAC = {v: k for k, v in CARDS.items()}

SUITS = {"S", "H", "D", "C"}

HANDS = {"Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "Pair": 2,
        "High Card": 1}

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
    def is_straight(cards) -> bool:

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
        self.current_hands = []
        
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
                
        self.ties = list(filter(lambda x: HANDS[x[1]]==highest, self.player_data))
        
        
        self.tiebreak = dict()
        if len(self.ties) > 1:
            indices = [self.player_data.index(x) for x in self.ties]
            # print(self.player_data)
            # print(self.ties)
            # print(indices)
        
            tie_data = []
            for index, tie in enumerate(self.ties):
                if tie[1] == "Flush":
                    suit_count = Counter([card[1] for card in tie[0]])
                    suit = {k for (k, v) in suit_count.items() if v > 4}
                    suit = list(suit)[0]
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
                else:
                    x_sum = [CARDS[x] for x in tie[0]]
                    tie_data.append((index, sum(x_sum)))
                    
                self.tiebreak[indices[index]] = x_sum
                
            winner = max(tie_data, key=lambda x: x[1])
            winner = self.player_data.index(self.ties[winner[0]])
        else:     
            winner = max(self.player_data, key=lambda x: HANDS[x[1]])
            winner = self.player_data.index(winner)

        self.winning_player = winner + 1
        self.winning_hand = self.player_data[winner][0]
        self.winning_rank = self.player_data[winner][1]
