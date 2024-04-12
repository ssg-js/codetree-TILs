import sys
from collections import deque


class Person:
    def __init__(self, target_x, target_y):
        self.on_board = False
        self.arrived = False
        self.target = (target_x, target_y)
        self.now = (-1, -1)

    def set_camp(self, arr): # 처음 들어올 때 캠프 배정
        d = [(-1, 0), (0, -1), (0, 1), (0, 1)]
        width = len(arr)
        visited = [[False] * width for _ in range(width)]
        queue = deque([self.target])
        visited[self.target[0]][self.target[1]] = True
        while queue:
            x, y = queue.popleft()
            for dx, dy in d:
                nx, ny = x+dx, y+dy
                if 0 <= nx < width and 0 <= ny < width and not visited[nx][ny]:
                    if arr[nx][ny] == 0:
                        queue.append((nx, ny))
                        visited[nx][ny] = True
                    elif arr[nx][ny] == 1: # 캠프 도착
                        self.on_board = True
                        self.now = (nx, ny)
                        return nx, ny

    def move(self, arr): # on_board 후 이동, 편의점 도착 시 True, 아니면 False 반환
        d = [(-1, 0), (0, -1), (0, 1), (0, 1)]
        width = len(arr)
        visited = [[False] * width for _ in range(width)]
        queue = deque([])
        visited[self.now[0]][self.now[1]] = True
        for dx, dy in d: # 처음 사방
            nx, ny = self.now[0] + dx, self.now[1] + dy
            if 0 <= nx < width and 0 <= ny < width:
                if nx == self.target[0] and ny == self.target[1]: # 도착 처리
                    self.arrived = True
                    self.now = (nx, ny)
                    return True
                elif arr[nx][ny] == 0:
                    queue.append((nx, ny, (nx, ny)))
                    visited[nx][ny] = True
        while queue:
            x, y, np = queue.popleft()
            for dx, dy in d:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < width and not visited[nx][ny]:
                    if nx == self.target[0] and ny == self.target[1]:  # 최단 거리 방향 이동
                        self.now = (np[0], np[1])
                        return False
                    elif arr[nx][ny] == 0:
                        queue.append((nx, ny, np))
                        visited[nx][ny] = True


def arrange():
    for x, y in to_arrange:
        board[x][y] = 2


read = sys.stdin.readline
n, m = map(int, read().split())
board = [list(map(int, read().split())) for _ in range(n)] # 0: 길, 1: 베이스캠프, 2: 벽
people = []
for _ in range(m):
    a, b = map(lambda x: int(x)-1, read().split())
    person = Person(a, b)
    people.append(person)
cnt = m
t = 1
while cnt > 0:
    to_arrange = []
    # 1
    for p in people:
        if p.on_board and not p.arrived: # 격자에 올라온 애들중에 도착 안한 애들
            if p.move(board): # 도착한 애들
                to_arrange.append(p.now)
                cnt -= 1
                if cnt == 0:
                    print(t)
    arrange()
    to_arrange = []
    # 3
    if t <= m:
        p = people[t-1]
        to_arrange.append(p.set_camp(board))
    arrange()
    t += 1