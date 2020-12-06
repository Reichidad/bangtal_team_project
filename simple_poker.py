from bangtal import *
import os
from random import *
import interface

class SimplePoker():
    tutorial_flag = True
    poker_scene = Scene("", 'images/poker/background.png')

    bet_phase = False
    result_phase = False

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

    def __init__(self, main_scene, main_money_control):
        self.scene_main = main_scene
        self.money_control = main_money_control
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
    
    # run the simple poker game
    def runPoker(self):
        self.poker_scene.enter()

    # card image list initializing
    def init_card(self, directory, cards, arr):
        for card in cards:
            arr.append(directory + '/' + card)

        return arr 

    # set hands with card backward
    def setHands(self):
        for i in range(5):
            self.hands[i].setImage(self.card_back)
            self.hands[i].locate(self.poker_scene, self.positions[i][0], self.positions[i][1])
            self.hands[i].setScale(3.3)
            self.hands[i].show()
            self.com_hands[i].locate(self.poker_scene, self.com_positions[i][0], self.com_positions[i][1])
            self.com_hands[i].setScale(3.3)
            self.com_hands[i].show()

    # start button listener -> hide start button / card game init
    def startPoker(self, x, y, action):
        self.start.hide() 
        self.reroll_icon.show()
        self.bet_btn.show()
        self.setHands()
        self.numbers = [i for i in range(52)]
        if self.tutorial_flag:
            showMessage("[튜토리얼 - Simple Poker]\n당신의 패는 아래쪽, 상대(컴퓨터)의 패는 위쪽입니다.\nGame Start 버튼을 눌러보세요!")

    # reroll button listener -> a single game playing
    def rerollHands(self, x, y, action):

        # start phase : before bet, show 3 hands
        if self.bet_phase is False:
            # all cards backward
            for i in range(5):
                self.hands[i].setImage(self.card_back)
                self.com_hands[i].setImage(self.card_back)
            # User hands for loop -> pick 3 numbers without duplications / save them into hands, hands_number
            print(len(self.numbers))
            for count in range(3):
                current_card = self.numbers.pop(randint(0, 51 - count))
                self.hands_number[count] = current_card
                self.hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.hands[count].show()

            # Computer hands
            for count in range(3):
                current_card = self.numbers.pop(randint(0, 48 - count))
                self.com_hands_number[count] = current_card
                self.com_hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.com_hands[count].show()

            # bet phase flag on
            self.bet_phase = True
            # tutorial message
            if self.tutorial_flag:
                showMessage("[튜토리얼 - Simple Poker]\n당신과 상대의 패를 3장씩 오픈합니다.\n지금부터 원하는 만큼 베팅을 할 수 있습니다! Bet 버튼을 눌러보세요.")
        
        # result phase : after bet, show 2 more hands and result
        elif self.result_phase:
            result_msg = ''
        
            # User hands for loop -> pick 2 numbers without duplications / save them into hands, hands_number
            for count in range(3, 5):
                current_card = self.numbers.pop(randint(0, 45 - count))
                self.hands_number[count] = current_card
                self.hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.hands[count].show()

            # result message edit
            player_hand, player_msg = self.handResult(self.hands_number)
            result_msg += "플레이어 : " + player_msg + "\n"

            # Computer hands
            for count in range(3, 5):
                current_card = self.numbers.pop(randint(0, 43 - count))
                self.com_hands_number[count] = current_card
                self.com_hands[count].setImage(self.card_images[current_card % 4][current_card % 13])
                self.com_hands[count].show()

            # result message edit
            com_hand, com_msg = self.handResult(self.com_hands_number)
            result_msg += "상대(컴퓨터) : " + com_msg + "\n"

            # reset flag and values
            self.bet_phase = False
            self.bet_chips = 0
            self.numbers = [i for i in range(52)]
            self.tutorial_flag = False
            self.result_phase = False
    
            # result message edit
            if player_hand < com_hand:
                result_msg += "당신이 이겼습니다! 2 배의 상금이 주어집니다!"
                win_sound = Sound('./audio/win.wav')
                win_sound.play(False)
                self.money_control.calc_money(2)
            elif player_hand == com_hand:
                result_msg += "비겼습니다! 본전!"
                self.money_control.calc_money(1)
            else:
                result_msg += "당신이 졌습니다!"
                self.money_control.calc_money(0)

            result_msg += "\nGame Start 버튼을 눌러 게임을 반복할 수 있습니다."

            # reset money_control
            self.money_control.cancle_bet()
            self.money_control.reset_chip()
            # show result
            showMessage(result_msg)

        # no bet in bet phase
        else:
            showMessage("최소 한 번은 베팅해주세요.")

    # bet button listener
    def betOnce(self, x, y, action):
        if self.bet_phase is True:
            self.money_control.add_bet_money(25)
            self.money_control.add_chip(chip_dir="./images/chip.png")
            self.money_control.show_chip(self.poker_scene, x=600, y=300)
            if self.tutorial_flag:
                showMessage("[튜토리얼 - Simple Poker]\n칩을 베팅했습니다. 하나의 칩은 25달러입니다. Game Start버튼을 한번 더 누르면 이번 게임의 결과를 확인할 수 있습니다.")
            self.result_phase = True

    # exit button listener -> endGame()
    def exitGame(self, x, y, action):
        # 게임 초기화
        self.start.show() 
        self.reroll_icon.hide()
        self.bet_btn.hide()

         # reset flag and values
        self.bet_phase = False
        self.bet_chips = 0
        self.numbers = [i for i in range(52)]
        self.tutorial_flag = True
        self.result_phase = False

        for i in range(5):
            self.hands[i].setImage(self.card_back)
            self.com_hands[i].setImage(self.card_back)
            self.hands[i].hide()
            self.com_hands[i].hide()

        # reset money_control
        self.money_control.calc_money(0)
        self.money_control.cancle_bet()
        self.money_control.reset_chip()
        self.money_control.set_money_gui(self.scene_main, 10, 10, "./images/number/")
        self.money_control.update_money_gui()
        self.scene_main.enter()

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
            return 1, "Royal Flush"
        elif straight_counter == 4 and flush_counter == 1:
            return 2, "Straight Flush"
        elif pair_counter == 6:
            return 3, "Four of a kind"
        elif pair_counter == 4:
            return 4, "Full House"
        elif flush_counter == 1:
            return 5, "Flush"
        elif straight_counter == 4 or (current_hand_numbers in straight_with_ace) :
            return 6, "Straight"
        elif pair_counter == 3:
            return 7, "Three of a kind"
        elif pair_counter == 2:
            return 8, "Two pair"
        elif pair_counter == 1:
            return 9, "One pair"
        else:
            return 10, "Top"

# 이렇게 객체 선언하고 runPoker()로 실행하면 됨
# 객체 선언할 때 현재 money_control 잔액 넘겨주면 됨
