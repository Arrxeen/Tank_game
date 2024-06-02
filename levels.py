import random

#матриці 100x100
def generate_level():
    level = []
    for i in range(100):
        row = []
        for j in range(100):
            cell = random.choices([0, 1, 2, 3, 4], [80, 10, 5, 3, 2])[0]
            row.append(cell)
        level.append(row)
    return level

def generate_playable_level(width, height):
    # Ініціалія
    level = [[0 for _ in range(width)] for _ in range(height)]
    
    # Встановлюємо танк
    player_start_x = random.randint(0, width - 1)
    player_start_y = random.randint(0, height - 1)
    level[player_start_y][player_start_x] = 4  # 4 - танк

    # Розміщення
    for x in range(width):
        level[0][x] = 1
        level[height - 1][x] = 1
    for y in range(height):
        level[y][0] = 1
        level[y][width - 1] = 1
    
    #випадкові об'єкти на карту
    num_objects = (width * height) // 2  # менше цифра більше наповненя
    for _ in range(num_objects):
        x, y = random.randint(1, width - 2), random.randint(1, height - 2)
        if level[y][x] == 0:
            level[y][x] = random.choices([1, 2, 3], [50, 30, 20])[0]

    if not is_playable(level, player_start_x, player_start_y):
        return generate_playable_level(width, height)

    return level

def is_playable(level, start_x, start_y):
    width = len(level[0])
    height = len(level)
    visited = [[False for _ in range(width)] for _ in range(height)]
    
    def dfs(x, y):
        if x < 0 or x >= width or y < 0 or y >= height:
            return False
        if visited[y][x] or level[y][x] == 1:
            return False
        visited[y][x] = True
        if level[y][x] == 3:
            return True
        return dfs(x + 1, y) or dfs(x - 1, y) or dfs(x, y + 1) or dfs(x, y - 1)

    return dfs(start_x, start_y)

for row in level:
    print(' '.join(map(str, row)))


a3= [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 3, 0, 1, 1, 1, 0, 2, 2, 2, 0, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 3, 0, 3, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 2, 2, 2, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 4, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 1,],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0 , 1, 0, 0, 0 , 0, 1,],
    [1, 0, 1, 0, 0, 3, 1, 0, 3, 0, 3, 0, 1, 3, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 2, 2, 2, 0, 1, 1, 1, 0, 1 ,1 ,0 ,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 ,1]
]

#UROVEN 20 Na 15 

a2 = generate_playable_level(20,15)

a1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 1, 2, 0, 0, 2, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 2, 2, 2, 2, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 1, 1, 1, 1, 0, 4, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
