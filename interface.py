from bangtal import *
import time
import random
import os


class MoneyControl():
	money = 0
	bet_money = 0
	chip_list = []

	def __init__(self,init_money=10000): #시작 머니
		self.money = init_money

	### money 관련
	def get_money(self):
		return self.money
	def set_money(self,num):
		self.money = num

	def add_bet_money(self,add_bet_money,show=True): # 돈 배팅
		bet_sound = Sound('./audio/bet.wav')
		bet_sound.play(False)
		self.money -= add_bet_money
		self.bet_money = self.bet_money + add_bet_money
		self.update_money_gui()

	def set_bet_money(self,bet_money,show=True): # 돈 배팅
		self.money -= bet_money
		self.bet_money = bet_money
		self.update_money_gui()

	def cancle_bet(self): # 배팅한 돈 취소
		self.money = self.money + self.bet_money
		self.bet_money = 0
		self.update_money_gui()

	def calc_money(self,multiply=2, score = -1): # 이겼을 때 돈 추가, mul은 배율, 졌을 때도 0 해줘야함 (초기화)
		if score == -1:
			self.bet_money *= multiply
		elif not score:
			self.bet_money = 0
		else:
			while score:
				e = score.pop()
				self.bet_money *= e
			win_sound = Sound('./audio/win.wav')
			win_sound.play(False)

		self.money = self.money + self.bet_money
		self.bet_money = 0
		self.update_money_gui()

	### chip 표시 관련
	def add_chip(self,chip_dir="./images/chip.png",x=600,y=200): #칩 종류 // 지금은 한가지
		chip = Object(chip_dir)
		chip.setScale(0.05)
		self.chip_list.append(chip)

	def show_chip(self,scene,x=600,y=200):
		for i,chip in enumerate(self.chip_list):
			chip.locate(scene, x+10*i, y)
			chip.show()

	def reset_chip(self):
		for chip in self.chip_list:
			chip.hide()
		self.chip_list = []
		self.bet_money = 0

	def print_state(self):
		print("--money state--")
		print(self.money)
		print(self.bet_money)
		print(len(self.chip_list))

	### money_Gui 관련
	def set_money_gui(self,scene,x,y,money_dir):
		self.scene = scene
		self.money_x = x
		self.money_y = y
		self.money_dir = money_dir

		self.money_object = Object(self.money_dir+"money_state.png")
		self.money_object.setScale(0.4)
		self.money_object.locate(self.scene, self.money_x, self.money_y)

		self.money_num_list = []
		count = 0
		for i in range(0,5):
			num_object = Object(self.money_dir + "0.png")
			num_object.setScale(1)
			num_object.locate(self.scene, self.money_x+230-count*20, self.money_y+20)
			num_object.show()
			self.money_num_list.append(num_object)
			count += 1
		self.update_money_gui()
		self.money_object.show()

	def update_money_gui(self):

		self.money_object.show()
		self.money_ui_list = []
		self.money_ui_list.append(self.money_object)
		if self.money < 100:
			showMessage("돈이 다 떨어지셨군요. 특별히 충전해드립니다!")
			self.set_money(1000)
		money = self.money
		number_list = []
		count = 0
		for obj in self.money_num_list:
			obj.hide()

		while True:
			if money == 0 :
				break
			num = money % 10
			self.money_num_list[count].setImage(self.money_dir + str(num)+".png")
			self.money_num_list[count].show()

			count += 1
			money = int(money / 10)
			print(num)



if __name__ == "__main__":

	## 시작할 때
	money_control = MoneyControl(10000) # 처음 돈
	money_control.set_money_gui(scene_table, 100, 100, "./images/number/") # gui 위치할 곳, 이미지 폴더

	##배팅할 때
	money_control.set_bet_money(50)  # 한번에 50원 배팅 ( 배팅금이 아예 무조건 저걸로 설정 )
	money_control.add_bet_money(25) #25원 배팅 추가 ( 배팅금 초기화 안되고 쌓이는 것 )

	money_control.add_chip(chip_dir="./images/chip.png",x=600,y=200) # gui 에 칩 추가. xy는 표시될 로케이션. 칩 이미지 설정 가능
	money_control.show_chip(scene_table) # gui에서 칩 show

	money_control.cancle_bet()  # 배팅 취소 뱃머니 초기화
	money_control.reset_chip()  # 칩도 초기화 (사라짐 )

	money_control.calc_money(2) # 게임 종료시 돈 계산 배율 (승리시 2배 추가) 패배하면 0으로 해주셈 bet_money 초기화 떄문에
	money_control.calc_money(0) 
	
	## money guil 에 출력
	money_control.set_money_gui(scene_table, 100, 100, "./images/number/") # 출력할 scene 및 x,y, img dir

	money_control.update_money_gui() # money 따라 gui 업데이트. 이거는 money 계산할 때마다 자동으로 실행되게 해놨음.
