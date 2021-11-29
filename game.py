from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from board import Board

D = True
class QuoridorGame(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(400, 500, 1000,700) # 조절해야함 4k 기준
        # init Layout
        quoridorLayout = QGridLayout()
        self.setLayout(quoridorLayout)

        # init board_button
        self.board_button = []
        for y in range(17):
            tmp_board = []
            for x in range(17):
                tmp_button = QPushButton()
                tmp_button.setMaximumSize(34,34) #boxsize 제한 34가 ui그리드에 딱 맞는 크기 
                tmp_button.clicked.connect(self.btnclick)
                if y%2 or x%2:
                    tmp_button.setStyleSheet("background-color: gray")
                else:
                    tmp_button.setStyleSheet("background-color: white")
                
                quoridorLayout.addWidget(tmp_button, y, x)
                tmp_board.append(tmp_button)
            self.board_button.append(tmp_board)
        
        # Display widget for current status
        self.player1block = QLineEdit()
        self.player1block.setReadOnly(True)
        quoridorLayout.addWidget(self.player1block, 0, 18)
        
        self.statusText = QLineEdit()
        self.statusText.setReadOnly(True)
        quoridorLayout.addWidget(self.statusText, 6, 18)
        
        self.change_btn = QToolButton()
        self.change_btn.setText("가로")
        self.change_btn.clicked.connect(self.change_dir)
        quoridorLayout.addWidget(self.change_btn, 8, 18)
        
        self.currentturn = QLineEdit()
        quoridorLayout.addWidget(self.currentturn, 10, 18)


        self.player2block = QLineEdit()
        self.player2block.setReadOnly(True)
        quoridorLayout.addWidget(self.player2block, 16, 18)
        self.startGame()
        
        self.setMouseTracking(True) #mouse 현재 위치 픽셀 계산

    def mouseMoveEvent(self, pos):
        
        self.mouseXpos = 0
        self.mouseYpos = 0
        x = pos.x()
        y = pos.y()
        x -= 11
        y -= 11
        self.mouseXpos = int(x/43) #43을 조절해야함
        self.mouseYpos = int(y/43) #43을 조절해야함 지금은 4k 기준 
        text = f"x: {x+11}, y: {y+11}, gridx: {self.mouseXpos}, gridy: {self.mouseYpos}"
        if self.mouseXpos<=16 and self.mouseYpos<=16:
            self.wallcheker(self.mouseXpos,self.mouseYpos)
        if D:
            print(text)
 
    def startGame(self):
        self.board = Board()
        self.turn = 2 # player1
        self.board.whereCanMove(self.turn)
        self.color_4()

        self.wall_count = [10,10]
        self.player1block.setText("player1 은 벽 개수 : "+str(self.wall_count[0]))
        self.player2block.setText("player2 남은 벽 개수 : "+str(self.wall_count[1]))
        
        self.currentturn.setText("Red turn")
        self.currentturn.setStyleSheet("color : Red")

        self.board_button[0][8].setStyleSheet("background-color : red")
        self.board_button[16][8].setStyleSheet("background-color : blue")
    
    def change_dir(self):
        btn = self.sender()
        btn.setText("가로" if btn.text() == "세로" else "세로")
        self.board.set_direction(0 if btn.text() == "가로" else 1)

    def btnclick(self):
        (y, x) = self.find_btn(self.sender())
        if D:
            print(f"mouse clicked x: {x}, y: {y} ")
        if y % 2 or x % 2:  # 벽 세우는 곳임
            if self.wall_count[self.turn - 2] <= 0:
                self.statusText.setText("벽이 부족합니다!")
                # 벽이 없습니다
                return 
            if self.board.wall_clicked(y, x):
                # 설치 & status 변경
                for tmp in [0, -1, 1]:
                    yy = y + tmp*self.board.direction
                    xx = x + tmp*(1 - self.board.direction)
                    self.board.status[yy][xx] = 1
                    self.board_button[yy][xx].setStyleSheet("background-color : brown")
                # 벽 개수 감소
                self.wall_count[self.turn - 2] -= 1
                # 턴 종료
                self.next_turn()
            else:
                self.statusText.setText("설치 불가능한 지역입니다!")
        else:  # 말이 움직이는 곳임
            if self.board.player_clicked(y, x):
                #말 이동
                (i,j) = self.board.find_board(self.turn)
                self.board.status[y][x] = self.turn
                self.board.status[i][j] = 0
                self.board_button[y][x].setStyleSheet("background-color : " + ("red " if self.turn == 2 else "blue"))
                self.board_button[i][j].setStyleSheet("background-color : white")
                self.next_turn()
    
    
    def wallcheker(self,x,y): 
        for i in range(17):
            for j in range(17):
                if (i%2 or j%2) and self.board.status[i][j] == 0:     
                        self.board_button[i][j].setStyleSheet("background-color : gray")
        
        if y % 2 or x % 2:  
            if self.board.wall_check(y, x):    
                for tmp in [0, -1, 1]:
                    yy = y + tmp*self.board.direction
                    xx = x + tmp*(1 - self.board.direction)
                    self.board_button[yy][xx].setStyleSheet("background-color : yellow")

    def find_btn(self, btn):
        for i in range(17):
            for j in range(17):
                if self.board_button[i][j] == btn:
                    return (i,j)

    def next_turn(self):
        (y, x) = self.board.find_board(self.turn)
        if (3 - self.turn) * 16 == y:
            self.statusText.setStyleSheet("color : " + ("red " if self.turn == 2 else "blue"))
            self.statusText.setText(("Red " if self.turn == 2 else "Blue") + "의 승리!")
            self.erase_4()
            return
        #erase 하기

        self.turn = 5 - self.turn
        self.erase_4()
        self.board.whereCanMove(self.turn)
        self.color_4()
        
        self.player1block.setText("1번 플레이어 남은 벽 개수 : " + str(self.wall_count[0]))
        self.player2block.setText("2번 플레이어 남은 벽 개수 : " + str(self.wall_count[1]))
        
        self.statusText.setText("")
        if self.turn == 2:
            self.currentturn.setText("Red turn")
            self.currentturn.setStyleSheet("color : Red")
        else:
            self.currentturn.setText("Blue turn")
            self.currentturn.setStyleSheet("color : Blue")
        pass

    def erase_4(self):
        for i in range(17):
            for j in range(17):
                if self.board.status[i][j] == 4:
                    self.board.status[i][j] = 0
                    self.board_button[i][j].setStyleSheet("background-color : white")

    
    def color_4(self):
        for i in range(17):
            for j in range(17):
                if self.board.status[i][j] == 4:
                    self.board_button[i][j].setStyleSheet("background-color : green")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    game = QuoridorGame()
    game.show()
    sys.exit(app.exec_())



'''
for x in range(17):
        for y in range(17):
            print(self.board.status[x][y],end=" ")
        print("\n")
    print("\n\n\n")
''' 