import pygame, sys, random, time

def new_draw():
    screen.fill(white)

    for i in range(1, 21):
        for j in range(10):
            bolck = background[i][j]
            if bolck:
                pygame.draw.rect(screen, blue, (j * 25 + 1, 500 - i * 25 + 1, 23, 23))

    x, y = centre
    for i, j in active:
        i += x
        j += y
        pygame.draw.rect(screen, blue, (j * 25 + 1, 500 - i * 25 + 1, 23, 23))

    pygame.display.update()


def move_LR(n):
    """n=-1代表向左，n=1代表向右"""
    x, y = centre
    y += n
    for i, j in active:
        i += x
        j += y
        if j < 0 or j > 9 or background[i][j]:
            break
    else:
        centre.clear()
        centre.extend([x, y])


def rotate():
    x, y = centre
    l = [(-j, i) for i, j in active]
    for i, j in l:
        i += x
        j += y
        if j < 0 or j > 9 or background[i][j]:
            break
    else:
        active.clear()
        active.extend(l)


def move_down():
    x, y = centre
    x -= 1
    for i, j in active:
        i += x
        j += y
        if background[i][j]:
            break
    else:
        centre.clear()
        centre.extend([x, y])
        return
    # 如果新位置未被占用 通过return结束
    # 如果新位置被占用则继续向下执行
    x, y = centre
    for i, j in active:
        background[x + i][y + j] = 1

    l = []
    for i in range(1, 20):
        if 0 not in background[i]:
            l.append(i)
    # l装 行号，鉴于删去后，部分索引变化，对其降序排列，倒着删除
    l.sort(reverse=True)

    for i in l:
        background.pop(i)
        background.append([0 for j in range(10)])
        # 随删随补

    # score[0] += len(l)
    # pygame.display.set_caption("分数：%d" % (score[0]))

    active.clear()
    active.extend(list(random.choice(all_block)))
    # all_block保存7种形状的信息，手打出来的
    centre.clear()
    centre.extend([20, 4])

    x, y = centre
    for i, j in active:
        i += x
        j += y
        if background[i][j]:
            break
    else:
        return
    alive.append(1)


pygame.init()
screen = pygame.display.set_mode((250, 500))
pygame.display.set_caption("俄罗斯方块1.0")
fclock = pygame.time.Clock()

all_block = (((0, 0), (0, -1), (0, 1), (0, 2)),
             ((0, 0), (0, 1), (-1, 0), (-1, 1)),
             ((0, 0), (0, -1), (-1, 0), (-1, 1)),
             ((0, 0), (0, 1), (-1, -1), (-1, 0)),
             ((0, 0), (0, 1), (1, 0), (0, -1)),
             ((0, 0), (1, 0), (-1, 0), (1, -1)),
             ((0, 0), (1, 0), (-1, 0), (1, 1)))
background = [[0 for i in range(10)] for j in range(24)]
background[0] = [1 for i in range(10)]
active = list(random.choice(all_block))
centre = [20, 4]
# score = [0]

black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255

times = 0
alive = []
press = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_LR(-1)
            elif event.key == pygame.K_RIGHT:
                move_LR(1)
            elif event.key == pygame.K_UP:
                rotate()
            elif event.key == pygame.K_DOWN:
                press = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                press = False
    if press:
        times += 10

    if times >= 50:
        move_down()
        times = 0
    else:
        times += 1

    if alive:
        # pygame.display.set_caption("over分数：%d" % (score[0]))
        time.sleep(3)
        break
    new_draw()
    fclock.tick(100)