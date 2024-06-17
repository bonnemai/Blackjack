'''
Game module
Contains all necessary functions for the game
'''

import os

from card import Hand
from helper import clear


# from blackjack import clear


def player_choice(hand,chip):
    '''
    This function accepts and validates the choice of what the user's next move will be.
    '''
    valid_options = ['S','H','DD']
    choice = 'wrong'
    
    while True:
        try:
            if len(hand.cards) == 2 and chip.bet <= (chip.balance/2):
                choice = input("Do you want to Stand, Hit or DoubleDown (S or H or DD)?: ")
            else:
                choice = input("Do you want to Stand, Hit (S or H)?: ")
        
            if choice == 'DD' and (len(hand.cards) != 2 or chip.bet > (chip.balance/2)):
                raise ValueError("You cannot Double Down at this point!")
             
            if choice not in valid_options:
                raise ValueError("Select a valid option!")
        
        except ValueError as error:
            print(error)
        
        else:
            return choice


def player_turn(hand_player,hand_dealer,chip,deck):
    '''
    This function takes in the user choice using "player_choice()" function and, depending on that choice, it determines whether the player can continue with the game or if they have lost. 
    Returns True if they can continue or False if they have lost.
    '''
    outcome = True
    print(f"Deck expectancy: {deck.expectancy()}")
    choice ="H" if hand_player.value()+deck.expectancy()<21 else "S"
    # choice = player_choice(hand_player,chip)
    
    while True:
        if choice == 'S':
            clear()
            print("You have decided to Stand!")
            print("Moving on to the dealer!")
            break
            
        if choice == 'H':
            clear()
            hand_player.add_card(deck.deal())
            print("You have decided to Hit! Here are your new cards")
            print(f"Deck expectancy: {deck.expectancy()}")
            display_cards(hand_player,hand_dealer)
            
            if hand_player.value() > 21:
                print(f"{hand_player.name} busted! Dealer wins!")
                chip.remove_balance(chip.bet)
                outcome = False
                break
            
            else:
                # print(f"Deck expectancy: {deck.expectancy()}")
                # choice = player_choice(hand_player,chip)
                choice = "H" if hand_player.value() + deck.expectancy() < 21 else "S"
                continue
                
        if choice == 'DD':
            # os.system('cls')
            clear()
            print("You have decided to Double Down! Here are you're new cards!")
            chip.bet = chip.bet * 2
            hand_player.add_card(deck.deal())
            display_cards(hand_player,hand_dealer)
            
            if hand_player.value() > 21:
                print(f"{hand_player.name} busted! Dealer wins!")
                chip.remove_balance(chip.bet)
                outcome = False
                break
            
            print("Moving on to the Dealer!")
            break
    
    return outcome


def dealer_turn(hand_player,hand_dealer,chip,deck):
    '''
    This function determines what the dealer should do based on his cards and decides who has won the game.
    '''
    hand_dealer.cards[1].turn_card_over()

    display_cards(hand_player,hand_dealer)

    if hand_player.value() == 21 and len(hand_player.cards) == 2:
        if hand_dealer.value() == 21:
            print("It's a push!")
        
        else:
            print(f"{hand_player.name} got a BlackJack!")
            chip.add_balance((3/2)*chip.bet)    
    else:
        while hand_dealer.value() <= 16:
            print("Dealer has less than 17! Dealer gets to Hit!")
            hand_dealer.add_card(deck.deal())
            display_cards(hand_player,hand_dealer)
        
        if hand_dealer.value() > 21:
            print(f"Dealer busts, {hand_player.name} wins!")
            chip.add_balance(chip.bet)
            
        elif hand_dealer.value() > hand_player.value():
            print("Dealer has a higher value! Dealer wins!")
            chip.remove_balance(chip.bet)
        
        elif hand_dealer.value() == hand_player.value():
            print("It's a push!")

        else:
            print(f"{hand_player.name} has a higher value! {hand_player.name} wins!")
            chip.add_balance(chip.bet)


def choice_to_continue():
    '''
    This function accepts and validates the choice of whether the user wants to play another round or not.
    '''
    valid_options = ['Y','N']
    choice = 'wrong'
    
    # while choice not in valid_options:
    #     choice = input("Do you want to play another round (Y os N)?")
    #
    #     if choice not in valid_options:
    #         print("Select a valid option!")
    #     else:
    return 'Y'
            

def display_cards(hand_player=0,hand_dealer=0):
    '''
    This function is used to display cards of either the player or the dealer or both.
    '''
    if hand_player:
        print("\n")
        print(f"{hand_player.name}'s cards ->", end = ' ')
        
        for card in hand_player.cards:
            print(card,end=' ')
        print(f"{Hand('OB',hand_player.cards).value()}")
        # print(f"{hand_player.value()}")
    
    if hand_dealer:
        print(f"Dealer's cards ->", end = ' ')

        for card in hand_dealer.cards:
            print(card,end=' ')
        print(f"{Hand('Dealer',hand_dealer.cards).value()}")
    print('\n')


if __name__ == '__main__':
    print("This is game.py module, please open blackjack.py")
    input("Press ENTER to exit.......")
