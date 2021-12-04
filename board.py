class Board:

    def __init__(self):
        self.direction = 0
        self.status = [[0]*17 for i in range(17)]
        self.status[0][8] = 2
        self.status[16][8] = 3
    
    # 벽 설치!
    def wall_check(self, y, x):
        # 범위 확인
        if (not (y%2 and x%2)) or x<=0 or y<=0 or x>=16 or y>=16:
            return False
        # 놓을 곳이 비어있는지(벽이 이미 설치되어있는지) 확인
        for tmp in [0, -1, 1]:
            if self.status[y + tmp*self.direction][x + tmp*(1 - self.direction)] == 1:
                return False
        # 모든 경로가 막혀있나? bfs로 확인!
        (i1,j1) = self.find_board(2)
        (i2,j2) = self.find_board(3)
        if self.bfs(i1,j1,16) and self.bfs(i2,j2,0):
            return True
        # 이동할 수 있는 경로가 막힙니다!
        return False

    def wall_clicked(self, y, x):
        # 범위 확인
        if (not (y%2 and x%2)) or x<=0 or y<=0 or x>=16 or y>=16:
            return False
        # 놓을 곳이 비어있는지(벽이 이미 설치되어있는지) 확인
        for tmp in [0, -1, 1]:
            if self.status[y + tmp*self.direction][x + tmp*(1 - self.direction)] == 1:
                return False
        for tmp in [0, -1, 1]:
            self.status[y + tmp*self.direction][x + tmp*(1 - self.direction)] = 1
        # 모든 경로가 막혀있나? bfs로 확인!
        (i1,j1) = self.find_board(2)
        (i2,j2) = self.find_board(3)
        if self.bfs(i1,j1,16) and self.bfs(i2,j2,0):
            return True
        for tmp in [0, -1, 1]:
            self.status[y + tmp*self.direction][x + tmp*(1 - self.direction)] = 0
        # 이동할 수 있는 경로가 막힙니다!
        return False

    def bfs(self, sy, sx, e):
        q = [(sy, sx)]
        tmp = [0,0,1,-1]
        chk = [[0]*17 for i in range(17)]
        while len(q) > 0:
            (y,x) = q.pop()
            if y == e: return True
            for i in range(4):
                yy = y + tmp[i]
                xx = x + tmp[3-i]
                if not (yy >= 0 and yy < 17 and xx >= 0 and xx < 17 and self.status[yy][xx] == 0 and chk[yy+tmp[i]][xx+tmp[3-i]] == 0): continue
                if 2 <= self.status[yy+tmp[i]][xx+tmp[3-i]] <= 3 and not (yy+tmp[i] == sy and xx+tmp[3-i] == sx):
                    yyy = yy + tmp[i]*2; xxx = xx + tmp[3-i]*2
                    if not (yyy >= 0 and yyy < 17 and xxx >= 0 and xxx < 17 and self.status[yyy][xxx] == 0): continue
                    yyy += tmp[i]; xxx += tmp[3-i]
                    if (yyy == sy and xxx == sx) or chk[yyy][xxx] == 1: continue
                    chk[yyy][xxx] = 1
                    q.append((yyy,xxx))
                else:
                    chk[yy+tmp[i]][xx+tmp[3-i]] = 1
                    q.append((yy+tmp[i],xx+tmp[3-i]))
            pass
        return False

    def player_clicked(self, y, x):
        if self.status[y][x] == 4:
            return True
        return False

    def whereCanMove(self, turn):
        (y, x) = self.find_board(turn)
        tmp = [0,0,1,-1]
        res = []
        for i in range(4):
            yy = y + tmp[3-i]; xx = x + tmp[i]
            if not (yy >= 0 and yy < 17 and xx >= 0 and xx < 17 and self.status[yy][xx] == 0): continue
            yy += tmp[3-i]; xx += tmp[i]

            if 2 <= self.status[yy][xx] <= 3:
                #상대편의 말이 있다!
                yyy = yy + tmp[3-i]; xxx = xx + tmp[i]
                if not (yyy >= 0 and yyy < 17 and xxx >= 0 and xxx < 17 and self.status[yyy][xxx] == 0): continue
                yyy += tmp[3-i]; xxx += tmp[i]
                if yyy == y and xxx == x: continue
                self.status[yyy][xxx] = 4
                res.append((yyy,xxx))
            else:
                self.status[yy][xx] = 4
                res.append((yy, xx))
        return res

    def find_board(self, tar):
        for i in range(17):
            for j in range(17):
                if self.status[i][j] == tar:
                    return (i,j)

    def set_direction(self, dir): # 가로 : 0, 세로 : 1
        self.direction = dir
        pass
