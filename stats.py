"""BlackJack Statistics"""
from time import time

import card
import game
from helper import clear


def main():
    '''
    This function contains the game logic.
    '''
    round_num = 0
    start = time()
    print('Welcome to BlackJack!')

    hand_player = card.Hand.ask_name()
    hand_dealer = card.Hand('Dealer')

    # create and shuffle deck
    new_deck = card.Deck()
    new_deck.shuffle()
    nb_won = 0
    nb_draw = 0
    nb_tests = 1_000
    min_deck_expectancy = 1_000_000
    max_deck_expectancy = 0

    # enter loop for rounds
    for i in range(0, nb_tests):
        clear()
        chips_player = card.Chip.ask_balance()
        # stop the game when player runs out of balance
        if chips_player.balance <= 0:
            print("You're out of balance!")
            round_on = False
            break

        # clear the cards of player and dealer from previous round
        hand_player.clear_hand()
        hand_dealer.clear_hand()
        chips_player.clear_bet()

        # if we have less than 10 cards, we restack/create a new deck and shuffle it
        new_deck.restack()

        round_num += 1
        print(f"Round {round_num} begins!")
        print(f"Available Balance: {chips_player.balance}")

        # ask how much they want to bet for the current round
        chips_player.ask_bet(round_num)

        # deal two cards to the player and the dealer
        for _ in range(2):
            hand_player.add_card(new_deck.deal())
            hand_dealer.add_card(new_deck.deal())

        # last card of dealer has to be facing down
        hand_dealer.cards[1].turn_card_over()

        # display their cards
        game.display_cards(hand_player, hand_dealer)
        # print(f"Deck expectancy: {new_deck.expectancy()}")
        expectancy = new_deck.expectancy()
        if expectancy < min_deck_expectancy:
            min_deck_expectancy = expectancy
        if expectancy > max_deck_expectancy:
            max_deck_expectancy = expectancy
        # players turn, dealers turn
        if game.player_turn(hand_player, hand_dealer, chips_player, new_deck):
            game.dealer_turn(hand_player, hand_dealer, chips_player, new_deck)
        nb_won += chips_player.balance == 2
        nb_draw += chips_player.balance == 1

    # end
    clear()
    print(f"Thank you for playing, Won: {nb_won} Draw: {nb_draw} out of {nb_tests} tries in {time() - start:.3f} ms")
    print(f"Min Expectancy: {min_deck_expectancy:.3f} Max Expectancy: {max_deck_expectancy:.3f}")


main()
input("Press ENTER to exit.......")
