import random

#матриці 100x100
def generate_level():
    level = []
    for _ in range(100):
        row = []
        for _ in range(100):
            cell = random.choices([0, 1, 2, 3, 4], [80, 10, 5, 3, 2])[0]
            row.append(cell)
        level.append(row)
    return level

def generate_playable_level(width, height):
    for _ in range(500):
        level = [[0 for _ in range(width)] for _ in range(height)]

        player_start_x = random.randint(2, width - 3)
        player_start_y = random.randint(2, height - 3)
        level[player_start_y][player_start_x] = 4

        for x in range(width):
            level[0][x] = 1
            level[height - 1][x] = 1
        for y in range(height):
            level[y][0] = 1
            level[y][width - 1] = 1

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                level[player_start_y + dy][player_start_x + dx] = 0
        level[player_start_y][player_start_x] = 4

        num_objects = (width * height) // 7
        for _ in range(num_objects):
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if level[y][x] == 0:
                level[y][x] = random.choices([1, 2, 3], [45, 35, 20])[0]

        if not any(3 in row for row in level):
            continue
        if is_playable(level, player_start_x, player_start_y):
            return level

    level = [[0 for _ in range(width)] for _ in range(height)]
    for x in range(width):
        level[0][x] = 1
        level[height - 1][x] = 1
    for y in range(height):
        level[y][0] = 1
        level[y][width - 1] = 1

    player_start_x = 1
    player_start_y = 1
    level[player_start_y][player_start_x] = 4
    level[1][width - 2] = 3
    level[height - 2][width - 2] = 3
    for x in range(1, width - 1):
        level[1][x] = 0
    level[player_start_y][player_start_x] = 4
    return level

def is_playable(level, start_x, start_y):
    width = len(level[0])
    height = len(level)
    visited = [[False for _ in range(width)] for _ in range(height)]
    enemies = []
    
    def dfs(x, y):
        if x < 0 or x >= width or y < 0 or y >= height:
            return False
        if visited[y][x] or level[y][x] == 1:
            return False
        visited[y][x] = True
        if level[y][x] == 3:
            enemies.append((x, y))
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)
        return True

    dfs(start_x, start_y)
    enemy_count = sum(cell == 3 for row in level for cell in row)
    return len(enemies) == enemy_count and enemy_count > 0



a3= [
    [1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 3, 0, 1, 1, 1, 0, 3, 3, 3, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 3, 0, 3, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 3, 3, 3, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 1,],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0 , 1, 0, 0, 0 , 0, 1,],
    [1, 0, 1, 0, 0, 3, 1, 0, 3, 0, 3, 0, 1, 3, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 3, 3, 3, 0, 1, 1, 1, 0, 1 ,1 ,0 ,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1]
]

#UROVEN 20 Na 15 

a2 = generate_playable_level(20,15)

a1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 2, 0, 0, 2, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 2, 2, 2, 2, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 1, 1, 1, 1, 0, 4, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
