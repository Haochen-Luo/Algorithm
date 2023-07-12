问题：8*8的棋盘，knight走L，初始位置位于中心四格之一,计算k步之后仍在棋盘的概率
本质还是BFS/DFS。
另一种思路：
计算k步之后在棋盘的位置/(len(possible_move)**k)
```py
def is_on_chessboard(x,y):
    return 0<=x<8 and 0<=y<8
possible_moves = [
    (1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)
]


def simulation():
    total_runs = 60000
    count = 0
    import random
    for i in range(total_runs):
        start_x = 4
        start_y = 4
        for j in range(4):
            move_index = random.randint(0, len(possible_moves) - 1)
            start_x += possible_moves[move_index][0]
            start_y += possible_moves[move_index][1]
            if not is_on_chessboard(start_x, start_y):
                break
        if is_on_chessboard(start_x, start_y):
            count += 1

    print(count / total_runs)


def dfs(x,y,step,k):
    if not is_on_chessboard(x,y):
        return 0
    if step==k:
        return 1
    p  = 0

    for move in possible_moves:
        dx = move[0]
        dy = move[1]
        p+=1/len(possible_moves)*dfs(x+dx,y+dy,step+1,k)
    return p


def k_step_possibility(k):
    start_x = 4
    start_y = 4
    p = 0
    step = 1
    for move in possible_moves:
        dx = move[0]
        dy = move[1]
        p+=1/len(possible_moves)*dfs(start_x+dx,start_y+dy,step,k)

    print(p)
    return p
# simulation()
k_step_possibility(8)



def k_step_possibility(k):
    start_x = 4
    start_y = 4
    p = 0
    step = 1
    for move in possible_moves:
        dx = move[0]
        dy = move[1]
        p+=1/len(possible_moves)*dfs(start_x+dx,start_y+dy,step,k)

    print(p)
    return p
```
