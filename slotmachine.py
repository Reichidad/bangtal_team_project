from bangtal import *
import random
from interface import MoneyControl


class Slot_Machine():
    def __init__(self, scene_main, main_money_control):
        self.main = scene_main
        self.scene = Scene("Slot Machine", './images/slot/bg.png')
        self.scene.enter()
        self.moneycontrol = main_money_control
        self.slot = [] #Object 모음
        
        #spin button
        self.spin = Object('./images/slot/spin.png')
        self.spin.locate(self.scene, 0, 0)
        self.spin.onMouseAction = spin_clicked
        
        #bet button
        self.bet = Object('./images/slot/bet.png')
        self.bet.locate(self.scene, 0, 0)
        self.bet.onMouseAction = bet_clicked
        
        #exit button
        self.exit = Object('./images/slot/exit.png')
        self.exit.locate(self.scene, 0, 0)
        self.exit.onMouseAction = exit_clicked

        
        
    def reset_state(self, N, M):        
        self.state = [[random.randint(1,9) for _ in range(N)] for _ in range(M)]
        icon_path = ['./images/slot/01.png', './images/slot/02.png', './images/slot/03.png',
                     './images/slot/04.png', './images/slot/05.png', './images/slot/06.png',
                     './images/slot/07.png', './images/slot/08.png', './images/slot/09.png', './images/slot/10.png']
        
        dx, dy, init_x, init_y = 0, 0, 0, 0
        
        while self.slot:
            e = self.slot.pop()
            e.hide()
        
        for i in range(M):
            for j in range(N):
                x = init_x + (dx*i)
                y = init_y + (dy*j)
                slot = Object(icon_path[self.state[i][j]])
                slot.locate(self.scene, x, y)
                slot.show()
                self.slot.append(show)

    def get_score(self, N, M):
        score = []
        for i in range(N):
            temp = dict()
            for j in range(M):
                if not self.state[j][i] in temp:
                    temp.update({self.state:1})
                else:
                    temp[self.state] += 1
            for e in temp.keys():
                if temp[e] == M:
                    score.appned(2)
                    
        for j in range(M):
            temp = dict()
            for i in range(N):
                if not self.state[j][i] in temp:
                    temp.update({self.state:1})
                else:
                    temp[self.state] += 1
            for e in temp.keys():
                if temp[e] == N:
                    if e == 1:
                        score.append(30)
                    elif e == 2:
                        score.append(100)
                    else:
                        score.appned(4)
        self.moneycontrol.calc_money(score = score)
        self.moneycontrol.cancle_bet()
        self.moneycontrol.reset_chip()

                
    def spin_clicked(self, x, y, action):
        N, M = 5, 3
        self.reset_state(N, M)
        self.get_score(N, M)
        
    def bet_clicked(self, x, y, action):
        self.moneycontrol.add_bet_money(25)
        self.moneycontrol.add_chip()
        self.moneycontrol.show_chip()
        
    def exit_clicked(self, x, y, action):
        self.moneycontrol.set_money_gui(self.main, 10, 10, "./images/number/")
        self.moneycontrol.update_money_gui()
        self.main.enter()
        
    
        
            