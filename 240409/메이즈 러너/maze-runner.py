import sys


def check_square(square, edge):
    if square[0] < 0 and square[1] < 0: # 왼쪽 위 초과
        return [0, 0, edge - 1, edge - 1]
    if square[0] < 0: # 위쪽 초과
        square[0] = 0
        square[2] = edge - 1
        return square
    if square[1] < 0: # 왼쪽 초과
        square[1] = 0
        square[3] = edge - 1
        return square
    if square[2] >= n and square[3] >= n: # 오른 아래 초과
        return [n - edge, n - edge, n - 1, n - 1]
    if square[2] >= n: # 아래 초과
        square[0] = n - edge
        square[2] = n - 1
        return square
    if square[3] >= n: # 오른 초과
        square[1] = n - edge
        square[3] = n - 1
        return square
    return square


def move(x, y, target_x, target_y):
    d = [(1, 0), (-1, 0), (0, 1), (0, -1)] # 상하 우선
    dis = abs(x - target_x) + abs(y - target_y)
    for dx, dy in d:
        nx, ny = x + dx, y + dy
        n_dis = abs(nx - target_x) + abs(ny - target_y)
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0 and dis > n_dis:
            return nx, ny
    return -1, -1


def rotate(exit):
    v = 100
    leftup_x, leftup_y, rightdown_x, rightdown_y = 10, 10, 10, 10
    e = 10
    for px, py in party:  # 구역 정하기
        edge = max(abs(px - exit[0]), abs(py - exit[1])) + 1
        square = [max(px, exit[0]) - edge + 1, max(py, exit[1]) - edge + 1, max(px, exit[0]), max(py, exit[1])]
        square = check_square(square, edge)
        temp = edge ** 2
        if temp < v:
            v = temp
            leftup_x, leftup_y, rightdown_x, rightdown_y = square
            e = edge
        if temp == v:  # 같은 경우
            if leftup_x > square[0]:
                v = temp
                leftup_x, leftup_y, rightdown_x, rightdown_y = square
                e = edge
            if leftup_x == square[0]:  # 또 같은 경우
                if leftup_y > square[1]:
                    v = temp
                    leftup_x, leftup_y, rightdown_x, rightdown_y = square
                    e = edge
    # 구역 돌리기
    if party:
        # 벽
        temp = [board[i][leftup_y:rightdown_y + 1] for i in range(leftup_x, rightdown_x + 1)]  # 깊은 복사
        for i in range(e):
            for j in range(e):
                if temp[i][j] > 0:
                    board[leftup_x + j][rightdown_y - i] = temp[i][j] - 1
                else:
                    board[leftup_x + j][rightdown_y - i] = 0
        # 사람
        for i, p in enumerate(party):
            px, py = p
            if leftup_x <= px <= rightdown_x and leftup_y <= py <= rightdown_y:
                party[i] = [leftup_x + py - leftup_y, leftup_y + rightdown_x - px]
        # 출구
        exit[0], exit[1] = leftup_x + exit[1] - leftup_y, leftup_y + rightdown_x - exit[0]


read = sys.stdin.readline
n, m, k = map(int, read().split())
board = [list(map(int, read().split())) for _ in range(n)]
party = [list(map(lambda x: int(x) - 1, read().split())) for _ in range(m)]
exit = list(map(lambda x: int(x) - 1, read().split()))
ans = 0
while k > 0 and party:
    for _ in range(len(party)):  # 각 참가자 이동
        temp_x, temp_y = party.pop(0)
        x, y = move(temp_x, temp_y, exit[0], exit[1])
        if x != -1:
            ans += 1
            if x != exit[0] or y != exit[1]:  # 탈출안하면 다시 추가
                party.append([x, y])
        else: # 그 자리 그대로인 경우
            party.append([temp_x, temp_y])

    rotate(exit)
    k -= 1
exit[0] += 1
exit[1] += 1
print(ans)
print(*exit)