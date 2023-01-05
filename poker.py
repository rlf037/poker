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
    
    print(f"The poker hand is {deck.poker_hand()}")
    
    print()
    
    win_player = deck.judge()
    print(f"Winning player is {win_player} with {deck.winning_hand}")
    
class Deck():
    def __init__(self):
        
        deck = []
        
        for suit in SUITS:
            for k in CARD_RANK.keys():
                card = (k, suit)
                deck.append(card)
            
        self.deck = deck
        self.current_players = 0
        self.current_hands = []
        self.flopped = False
        self.turned = False
        self.rivered = False
        self.winning_hand = None
        
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
        
        return (*self.flop, self.turn, self.river)
            
    def size(self):
        return len(self.deck)
    
    def judge(self):
        
        winner = 0
        
        self.winning_hand = []
        return winner
            
if __name__ == "__main__":
    main()
    
    
