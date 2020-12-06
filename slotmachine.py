from bangtal import *
import random
from interface import MoneyControl


class Slot_Machine():
    def __init__(self, open_path = 'Images/slot/bg.png'):
        self.scene = Scene("Slot Machine", open_path)
        self.reset()
        self.slot = []
        self.spin = Object('Images/slot/spin.png')
        self.spin.locate(self.scene, 0, 0)
        self.spin.onMouseAction = spin_clicked
        self.moneycontrol = MoneyControl
    def reset_state(self):
        N, M = 5, 3
        
        self.state = [[random.randint(1,9) for _ in range(N)] for _ in range(M)]
        icon_path = ['Images/slot/01.png', 'Images/slot/02.png', 'Images/slot/03.png',
                     'Images/slot/04.png', 'Images/slot/05.png', 'Images/slot/06.png',
                     'Images/slot/07.png', 'Images/slot/08.png', 'Images/slot/09.png', 'Images/slot/10.png']
        
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
                
    def spin_clicked(self, x, y, action):
        self.reset_state()
    
    def get_score(self):
        
            
            