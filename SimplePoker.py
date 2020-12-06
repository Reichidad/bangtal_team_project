from bangtal import *
import os
from random import *
import interface

poker_scene = Scene("", 'poker/background.png')

bet_chips = 0
bet_phase = False

# exit button
exit = Object("poker/exit.png")
exit.locate(poker_scene, 1100, 100)
exit.show()

# start button
start = Object("poker/start.png")
start.locate(poker_scene, 540, 100)
start.show()

# reroll button
reroll_icon = Object('poker/button/start.png')
reroll_icon.locate(poker_scene, 400, 300)
reroll_icon.setScale(0.5)

# bet button
bet_btn = Object('poker/button/bet.png')
bet_btn.locate(poker_scene, 250, 300)
bet_btn.setScale(0.5)

# card decks
deck_numbers = [i for i in range(52)]
clubs_directory = 'poker/deck/clubs'
diamonds_directory = 'poker/deck/diamonds'
hearts_directory = 'poker/deck/hearts'
spades_directory = 'poker/deck/spades'
card_back = 'poker/deck/back.png'

clubs = []
diamonds = []
hearts = []
spades = []

# listdir card order : 10, 2, 3, 4, 5, 6, 7, 8, 9, a, j, k ,q
cards = os.listdir(clubs_directory)
# card order edit to : a, 2, 3, 4, 5, 6, 7, 8, 9, 10, j, q ,k
cards[0], cards[9] = cards[9], cards[0]
cards[11], cards[12] = cards[12], cards[11]

# hands & positions
hands = [Object(card_back) for i in range(5)]
hands_number = [0, 0, 0, 0, 0]
positions = [(40, 100), (190, 100), (340, 100), (490, 100), (640, 100)]

# hands & positions
com_hands = [Object(card_back) for i in range(5)]
com_hands_number = [0, 0, 0, 0, 0]
com_positions = [(40, 400), (190, 400), (340, 400), (490, 400), (640, 400)]


# card image list initializing
def init_card(directory, cards, arr):
    for card in cards:
        arr.append(directory + '/' + card)

    return arr


init_card(clubs_directory, cards, clubs)
init_card(diamonds_directory, cards, diamonds)
init_card(hearts_directory, cards, hearts)
init_card(spades_directory, cards, spades)
card_images = [clubs, diamonds, hearts, spades]


def setHands(hands, positions):
    for i in range(5):
        hands[i].locate(poker_scene, positions[i][0], positions[i][1])
        hands[i].setScale(3)
        hands[i].show()


# start button listener -> hide start button / card game init
def startPoker(x, y, action):
    start.hide()
    reroll_icon.show()
    bet_btn.show()
    setHands(hands, positions)
    setHands(com_hands, com_positions)


# 52 cards numbering
numbers = [i for i in range(52)]


# reroll button listener -> a single game playing
def rerollHands(x, y, action):
    global bet_phase, bet_chips, numbers

    if bet_phase is False:
        for i in range(5):
            hands[i].setImage(card_back)
            com_hands[i].setImage(card_back)

        for count in range(3):
            current_card = numbers.pop(randint(0, 51 - count))
            hands_number[count] = current_card
            hands[count].setImage(card_images[current_card % 4][current_card % 13])
            hands[count].show()

        for count in range(3):
            current_card = numbers.pop(randint(0, 48 - count))
            com_hands_number[count] = current_card
            com_hands[count].setImage(card_images[current_card % 4][current_card % 13])
            com_hands[count].show()

        bet_phase = True

    else:
        result_msg = ''

        # for loop -> pick 5 numbers without duplications / save them into hands, hands_number
        for count in range(3, 5):
            current_card = numbers.pop(randint(0, 45 - count))
            hands_number[count] = current_card
            hands[count].setImage(card_images[current_card % 4][current_card % 13])
            hands[count].show()
        # show the hand result
        player_hand, player_msg = handResult(hands_number)
        result_msg += "Your hand : " + player_msg + "\n"

        for count in range(3, 5):
            current_card = numbers.pop(randint(0, 43 - count))
            com_hands_number[count] = current_card
            com_hands[count].setImage(card_images[current_card % 4][current_card % 13])
            com_hands[count].show()

        com_hand, com_msg = handResult(com_hands_number)
        result_msg += "Computer hand : " + com_msg + "\n"
        bet_phase = False
        bet_chips = 0
        numbers = [i for i in range(52)]

        if player_hand < com_hand:
            result_msg += "You win!"
        elif player_hand == com_hand:
            result_msg += "Draw!"
        else:
            result_msg += "You lose!"
        showMessage(result_msg)


# bet button listener
def betOnce(x, y, action):
    global bet_chips
    if bet_phase is True:
        bet_chips += 1
        showMessage("Your bet : " + str(bet_chips))


# exit button listener -> endGame()
def exitGame(x, y, action):
    endGame()


# poker rules calculation
def handResult(hands_number):
    current_hand_kinds = []
    current_hand_numbers = []

    for num in hands_number:
        # 0~ 51 -> kinds / numbers
        current_hand_kinds.append(num % 4)
        current_hand_numbers.append(num % 13)

    # sort for easy calculation
    current_hand_numbers.sort()

    # pair counter
    # one pair -> 1
    # two pair -> 2
    # three of a kind -> 3
    # full house -> 4
    # four of a kind -> 6
    pair_counter = 0
    for n1 in range(0, 4):
        for n2 in range(n1 + 1, 5):
            if current_hand_numbers[n1] == current_hand_numbers[n2]:
                pair_counter = pair_counter + 1

    # flush counter
    # number of kinds
    # 1 -> flush
    flush_counter = len(list(set(current_hand_kinds)))

    # straight counter
    # 4 / pair counter == 0 -> straight
    straight_counter = current_hand_numbers[4] - current_hand_numbers[0]
    if pair_counter != 0:
        straight_counter = -1
    # straight with ace
    # Exception handling for straights with aces
    straight_with_ace = [[0, 1, 2, 11, 12],
                         [0, 1, 10, 11, 12],
                         [0, 1, 2, 3, 12]]

    # result calculation
    if current_hand_numbers == [0, 9, 10, 11, 12] and flush_counter == 1:
        return 1, "Royal Flush"
    elif straight_counter == 4 and flush_counter == 1:
        return 2, "Straight Flush"
    elif pair_counter == 6:
        return 3, "Four of a kind"
    elif pair_counter == 4:
        return 4, "Full House"
    elif flush_counter == 1:
        return 5, "Flush"
    elif straight_counter == 4 or (current_hand_numbers in straight_with_ace):
        return 6, "Straight"
    elif pair_counter == 3:
        return 7, "Three of a kind"
    elif pair_counter == 2:
        return 8, "Two pair"
    elif pair_counter == 1:
        return 9, "One pair"
    else:
        return 10, "Top"


# Prepare for startGame call
bet_btn.onMouseAction = betOnce
exit.onMouseAction = exitGame
start.onMouseAction = startPoker
reroll_icon.onMouseAction = rerollHands
startGame(poker_scene)