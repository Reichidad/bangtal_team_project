from bangtal import *
import os
from random import *

scene1 = Scene("", 'poker/background.png')

# exit button
exit = Object("poker/exit.png")
exit.locate(scene1, 1100, 100)
exit.show()

# start button
start = Object("poker/start.png")
start.locate(scene1, 540, 100)
start.show()

# reroll button
reroll_icon = Object('poker/reroll.png')
reroll_icon.locate(scene1, 700, 100)

# help button
help = Object("poker/help.png")
help.locate(scene1, 10, 230)
help.show()

# help text
help_text = Object("poker/help_text.png")
help_text.locate(scene1, 50, 0)

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
positions = [(40, 310), (190, 310), (340, 310), (490, 310), (640, 310)]

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

# start button listener -> hide start button / card game init
def startPoker(x, y, action):
    start.hide() 
    reroll_icon.show()
    for i in range(5):
        hands[i].locate(scene1, positions[i][0], positions[i][1])
        hands[i].setScale(3)
        hands[i].show()

# reroll button listener -> a single game playing
def rerollHands(x, y, action):
    # 52 cards numbering
    numbers = [i for i in range(52)]
    # for loop -> pick 5 numbers without duplications / save them into hands, hands_number
    for count in range(5):
        current_card = numbers.pop(randint(0, 51 - count))
        hands_number[count] = current_card
        hands[count].setImage(card_images[current_card % 4][current_card % 13])
        hands[count].show()
    # show the hand result
    showMessage(handResult())

# exit button listener -> endGame()
def exitGame(x, y, action):
    endGame()

# help button listener -> show help_text
def showHelp(x, y, action):
    help_text.show()

# help_text listener -> close the help
def exitHelp(x, y, action):
    if 220 < x < 280 and 0 < y < 50:
        help_text.hide()

# poker rules calculation
def handResult():
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
        for n2 in range(n1+1, 5):
            if current_hand_numbers[n1] == current_hand_numbers[n2]:
                pair_counter = pair_counter + 1

    # flush counter
    # number of kinds
    # 1 -> flush
    flush_counter = len(list(set(current_hand_kinds)))

    # straight counter
    # 4 / pair counter == 0 -> straight
    straight_counter = current_hand_numbers[4] - current_hand_numbers[0]
    if pair_counter != 0 :
        straight_counter = -1
    # straight with ace
    # Exception handling for straights with aces
    straight_with_ace = [[0, 1, 2 ,11 ,12],
                         [0, 1, 10, 11, 12],
                         [0, 1, 2, 3, 12]]

    # result calculation
    if current_hand_numbers == [0, 9, 10, 11, 12] and flush_counter == 1:
        return "Royal Flush"
    elif straight_counter == 4 and flush_counter == 1:
        return "Straight Flush"
    elif pair_counter == 6:
        return "Four of a kind"
    elif pair_counter == 4:
        return "Full House"
    elif flush_counter == 1:
        return "Flush"
    elif straight_counter == 4 or (current_hand_numbers in straight_with_ace) :
        return "Straight"
    elif pair_counter == 3:
        return "Three of a kind"
    elif pair_counter == 2:
        return "Two pair"
    elif pair_counter == 1:
        return "One pair"
    elif current_hand_numbers[0] == 0:
        return "A Top"
    else:
        num_to_str = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q' ,'K']
        return num_to_str[current_hand_numbers[4]] + " Top"

# Prepare for startGame call
exit.onMouseAction = exitGame
start.onMouseAction = startPoker
help.onMouseAction = showHelp
help_text.onMouseAction = exitHelp
reroll_icon.onMouseAction = rerollHands
startGame(scene1)