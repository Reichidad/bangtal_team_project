from bangtal import *
import time
import random
import os

SOLVE = 15

IMG_DIR = "./images/"
BUTTON_DIR = IMG_DIR + "button/"
CARDS_DIR = IMG_DIR + "card/"
background_name = "table"

scene_table = Scene("Blackjack",IMG_DIR+background_name+".jpg")
showMessage("Welcome to blackjack table")

my_money = 10000
bet_money = 0
chip_list = []

dealers_cards = []
players_cards = []
card_obj_list = []

def get_cards():
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


def calc_score(card_list):
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

def str_score():
    global players_cards,dealers_cards

    p_score = str(calc_score(players_cards))
    d_score = str(calc_score(dealers_cards))

    return "dealer : " + d_score + " / me : " + p_score


def show_cards(mode): #mode = 1 > show back / 0 > show card
    global card_obj_list
    global back_cards

    for obj in card_obj_list:
        obj.hide()
    card_obj_list = []

    d_width = 450
    d_count = 0
    p_width = 450
    p_count = 0

    if mode == 1:

        back_cards.show()
        d_count += 1

    shape_name = ""
    val_name = ""

    for i in range(mode,len(dealers_cards)):
        d_count += 1
        shape,value = dealers_cards[i]
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

        card_obj = Object(CARDS_DIR + val_name + "_of_" + shape_name + ".png")
        card_obj.setScale(0.14)
        card_obj.locate(scene_table, d_width + d_count * 100, 500)
        card_obj.show()
        card_obj_list.append(card_obj)

    for i in range(0,len(players_cards)):
        p_count += 1
        shape,value = players_cards[i]
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

        card_obj = Object(CARDS_DIR + val_name + "_of_" + shape_name + ".png")
        card_obj.setScale(0.14)
        card_obj.locate(scene_table, p_width + p_count * 100, 100)
        card_obj.show()
        card_obj_list.append(card_obj)

def hide_cards():
    global card_obj_list,back_cards

    for card in card_obj_list:
        card.hide()
    back_cards.hide()


def click_start(x, y, action):
    global scene_table
    global start_but, bet_but, clear_but
    global bet_money,my_money
    global dealers_cards,players_cards
    global hit_but, stand_but

    game_end = False

    player_card_width = 120
    if bet_money == 0:
        showMessage("Bet your money!!")
        clear_scene()
        return 0


    my_money = my_money - bet_money
    start_but.hide()
    bet_but.hide()
    clear_but.hide()


    dealers_cards.append(get_cards())
    dealers_cards.append(get_cards())
    players_cards.append(get_cards())
    players_cards.append(get_cards())

    dealer_score = calc_score(players_cards)
    player_score = calc_score(players_cards)
    if player_score == 21:
        game_end = True
        hide_cards()
        show_cards(1)
        showMessage("!!!!!!!!! blackjack !!!!!!!!!")
        my_money = my_money + int (bet_money * 2.5)
        return 0
    hide_cards()
    show_cards(1)

    showMessage("Dealer score : " + str(dealer_score)+"\nMy score : "+ str(player_score))

    hit_but.show()
    stand_but.show()



def click_hit(x, y, action):
    global players_cards

    new_card = get_cards()
    players_cards.append(new_card)
    show_cards(1)

    score = calc_score(players_cards)
    if score > 21:
        showMessage(" --- BURST --- \n" + "Lose " + str(bet_money) + "$")
        clear_scene()


def click_stand(x, y, action):
    global players_cards,dealers_cards, my_money
    d_burst = False

    d_score = calc_score(dealers_cards)
    p_score = calc_score(players_cards)


    while d_score < 17:
        dealers_cards.append(get_cards())
        d_score = calc_score(dealers_cards)
    showMessage("My money : " + str(my_money) + "$")
    if d_score > 21:
        showMessage("Dealer Burst!!\n Get " + str(bet_money * 2) + "$"+ " My money : " + str(my_money) + "$\n" + str_score())
        my_money += bet_money * 2
    elif d_score > p_score:
        showMessage("Dealer Win!!\n Lose " + str(bet_money) + "$"+ " My money : " + str(my_money) + "$\n" +str_score())
    elif d_score < p_score:
        showMessage("Player Win!!\n Get " + str(bet_money * 2) +"$"+ " My money : " + str(my_money) + "$\n" +str_score())
        my_money += bet_money * 2
    else:
        my_money + bet_money
        showMessage("Draw\n" + " My money : " + str(my_money) + "$")

    hide_chip()
    hide_cards()
    show_cards(0)
    clear_scene()









    score = calc_score(players_cards)
    if score > 21:
        showMessage(" --- BURST --- ")
        clear_scene()



def clear_scene():
    global start_but,bet_but,clear_but
    global hit_but,stand_but
    global players_cards,dealers_cards
    global bet_money,my_money


    hit_but.hide()
    stand_but.hide()

    start_but.show()
    bet_but.show()
    clear_but.show()
    hide_chip()
    bet_money = 0

    players_cards = []
    dealers_cards = []
    card_obj_list = []

    #showMessage("My money : " + str(my_money) + "$")




def hide_chip():
    global chip_list
    for chip in chip_list:
        chip.hide()
    chip_list = []






def click_bet(x, y, action):
    global scene_table
    global start_but, bet_but, clear_but
    global chip_list, bet_money

    height = len(chip_list) * 10 + 600
    hide_cards()

    bet_money += 25
    chip = Object(IMG_DIR + "chip.png")
    chip.setScale(0.05)
    chip.locate(scene_table, height, 200)
    chip.show()
    chip_list.append(chip)


def click_clear(x, y, action):
    global scene_table
    global start_but, bet_but, clear_but
    global chip_list

    hide_cards()
    for chip in chip_list:
        chip.hide()
    chip_list = []


dispensor = Object(IMG_DIR + "card_deck.png")
dispensor.setScale(0.4)
dispensor.locate(scene_table,300,500)
dispensor.onMouseAction = click_start
dispensor.show()


start_but = Object(BUTTON_DIR + "start.png")
start_but.setScale(0.4)
start_but.locate(scene_table,400,20)
start_but.onMouseAction = click_start
start_but.show()

bet_but = Object(BUTTON_DIR + "bet.png")
bet_but.setScale(0.4)
bet_but.locate(scene_table,600,20)
bet_but.onMouseAction = click_bet
bet_but.show()

clear_but = Object(BUTTON_DIR + "clear.png")
clear_but.setScale(0.4)
clear_but.locate(scene_table,800,20)
clear_but.onMouseAction = click_clear
clear_but.show()


hit_but = Object(BUTTON_DIR + "hit.png")
hit_but.setScale(0.4)
hit_but.locate(scene_table,500,20)
hit_but.onMouseAction = click_hit
#hit_but.show()

stand_but = Object(BUTTON_DIR + "stand.png")
stand_but.setScale(0.4)
stand_but.locate(scene_table,700,20)
stand_but.onMouseAction = click_stand
#stand_but.show()

back_cards = Object(CARDS_DIR + "back.jpg")
back_cards.setScale(0.08)
back_cards.locate(scene_table, 550, 500)

#back_cards.show()



startGame(scene_table)

