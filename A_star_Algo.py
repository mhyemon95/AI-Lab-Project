import math
import time
from queue import PriorityQueue

INF = 1000000
FREE = 0
BLOCK = 1
PATH = -1

N = 101

row, column = map(int, input().split())

par = [[(0, 0) for _ in range(N)] for _ in range(N)]
Maze = [[FREE for _ in range(N)] for _ in range(N)]
Manhattan_Distance = [[0 for _ in range(N)] for _ in range(N)]
Diagonal_Distance = [[0 for _ in range(N)] for _ in range(N)]
Euclidean_Distance = [[0 for _ in range(N)] for _ in range(N)]

fx = [0, -1, 0, 1, -1, -1, 1, 1]
fy = [1, 0, -1, 0, 1, -1, -1, 1]

def isValid(currentX, currentY):
    return 0 <= currentX < row and 0 <= currentY < column

def isUnBlocked(row, col):
    return Maze[row][col] == FREE

def Manhattan_Distances(goal):
    for currentX in range(row):
        for currentY in range(column):
            Manhattan_Distance[currentX][currentY] = abs(goal[0] - currentX) + abs(goal[1] - currentY)

def Diagonal_Distances(goal):
    for currentX in range(row):
        for currentY in range(column):
            Diagonal_Distance[currentX][currentY] = max(abs(goal[0] - currentX), abs(goal[1] - currentY))

def Euclidean_Distances(goal):
    for currentX in range(row):
        for currentY in range(column):
            Euclidean_Distance[currentX][currentY] = math.sqrt(((goal[0] - currentX) ** 2) + ((goal[1] - currentY) ** 2))

def AStarSearch(source, goal, d):
    if not isValid(source[0], source[1]):
        print("Source is invalid")
        return

    if not isValid(goal[0], goal[1]):
        print("Goal is invalid")
        return

    if not isUnBlocked(source[0], source[1]) or not isUnBlocked(goal[0], goal[1]):
        print("Source or the Goal is blocked")
        return

    if source[0] == goal[0] and source[1] == goal[1]:
        print("We are already at the destination")
        return

    Distance = [[0 for _ in range(N)] for _ in range(N)]
    if d == 1:
        for x in range(row):
            for y in range(column):
                Distance[x][y] = Manhattan_Distance[x][y]
    elif d == 2:
        for x in range(row):
            for y in range(column):
                Distance[x][y] = Diagonal_Distance[x][y]
    else:
        for x in range(row):
            for y in range(column):
                Distance[x][y] = Euclidean_Distance[x][y]

    cost = [[INF for _ in range(N)] for _ in range(N)]
    dist = [[INF for _ in range(N)] for _ in range(N)]

    pq = PriorityQueue()
    pq.put((0, source))
    cost[source[0]][source[1]] = 0
    while not pq.empty():
        current = pq.get()[1]
        current_x, current_y = current
        for k in range(4):
            nxt_x = current_x + fx[k]
            nxt_y = current_y + fy[k]
            if isValid(nxt_x, nxt_y) and Maze[nxt_x][nxt_y] != BLOCK and cost[current_x][current_y] + Distance[current_x][current_y] + 1 < cost[nxt_x][nxt_y]:
                dist[nxt_x][nxt_y] = dist[current_x][current_y] + 1
                cost[nxt_x][nxt_y] = cost[current_x][current_y] + Distance[current_x][current_y] + 1
                par[nxt_x][nxt_y] = current
                pq.put((cost[nxt_x][nxt_y], (nxt_x, nxt_y)))

        for k in range(4, 8):
            nxt_x = current_x + fx[k]
            nxt_y = current_y + fy[k]
            if isValid(nxt_x, nxt_y) and Maze[nxt_x][nxt_y] != BLOCK and cost[current_x][current_y] + Distance[current_x][current_y] + 1.414 < cost[nxt_x][nxt_y]:
                dist[nxt_x][nxt_y] = dist[current_x][current_y] + 1
                cost[nxt_x][nxt_y] = cost[current_x][current_y] + Distance[current_x][current_y] + 1.414
                par[nxt_x][nxt_y] = current
                pq.put((cost[nxt_x][nxt_y], (nxt_x, nxt_y)))

    if dist[goal[0]][goal[1]] == INF:
        print("Unable to reach at Goal")
        return

    path = []
    cur = goal
    while cur != source:
        path.append(cur)
        cur = par[cur[0]][cur[1]]
    path.append(source)
    print("Path:", path[::-1])

    pathcost = 0
    for i in range(1, len(path)):
        if (path[i][0] - path[i - 1][0]) ** 2 + (path[i][1] - path[i - 1][1]) ** 2 == 1:
            pathcost += 1
        else:
            pathcost += 1.414

    print("Path Cost:", pathcost)

obstacles = int(input())

for _ in range(obstacles):
    x, y = map(int, input().split())
    Maze[x][y] = BLOCK

source = tuple(map(int, input().split()))
goal = tuple(map(int, input().split()))

Manhattan_Distances(goal)
Diagonal_Distances(goal)
Euclidean_Distances(goal)

start_time = time.time()
AStarSearch(source, goal, 1)
AStarSearch(source, goal, 2)
AStarSearch(source, goal, 3)
end_time = time.time()

print("Time Taken: {:.2f} ms".format((end_time - start_time) * 1000))
