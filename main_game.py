from bangtal import *
from blackjack_class import Blackjack
from interface import *
from simple_poker import SimplePoker
from slotmachine import SlotMachine

IMG_DIR = "./images/"


scene_main = Scene("main game",IMG_DIR + "main_background.png")
start_money=1000
main_money_control = MoneyControl(start_money)
main_sound = Sound('./audio/main.mp3')
main_sound.play(True)
main_money_control.set_money_gui(scene_main, 10, 10, "./images/number/")



def click_slot(x, y, action):
    global scene_main
    slotmachine_game = SlotMachine(scene_main,main_money_control)

def click_blackjack(x, y, action):
    global scene_main
    blackjack_game = Blackjack(scene_main,main_money_control)


def click_poker(x, y, action):
    global scene_main
    poker_game = SimplePoker(scene_main, main_money_control)
    poker_game.runPoker()


slot_button = Object(IMG_DIR + "button.png")
slot_button.setScale(0.65)
slot_button.locate(scene_main,130,110)
slot_button.onMouseAction = click_slot
slot_button.show()

blackjack_button = Object(IMG_DIR + "button.png")
blackjack_button.setScale(0.65)
blackjack_button.locate(scene_main,510,110)
blackjack_button.onMouseAction = click_blackjack
blackjack_button.show()

poker_button = Object(IMG_DIR + "button.png")
poker_button.setScale(0.65)
poker_button.locate(scene_main,900,110)
poker_button.onMouseAction = click_poker
poker_button.show()

startGame(scene_main)


