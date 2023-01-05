import streamlit as st

from data import *
from poker import Deck


def main():
    
    st.subheader("Poker")
    
    players = st.slider("Number of Players", 1, 15, 3)
    
    if st.button("Shuffle"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.deck = Deck()
        st.session_state.deck.shuffle()
        
    if st.button("Deal"):
        st.session_state.deal = True
        st.session_state.deck.deal(players)
    
    if st.button("Flop"):
        st.session_state.flop = True
        st.session_state.deck.flop()
        
    if st.button("Turn"):
        st.session_state.turn = True
        st.session_state.deck.turn()
        
    if st.button("River"):
        st.session_state.river = True
        st.session_state.deck.river()
        st.session_state.deck.poker_hand()

    if st.button("Result"):
        st.session_state.deck.judge()
        st.session_state.result = True
        
    if "deal" in st.session_state:
        
        st.write("Cards left in deck: ", st.session_state.deck.size())
        columns = st.columns(players)
        
        for player, column in enumerate(columns):
            
            with column:
                st.subheader(f"Player {player+1}'s hand:")
                card1 = f"card_imgs/{st.session_state.deck.current_hands[player][0][0]}{st.session_state.deck.current_hands[player][0][1]}.png"
                card2 = f"card_imgs/{st.session_state.deck.current_hands[player][1][0]}{st.session_state.deck.current_hands[player][1][1]}.png"
                st.image([card1, card2], width=150)
                
                if "result" in st.session_state:
                    st.write(f"Rank: {st.session_state.deck.player_data[player][1]}")
                    # st.write(f"Hand: {st.session_state.deck.player_data[player][0]}")
        
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
        
    if "result" in st.session_state:
        st.subheader("Results:")
        st.write(f"Winning player is {st.session_state.deck.winning_player} with rank {st.session_state.deck.winning_rank}")
                
                
if __name__ == "__main__":
    
    st.set_page_config(page_title="Poker", page_icon="♠️", layout="wide", initial_sidebar_state="collapsed")
    
    main()