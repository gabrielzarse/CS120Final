# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:30:15 2023

@author: gdzar
"""

from random import choice, randint

masterDeck = ["A", "A", "A", "A",
               "2", "2", "2", "2",
               "3", "3", "3", "3",
               "4", "4", "4", "4",
               "5", "5", "5", "5",
               "6", "6", "6", "6",
               "7", "7", "7", "7",
               "8", "8", "8", "8",
               "9", "9", "9", "9",
               "10", "10", "10", "10",
               "J", "J", "J", "J",
               "Q", "Q", "Q", "Q",
               "K", "K", "K", "K"]


def setup(deck):
    # Initialize all of the hands
    playerHand, deck = pickCards(deck)
    dealerHand, deck = pickCards(deck)
    return deck, playerHand, dealerHand


def pickCards(deck):
    hand = []
    if len(deck) <= 6:
        deck = masterDeck.copy()
    for card in range(0, 2):
        chosenCard = choice(deck)
        hand.append(chosenCard)
        deck.remove(chosenCard)
    return hand, deck


def PrintUI(playerHand, dealerHand, deck, gameState):
    print()
    if gameState == "playerDealing":
        print("The dealer has these cards:\n_, " + ", ".join(dealerHand[1:]))
        print()
        print("You have these cards:\n" + ", ".join(playerHand))
        print()
        print(f"There are {len(deck)} cards left in the deck")
    elif gameState == "dealerDealing":
        print("The dealer has these cards:\n" + ", ".join(dealerHand))
        print()
        print("You have these cards:\n" + ", ".join(playerHand))
        print()
        if haveWon(playerHand, dealerHand):
            print("You have beaten the dealer.")
        else:
            print("You have not beaten the dealer.")
    else:
        print("Something has gone wrong")
        while True:
            pass


def haveWon(playerHand, dealerHand):
    numeric_playerHand = numericCards(playerHand.copy())
    playerhandTotal = 0
    for card in numeric_playerHand:
        playerhandTotal += card
    numeric_dealerHand = numericCards(dealerHand.copy())
    dealerhandTotal = 0
    for card in numeric_dealerHand:
        dealerhandTotal += card
    if dealerhandTotal > 21:
        if playerhandTotal > 21:
            return False
            print("you have busted")
        return True
    if dealerhandTotal == 21:
        return False
    if dealerhandTotal < 21:
        if dealerhandTotal < playerhandTotal <= 21:
            return True
        return False


def bettingPhase(tokens):
    print(f"You have {tokens} tokens.")
    while True:
        try:
            bet = int(input("Please enter you bet: "))
            if int(bet) > 0:
                if (tokens - bet) >= 0:
                    break
                print("You do not have enough to bet that ammount.")
            else:
                print("Please enter a number greater than zero.")
        except ValueError:
            print("Please enter a number.")
    return tokens - bet, bet


def playerDealing(deck, playerHand, gameState):
    if not deck:
        print("There are no cards left in the deck, the round ends.")
        gameState = "dealerDealing"
    else:
        while True:
            userCommand = input("Would you like to hit or to stay? (H/S): ").lower()
            if userCommand == "h":
                chosenCard = choice(deck)
                playerHand.append(chosenCard)
                deck.remove(chosenCard)
                break
            elif userCommand == "s":
                gameState = "dealerDealing"
                break
            else:
                print("Please only enter H for hit or S for stay.")
    return deck, playerHand, gameState


def dealerDealing(deck, dealerHand):
    while True:
        if not deck:
            break
        numeric_dealerHand = numericCards(dealerHand.copy())
        handTotal = 0
        for card in numeric_dealerHand:
            handTotal += card
        if handTotal < 16:
            chosenCard = choice(deck)
            dealerHand.append(chosenCard)
            deck.remove(chosenCard)
        elif handTotal == 16:
            if randint(0, 1):
                chosenCard = choice(deck)
                dealerHand.append(chosenCard)
                deck.remove(chosenCard)
            else:
                break
        elif 11 in numeric_dealerHand and handTotal > 21:
            for cardNumber, card in enumerate(numeric_dealerHand):
                if card == 11:
                    numeric_dealerHand[cardNumber] = 1
        else:
            break
    return deck, dealerHand


def numericCards(hand):
    for cardNumber, card in enumerate(hand):
        if card == "J" or card == "Q" or card == "K":
            hand[cardNumber] = 10
        elif card == "A":
            hand[cardNumber] = 11
        else:
            hand[cardNumber] = int(hand[cardNumber])
    handTotal = 0
    for card in hand:
        handTotal += card
    if handTotal > 21 and 11 in hand:
        for cardNumber, card in enumerate(hand):
            if card == 11:
                hand[cardNumber] = 1
    return hand


def playAgain():
    while True:
        playAgain = input("Do you want to play again? (Y/N): ").lower()
        if playAgain == "y":
            break
        elif playAgain == "n":
            quit()
        print("Please only enter a Y or N")


deck = masterDeck.copy()
tokens = 200

while True:
    gameState = "betting"
    playingGame = True

    deck, playerHand, dealerHand = setup(deck)

    while playingGame:
        if gameState == "betting":
            tokens, bet = bettingPhase(tokens)
            gameState = "playerDealing"
        else:
            PrintUI(playerHand, dealerHand, deck, gameState)
            deck, playerHand, gameState = playerDealing(deck, playerHand, gameState)
            if gameState == "dealerDealing":
                deck, dealerHand = dealerDealing(deck, dealerHand)
                if haveWon(playerHand, dealerHand):
                    tokens += 2 * bet
                PrintUI(playerHand, dealerHand, deck, gameState)
                playingGame = False
    if tokens:
        playAgain()
    else:
        input("You are all out of tokens. Hit enter to quit.")
        quit()