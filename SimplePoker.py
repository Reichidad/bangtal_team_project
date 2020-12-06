from bangtal import *
import os
from random import *
import interface


class SimplePoker():
    money_control = interface.MoneyControl()
    poker_scene = Scene("", 'images/poker/background.png')

    bet_chips = 0
    bet_phase = False

    exit = Object("images/poker/exit.png")
    start = Object("images/poker/start.png")
    reroll_icon = Object('images/button/start.png')
    bet_btn = Object('images/button/bet.png')

    # card decks
    deck_numbers = [i for i in range(52)]
    clubs_directory = 'images/poker/deck/clubs'
    diamonds_directory = 'images/poker/deck/diamonds'
    hearts_directory = 'images/poker/deck/hearts'
    spades_directory = 'images/poker/deck/spades'
    card_back = 'images/poker/deck/back.png'

    clubs = []
    diamonds = []
    hearts = []
    spades = []
    card_images = []

    # 52 cards numbering
    numbers = [i for i in range(52)]

    # listdir card order : 10, 2, 3, 4, 5, 6, 7, 8, 9, a, j, k ,q
    cards = os.listdir(clubs_directory)

    # hands & positions
    hands = [Object('images/poker/deck/back.png') for i in range(5)]
    hands_number = [0, 0, 0, 0, 0]
    positions = [(40, 100), (190, 100), (340, 100), (490, 100), (640, 100)]

    # hands & positions
    com_hands = [Object('images/poker/deck/back.png') for i in range(5)]
    com_hands_number = [0, 0, 0, 0, 0]
    com_positions = [(40, 400), (190, 400), (340, 400), (490, 400), (640, 400)]

    def __init__(self, start_money):
        self.money_control.set_money(start_money)
        self.money_control.set_money_gui(self.poker_scene, 750, 630, "./images/number/")
        self.money_control.update_money_gui()

        # exit button
        self.exit.locate(self.poker_scene, 1100, 100)
        self.exit.show()

        # start button
        self.start.locate(self.poker_scene, 540, 100)
        self.start.show()

        # reroll button
        self.reroll_icon.locate(self.poker_scene, 400, 300)
        self.reroll_icon.setScale(0.5)

        # bet button
        self.bet_btn.locate(self.poker_scene, 250, 300)
        self.bet_btn.setScale(0.5)

        # card order edit to : a, 2, 3, 4, 5, 6, 7, 8, 9, 10, j, q ,k
        self.cards[0], self.cards[9] = self.cards[9], self.cards[0]
        self.cards[11], self.cards[12] = self.cards[12], self.cards[11]

        self.init_card(self.clubs_directory, self.cards, self.clubs)
        self.init_card(self.diamonds_directory, self.cards, self.diamonds)
        self.init_card(self.hearts_directory, self.cards, self.hearts)
        self.init_card(self.spades_directory, self.cards, self.spades)

        self.card_images = [self.clubs, self.diamonds, self.hearts, self.spades]

        # Prepare for startGame call
        self.bet_btn.onMouseAction = self.betOnce
        self.exit.onMouseAction = self.exitGame
        self.start.onMouseAction = self.startPoker
        self.reroll_icon.onMouseAction = self.rerollHands

    def runPoker(self):
        startGame(self.poker_scene)

    # card image list initializing
    def init_card(self, directory, cards, arr):
        for card in cards:
            arr.append(directory + '/' + card)

        return arr

    def setHands(self):
        for i in range(5):
            self.hands[i].setImage(self.card_back)
            self.hands[i].locate(self.poker_scene, self.positions[i][0], self.positions[i][1])
            self.hands[i].setScale(3)
            self.hands[i].show()
            self.com_hands[i].locate(self.poker_scene, self.com_positions[i][0], self.com_positions[i][1])
            self.com_hands[i].setScale(3)
            self.com_hands[i].show()

    # start button listener -> hide start button / card game init
    def startPoker(self, x, y, action):
        self.start.hide()
        self.reroll_icon.show()
        self.bet_btn.show()
        self.setHands()
        showMessage("Your cards are at the bottom.")

    # reroll button listener -> a single game playing
    def rerollHands(self, x, y, action):
        if self.bet_phase is False:
            for i in range(5):
                self.hands[i].setImage(self.card_back)
                self.com_hands[i].setImage(self.card_back)

            for count in range(3):
                current_card = self.numbers.pop(randint(0, 51 - count))
                self.hands_number[count] = current_card
                self.hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.hands[count].show()

            for count in range(3):
                current_card = self.numbers.pop(randint(0, 48 - count))
                self.com_hands_number[count] = current_card
                self.com_hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.com_hands[count].show()

            self.bet_phase = True

        else:
            result_msg = ''

            # for loop -> pick 5 numbers without duplications / save them into hands, hands_number
            for count in range(3, 5):
                current_card = self.numbers.pop(randint(0, 45 - count))
                self.hands_number[count] = current_card
                self.hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.hands[count].show()
            # show the hand result
            player_hand, player_msg = self.handResult(self.hands_number)
            result_msg += "Your hand : " + player_msg + "\n"

            for count in range(3, 5):
                current_card = self.numbers.pop(randint(0, 43 - count))
                self.com_hands_number[count] = current_card
                self.com_hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.com_hands[count].show()

            com_hand, com_msg = self.handResult(self.com_hands_number)
            result_msg += "Computer hand : " + com_msg + "\n"
            self.bet_phase = False
            self.bet_chips = 0
            self.numbers = [i for i in range(52)]

            if player_hand < com_hand:
                result_msg += "You win!"
            elif player_hand == com_hand:
                result_msg += "Draw!"
            else:
                result_msg += "You lose!"
            showMessage(result_msg)

    # bet button listener
    def betOnce(self, x, y, action):
        if self.bet_phase is True:
            self.bet_chips += 1
            showMessage("Your bet : " + str(self.bet_chips))

    # exit button listener -> endGame()
    def exitGame(self, x, y, action):
        endGame()

    # poker rules calculation
    def handResult(self, hands_number):
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


poker = SimplePoker(10000)
poker.runPoker()