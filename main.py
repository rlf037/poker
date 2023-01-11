import time

import streamlit as st

from poker import *

AMENSTY = ['hands_empty', 'deck_empty', 'result_empty', 'players', 'sims', 'interval']

def main():
    
    st.subheader("Poker")
    
    st.session_state.hands_empty = st.empty()
    st.session_state.deck_empty = st.empty()
    st.session_state.result_empty = st.empty()
    
    display()
    
    with st.sidebar:
        st.session_state.players = st.slider("Number of Players", 1, 15, 3)
        
        if st.button("Shuffle"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.deck = Deck()
            st.session_state.deck.shuffle()
            
        if st.button("Deal"):
            st.session_state.deck.deal(st.session_state.players)
            st.session_state.deal = True
        
        if st.button("Flop"):
            st.session_state.deck.flop()
            st.session_state.flop = True
            
        if st.button("Turn"):
            st.session_state.deck.turn()
            st.session_state.turn = True
            
        if st.button("River"):
            st.session_state.deck.river()
            st.session_state.deck.poker_hand()
            st.session_state.river = True

        if st.button("Result"):
            st.session_state.deck.judge()
            st.session_state.result = True
            
        st.session_state.sims = st.slider("Number of Sims", 1, 100, 10)
        st.session_state.interval = st.slider("Delay", min_value=0.1, max_value=10., value=0.5, step=0.1)
    
        if st.button("Run Simulations"):
            
            for _ in range(st.session_state.sims):
                
                for key in st.session_state.keys():
                    if key not in AMENSTY:
                        del st.session_state[key]
                st.session_state.deck = Deck()
                st.session_state.deck.shuffle()
                
                st.session_state.deck.deal(st.session_state.players)
                st.session_state.deal = True
                display()
                time.sleep(st.session_state.interval)
                
                st.session_state.flop = True
                st.session_state.deck.flop()
                display()
                time.sleep(st.session_state.interval)
                
                st.session_state.deck.turn()
                st.session_state.turn = True
                display()
                time.sleep(st.session_state.interval)

                st.session_state.deck.river()
                st.session_state.deck.poker_hand()
                st.session_state.river = True
                display()
                time.sleep(st.session_state.interval)
                
                st.session_state.deck.judge()
                st.session_state.result = True
                display()
                time.sleep(st.session_state.interval)
                    
                
def display():
    
    if "deal" in st.session_state:
        
        with st.session_state.hands_empty.container():
            st.write("Cards left in deck: ", st.session_state.deck.size())
            columns = st.columns(st.session_state.players)
        
            for player, column in enumerate(columns):
                
                with column:
                    st.subheader(f"Player {player+1}'s hand:")
                    card1 = f"card_imgs/{st.session_state.deck.current_hands[player][0][0]}{st.session_state.deck.current_hands[player][0][1]}.png"
                    card2 = f"card_imgs/{st.session_state.deck.current_hands[player][1][0]}{st.session_state.deck.current_hands[player][1][1]}.png"
                    st.image([card1, card2], width=150)
                    
                    if "result" in st.session_state:
                        st.write(f"Rank: {st.session_state.deck.player_data[player][1]}")
                        
                        if player in st.session_state.deck.tiebreak:
                            kicker = f"Kicker: {SDRAC[st.session_state.deck.tiebreak[player][0]]}"
                        else:
                            kicker = ""
                        st.write(kicker)
    
    with st.session_state.deck_empty.container(): 
        if "river" in st.session_state:
            st.subheader("River:")
            card1 = f"card_imgs/{st.session_state.deck.shared_cards[0][0]}{st.session_state.deck.shared_cards[0][1]}.png"
            card2 = f"card_imgs/{st.session_state.deck.shared_cards[1][0]}{st.session_state.deck.shared_cards[1][1]}.png"
            card3 = f"card_imgs/{st.session_state.deck.shared_cards[2][0]}{st.session_state.deck.shared_cards[2][1]}.png" 
            card4 = f"card_imgs/{st.session_state.deck.shared_cards[3][0]}{st.session_state.deck.shared_cards[3][1]}.png"
            card5 = f"card_imgs/{st.session_state.deck.shared_cards[4][0]}{st.session_state.deck.shared_cards[4][1]}.png"
            st.image([card1, card2, card3, card4, card5], width=200)
            
        elif "turn" in st.session_state:
            st.subheader("Turn:")
            card1 = f"card_imgs/{st.session_state.deck.flop[0][0]}{st.session_state.deck.flop[0][1]}.png"
            card2 = f"card_imgs/{st.session_state.deck.flop[1][0]}{st.session_state.deck.flop[1][1]}.png"
            card3 = f"card_imgs/{st.session_state.deck.flop[2][0]}{st.session_state.deck.flop[2][1]}.png"
            card4 = f"card_imgs/{st.session_state.deck.turn[0]}{st.session_state.deck.turn[1]}.png"
            st.image([card1, card2, card3, card4], width=200)
            
        elif "flop" in st.session_state:
            st.subheader("Flop:")
            card1 = f"card_imgs/{st.session_state.deck.flop[0][0]}{st.session_state.deck.flop[0][1]}.png"
            card2 = f"card_imgs/{st.session_state.deck.flop[1][0]}{st.session_state.deck.flop[1][1]}.png"
            card3 = f"card_imgs/{st.session_state.deck.flop[2][0]}{st.session_state.deck.flop[2][1]}.png"
            st.image([card1, card2, card3], width=200)
        
    with st.session_state.result_empty.container():
        if "result" in st.session_state:
            st.subheader("Results:")
            st.write(f"Winning player is {st.session_state.deck.winning_player} with {st.session_state.deck.winning_rank} {'[kicker]' if len(st.session_state.deck.ties) > 1 else ''}")
                    
                
if __name__ == "__main__":
    
    st.set_page_config(page_title="Poker", page_icon="♠️", layout="wide", initial_sidebar_state="expanded")
    
    main()