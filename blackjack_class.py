from bangtal import *
import time
import random
import os
from interface import MoneyControl

class Blackjack():
    IMG_DIR = "./images/"
    BUTTON_DIR = IMG_DIR + "button/"
    CARDS_DIR = IMG_DIR + "card/"
    background_name = "table"

    scene_table = Scene("Blackjack",IMG_DIR+background_name+".jpg")



    def __init__(self,scene_main,main_money_control):
        showMessage("Welcome to blackjack table")
        self.scene_main  = scene_main
        self.scene_table.enter()
        #self.money_control = MoneyControl(now_money)
        self.money_control = main_money_control
        self.money_control.set_money_gui(self.scene_table,10,10,"./images/number/")
        self.chip_list = []


        self.dealers_cards = []
        self.players_cards = []
        self.card_obj_list = []

        self.exit = Object(self.IMG_DIR + "exit.png")
        self.exit.setScale(1)
        self.exit.locate(self.scene_table,1000, 20)
        self.exit.onMouseAction = self.click_exit
        self.exit.show()


        self.dispensor = Object(self.IMG_DIR + "card_deck.png")
        self.dispensor.setScale(0.4)
        self.dispensor.locate(self.scene_table, 300, 500)
        self.dispensor.onMouseAction = self.click_start
        self.dispensor.show()

        self.start_but = Object(self.BUTTON_DIR + "start.png")
        self.start_but.setScale(0.4)
        self.start_but.locate(self.scene_table, 400, 20)
        self.start_but.onMouseAction = self.click_start
        self.start_but.show()

        self.bet_but = Object(self.BUTTON_DIR + "bet.png")
        self.bet_but.setScale(0.4)
        self.bet_but.locate(self.scene_table, 600, 20)
        self.bet_but.onMouseAction = self.click_bet
        self.bet_but.show()

        self.clear_but = Object(self.BUTTON_DIR + "clear.png")
        self.clear_but.setScale(0.4)
        self.clear_but.locate(self.scene_table, 800, 20)
        self.clear_but.onMouseAction = self.click_clear
        self.clear_but.show()

        self.hit_but = Object(self.BUTTON_DIR + "hit.png")
        self.hit_but.setScale(0.4)
        self.hit_but.locate(self.scene_table, 500, 20)
        self.hit_but.onMouseAction = self.click_hit
        # self.hit_but.show()

        self.stand_but = Object(self.BUTTON_DIR + "stand.png")
        self.stand_but.setScale(0.4)
        self.stand_but.locate(self.scene_table, 700, 20)
        self.stand_but.onMouseAction = self.click_stand
        # self.stand_but.show()

        self.back_cards = Object(self.CARDS_DIR + "back.jpg")
        self.back_cards.setScale(0.08)
        self.back_cards.locate(self.scene_table, 550, 500)

        # self.back_cards.show()



    def get_cards(self):
        card = random.randint(0,51)
        shape = 0
        if card < 13:
            shape = 0
        elif card < 26:
            shape = 1
        elif card < 39:
            shape = 2
        else:
            shape = 3

        num = card - shape * 13 + 1
        return [shape,num]


    def calc_score(self,card_list):
        sum = 0
        ace_stack = 0

        for shape,num in card_list:
            if num == 1:
                ace_stack += 1
            elif num > 10:
                num = 10
            sum += num

        while ace_stack != 0:
            print("ace")
            if sum < 12:
                sum += 10
            else:
                sum += 1
            ace_stack -= 1
        print("sum : " + str(sum))
        return sum

    def str_score(self):

        p_score = str(self.calc_score(self.players_cards))
        d_score = str(self.calc_score(self.dealers_cards))

        return "dealer : " + d_score + " / me : " + p_score


    def show_cards(self,mode): #mode = 1 > show back / 0 > show card


        for obj in self.card_obj_list:
            obj.hide()
            print("===")
        self.card_obj_list = []

        d_width = 450
        d_count = 0
        p_width = 450
        p_count = 0

        if mode == 1:

            self.back_cards.show()
            d_count += 1

        shape_name = ""
        val_name = ""

        for i in range(mode,len(self.dealers_cards)):
            d_count += 1
            shape,value = self.dealers_cards[i]
            if shape == 0:
                shape_name = "diamonds"
            elif shape == 1:
                shape_name = "hearts"
            elif shape == 2:
                shape_name = "clubs"
            elif shape == 3:
                shape_name = "spades"

            if value == 1:
                val_name = "ace"
            elif value == 11:
                val_name = "jack"
            elif value == 12:
                val_name = "queen"
            elif value == 13:
                val_name = "king"
            else:
                val_name = str(value)

            card_obj = Object(self.CARDS_DIR + val_name + "_of_" + shape_name + ".png")
            card_obj.setScale(0.14)
            card_obj.locate(self.scene_table, d_width + d_count * 100, 500)
            card_obj.show()
            self.card_obj_list.append(card_obj)

        for i in range(0,len(self.players_cards)):
            p_count += 1
            shape,value = self.players_cards[i]
            if shape == 0:
                shape_name = "diamonds"
            elif shape == 1:
                shape_name = "hearts"
            elif shape == 2:
                shape_name = "clubs"
            elif shape == 3:
                shape_name = "spades"

            if value == 1:
                val_name = "ace"
            elif value == 11:
                val_name = "jack"
            elif value == 12:
                val_name = "queen"
            elif value == 13:
                val_name = "king"
            else:
                val_name = str(value)

            card_obj = Object(self.CARDS_DIR + val_name + "_of_" + shape_name + ".png")
            card_obj.setScale(0.14)
            card_obj.locate(self.scene_table, p_width + p_count * 100, 100)
            card_obj.show()
            self.card_obj_list.append(card_obj)

    def hide_cards(self):
        for card in self.card_obj_list:
            card.hide()
        self.back_cards.hide()

    def click_exit(self, x, y, action):
        self.money_control.set_money_gui(self.scene_main, 10, 10, "./images/number/")
        self.money_control.update_money_gui()

        self.hide_chip()
        self.hide_cards()
        self.clear_scene()
        self.scene_main.enter()

        self.start_but.hide()
        self.bet_but.hide()
        self.clear_but.hide()


    def click_start(self,x, y, action):


        game_end = False

        player_card_width = 120
        if self.money_control.bet_money == 0:
            showMessage("Bet your money!!")
            self.clear_scene()
            return 0

        self.start_but.hide()
        self.bet_but.hide()
        self.clear_but.hide()


        self.dealers_cards.append(self.get_cards())
        self.dealers_cards.append(self.get_cards())
        self.players_cards.append(self.get_cards())
        self.players_cards.append(self.get_cards())

        dealer_score = self.calc_score(self.players_cards)
        player_score = self.calc_score(self.players_cards)
        if player_score == 21:
            game_end = True
            #self.hide_cards()
            self.show_cards(1)
            showMessage("!!!!!!!!! blackjack !!!!!!!!!")
            self.money_control.calc_money(2.5)
            self.hide_chip()
            #self.hide_cards()
            self.clear_scene()
            return 0
        self.hide_cards()
        self.show_cards(1)

        showMessage("Dealer score : " + str(dealer_score)+"\nMy score : "+ str(player_score))

        self.hit_but.show()
        self.stand_but.show()



    def click_hit(self,x, y, action):

        new_card = self.get_cards()
        self.players_cards.append(new_card)
        self.show_cards(1)

        score = self.calc_score(self.players_cards)
        if score > 21:
            showMessage(" --- BURST --- \n" + "Lose " + str(self.money_control.bet_money) + "$")
            #self.hide_cards()
            self.clear_scene()


    def click_stand(self,x, y, action):

        d_burst = False

        d_score = self.calc_score(self.dealers_cards)
        p_score = self.calc_score(self.players_cards)

        score = self.calc_score(self.players_cards)
        # if score > 21:
        #     showMessage(" --- BURST --- ")
        #     print("--")
        #     print(len(self.card_obj_list))
        #     self.hide_cards()
        #     self.clear_scene()
        #     return 0

        while d_score < 17:
            self.dealers_cards.append(self.get_cards())
            d_score = self.calc_score(self.dealers_cards)
            showMessage("My money : " + str(self.money_control.get_money()) + "$")
        if d_score > 21:
            showMessage("Dealer Burst!!\n Get " + str(self.money_control.bet_money * 2) + "$"+ "\n" + self.str_score())
            self.money_control.calc_money(2)
        elif d_score > p_score:
            showMessage("Dealer Win!!\n Lose " + str(self.money_control.bet_money) + "$"+  "\n" +self.str_score())
        elif d_score < p_score:
            showMessage("Player Win!!\n Get " + str(self.money_control.bet_money * 2) +"$"+ "\n" +self.str_score())
            self.money_control.calc_money(2)
        else:
            self.money_control.calc_money(1)
            showMessage("Draw\n" )

        self.hide_chip()
        self.show_cards(0)
        #self.hide_cards()
        #self.show_cards(0)
        self.clear_scene()
        self.money_control.print_state()


    def clear_scene(self):



        self.hit_but.hide()
        self.stand_but.hide()

        self.start_but.show()
        self.bet_but.show()
        self.clear_but.show()
        self.hide_chip()
        bet_money = 0

        self.players_cards = []
        self.dealers_cards = []
        #self.card_obj_list = []

        #showMessage("My money : " + str(my_money) + "$")




    def hide_chip(self):
        self.money_control.reset_chip()


    def click_bet(self,x, y, action):


        height = len(self.chip_list) * 10 + 600
        self.hide_cards()

        self.money_control.add_bet_money(25)
        self.money_control.add_chip()
        self.money_control.show_chip(self.scene_table)


        self.money_control.print_state()


    def click_clear(self,x, y, action):

        self.hide_cards()
        self.money_control.cancle_bet()
        self.money_control.reset_chip()

    def return_money(self):
        self.main_money_control.set_money(self.money_control.get_money())
        self.main_money_control.update_money_gui()








if __name__ == "__main__":
    Blackjack()