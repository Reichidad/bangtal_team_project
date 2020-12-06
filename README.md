# CAU Casino  

 
![image](https://user-images.githubusercontent.com/25008566/101274719-ba70f180-37e3-11eb-805b-08c5fc554c8b.png)

 
 밖에 나갈 수 없는 코로나시대, 
 집에서 신나는 카지노 게임들을 즐겨보세요! 
 
 당신을 위한 시작 Money와, 3종의 게임이 기다리고 있습니다.
 슬롯머신, 블랙잭, 포커 중 원하는 게임을 마음껏 즐기고 돈을 불려보세요. 
  
 bangtal 라이브러리를 이용해 만든 게임입니다.
 
##### Team Project in Opensource sw and python programming class 

---
## Play
`pip install bangtal==0.24` 

`python main_game.py`


---
## Description 

#### main_game

- 게임을 선택할 수 있고, 다시 돌아올 수 있는 메인 화면입니다.
- Money Control 객체를 통해  돈 상태를 공유하고 화면에 실시간으로 출력할 수 있도록 합니다.
- 각 게임은 객체로 따로 관리하며, 각각 Scene과 Object를 갖고 있어 별개 게임 진행이 가능합니다.
- 서로 다른 게임에 들어갔다 나갈 수 있게 파이프라인을 구현했습니다.

    
---
### Slot Machine

![image](https://user-images.githubusercontent.com/25008566/101274903-2e5fc980-37e5-11eb-8258-fd53106c3b59.png)

#### 사용 방법
- Bet버튼을 통해 칩을 겁니다.
- Spin버튼을 통해 플레이 합니다.

#### 규칙
- 총 10개의 문양이 있습니다.
- 가로줄 빙고 1회당 배팅 금액의 10배 입니다.
- 세로줄 빙고 1회당 배팅 금액의 20배 입니다.
- 세로줄 빙고 7잭팟이 터질 경우 배팅 금액의 100배가 됩니다.
- 세로줄 빙고 777잭팟이 터질 경우 배팅 금액의 1000배가 됩니다.

---
### Blackjack

![image](https://user-images.githubusercontent.com/25008566/101274921-420b3000-37e5-11eb-82f4-361b8c5cd262.png)

유명한 카지노 게임인 블랙잭 게임입니다.
https://ko.wikipedia.org/wiki/%EB%B8%94%EB%9E%99%EC%9E%AD

- 딜러와 플레이어 중 카드합이 21에 가까운 사람이 승리합니다.
- 돈을 배팅하고 게임을 시작합니다.
- 플레이어는 카드를 더 받을지 (Hit), 그만 받을지 (Stand) 선택할 수 있습니다.  
그만 받는다면 딜러가 카드를 받습니다. 딜러는 점수가 17을 넘을 때까지 카드를 계속 받아야 합니다.  
- 딜러든 플레이어든 21점이 넘는다면 Burst 되어 패배합니다.  
- JQK 는 10으로 계산되며 ace는 1,11 중 자신에게 유리한 점수로 계산됩니다.
---
- 첫 두장에서 21이 나오면 블랙잭 입니다! 2.5배의 돈을 얻습니다. 
- 그 외 이기면 배팅한 금액의 2.5배를 얻습니다. 
- 지면 배팅한 금액을 잃습니다.

---
##### 특징
- 딜러와 플레이어의 카드 얻기  
- 스코어 계산 및 비교 (ace 의 동적 변화)
- 게임머니 배팅 및 관리
- 카드와 칩 오브젝트 관리

---
### Simple Poker
![image](https://user-images.githubusercontent.com/25008566/101274831-a2e63880-37e4-11eb-97b4-077954cd5fc6.png)

컴퓨터를 상대로 즐기는 간단한 포커 게임입니다.
##### 게임 플레이 방법
  - 화면 중앙의 start 버튼을 누르면 컴퓨터와 플레이어 각각 5장의 뒤집어진 카드를 받고, Bet 버튼과 Game Start 버튼이 생성됩니다.
  - Game Start버튼을 클릭하면 컴퓨터와 플레이어 카드 중 각각 3장씩 오픈됩니다. 이후 베팅 페이즈로 넘어갑니다.  
  플레이어는 이 단계에서 자신이 이길 확률을 파악하고 원하는 만큼 베팅해야합니다.
  - Bet 버튼을 클릭하면 클릭 한 번당 25달러씩 베팅하게됩니다. 플레이어는 베팅 페이즈동안 여러 번 베팅할 수 있습니다.
  - 원하는 만큼 베팅한 뒤 Game Start버튼을 클릭하여 게임의 결과를 확인할 수 있습니다.  
    컴퓨터의 패와 플레이어의 패가 각각 어떤 족보인지 표시하고, 승무패를 출력합니다.
  - 플레이어가 이기면 베팅한 금액의 2배를 얻고, 무승부 시에는 본전만 되찾으며, 패배할 시 베팅한 금액을 모두 잃습니다.
  - Game Start 버튼을 클릭하여 위의 게임을 여러 번 반복하여 플레이할 수 있습니다.
  - Exit 버튼을 클릭하여 게임의 초기 화면으로 돌아가서 게임을 변경할 수 있습니다.
##### 족보
  - 매 게임이 마무리 될 때 컴퓨터와 플레이어의 패가 어떤 족보인지 출력됩니다.
  - 이 게임에서 사용한 족보는 다음과 같습니다.
  1. Royal Flush
  2. Straight Flush
  3. Four of a Kind
  4. Full House
  5. Flush
  6. Straight
  7. Three of a Kind
  8. Two Pair
  9. One Pair
  10. Top
  - 같은 족보일 때는 가장 높은 카드와 상관없이 무승부 처리하였습니다.  
  예) 3 Top과 K Top은 서로 무승부입니다.
  - [Wikipedia - List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)



    
 
