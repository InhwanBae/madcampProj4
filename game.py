# 장애물 회피 게임 즉, 자율주행차:-D 게임을 구현합니다.
import numpy as np
import random
import pygame
import os

BLOCK_SIZE = 20
APPLE_COUNT = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 4방위 정의
#    1
# 3  0  4
#    2
dx = [0, 0, 0, -1, 1]
dy = [0, -1, 1, 0, 0]

def get_image(file_name):
    return pygame.image.load('resource'+os.sep+file_name+'.png')

def get_color():
    return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

bg = get_image('background')
eyes = []
for i in range(8):
    eyes.append(get_image('snakeEye'+str(i+1)))
foods = []
for i in range(16):
    foods.append(get_image('food'+str(i+1).zfill(2)))

small_foods = []
for i in range(16):
    small_foods.append(get_image('smallfood'+str(i+1).zfill(2)))

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    # x == y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # x != y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    # x < y
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y
    # x <=y
    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    # x > y
    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    # x>= y
    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y


class Snake:
    def __init__(self, x=-1, y=-1, pos=Pos(-1, -1)):
        if pos != Pos(-1,-1):
            self.pos = Pos
        self.pos = Pos(x, y)
        self.length = 3
        self.trunk = []
        self.head = self.pos

    def append_head(self, pos):
        self.trunk.append(pos)
        self.head = pos

    def maybe_remove_tail(self):
        if self.length < len(self):
            del self.trunk[0]

    def is_self_crash(self):
        for t in self.trunk[:-1]:
            if t == self.head:
                return True
        return False

    def is_crash_wall(self, width, height):
        if not (0 <= self.head.x < width and 0 <= self.head.y < height):
            return True

    def is_crash(self, pos):
        for t in self.trunk:
            if t == pos:
                return True
        return False

    def __eq__(self, other):
        return self.head == other.head

    def __len__(self):
        return len(self.trunk)


class Apple:
    def __init__(self, x=-1, y=-1, pos=Pos(-1,-1)):
        if pos != Pos(-1,-1):
            self.pos = pos
        else:
            self.pos = Pos(x, y)
        self.color = (get_color())
        self.is_big = random.randint(0,1)
        if self.is_big:
            self.shape = foods[random.randint(0, 15)]
        else:
            self.shape = small_foods[random.randint(0, 15)]

        # x == y
        def __eq__(self, other):
            return self.pos == other.pos

        # x != y
        def __ne__(self, other):
            return self.pos != other.pos

        # x < y
        def __lt__(self, other):
            return self.pos < other.pos

        # x <=y
        def __le__(self, other):
            return self.pos <= other.pos

        # x > y
        def __gt__(self, other):
            return self.pos > other.pos

        # x>= y
        def __ge__(self, other):
            return self.pos >= other.pos


class Game:
    def __init__(self, screen_width, screen_height, model_width, model_height, show_game=True,
                 fancy_graphic=False, self_crash=False):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.display_width = screen_width * BLOCK_SIZE
        self.display_height = screen_height * BLOCK_SIZE
        self.fancy_graphic = fancy_graphic
        self.self_crash = self_crash

        self.model_width = model_width
        self.model_height = model_height

        self.game_over = False

        # 사과 정의
        self.apple_list = []

        # 사용자 지렁이 정의
        self.lead_x = 0
        self.lead_y = 0
        self.lead_x_change = 0
        self.lead_y_change = 0

        self.total_reward = 0.
        self.current_reward = 0.
        self.total_game = 0
        self.show_game = show_game

        # 보여주기 위한 설정
        if show_game:
            self._prepare_display()

    def get_random_pos(self):
        return Pos(round(random.randrange(0, self.display_width - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        round(random.randrange(0, self.display_height - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE)

    # 봇들의 움직임 제어
    def get_bot_action(self, snake, _apple_list, _enemyList):
        # 4방위 정의
        #    1
        # 3  0  4
        #    2

        xhead = snake.head.x + 0
        yhead = snake.head.y + 0

        xpos = [xhead - BLOCK_SIZE * 3, xhead - BLOCK_SIZE * 2, xhead - BLOCK_SIZE, xhead,
                xhead + BLOCK_SIZE, xhead + BLOCK_SIZE * 2, xhead + BLOCK_SIZE * 3]
        ypos = [yhead - BLOCK_SIZE * 3, yhead - BLOCK_SIZE * 2, yhead - BLOCK_SIZE, yhead,
                yhead + BLOCK_SIZE, yhead + BLOCK_SIZE * 2, yhead + BLOCK_SIZE * 3]
        xapos = [xhead - BLOCK_SIZE * 5, xhead - BLOCK_SIZE * 4, xhead - BLOCK_SIZE * 3, xhead - BLOCK_SIZE * 2,
                 xhead - BLOCK_SIZE, xhead, xhead + BLOCK_SIZE, xhead + BLOCK_SIZE * 2, xhead + BLOCK_SIZE * 3,
                 xhead + BLOCK_SIZE * 4, xhead + BLOCK_SIZE * 5]
        yapos = [yhead - BLOCK_SIZE * 5, yhead - BLOCK_SIZE * 4, yhead - BLOCK_SIZE * 3, yhead - BLOCK_SIZE * 2,
                 yhead - BLOCK_SIZE, yhead, yhead + BLOCK_SIZE, yhead + BLOCK_SIZE * 2, yhead + BLOCK_SIZE * 3,
                 yhead + BLOCK_SIZE * 4, yhead + BLOCK_SIZE * 5]
        xabpos = [xhead - BLOCK_SIZE, xhead, xhead + BLOCK_SIZE]
        yabpos = [yhead - BLOCK_SIZE, yhead, yhead + BLOCK_SIZE]

        snake_list = []
        apple_list = []
        enemyList = []

        for i in snake.trunk:
            if xhead - BLOCK_SIZE * 5 <= i.x <= xhead + BLOCK_SIZE * 5 and yhead - BLOCK_SIZE * 5 <= i.y <= yhead + BLOCK_SIZE * 5:
                snake_list.append(i)
        for j in _apple_list:
            if xhead - BLOCK_SIZE * 5 <= j.pos.x <= xhead + BLOCK_SIZE * 5 and yhead - BLOCK_SIZE * 5 <= j.pos.y <= yhead + BLOCK_SIZE * 5:
                apple_list.append(j)

        for enemy in _enemyList:
            for pos in enemy.trunk:
                if xhead - BLOCK_SIZE * 5 <= pos.x <= xhead + BLOCK_SIZE * 5 and yhead - BLOCK_SIZE * 5 <= pos.y <= yhead + BLOCK_SIZE * 5:
                    enemyList.append(pos)

        # 숫자 같지 않도록 0~1의 난수로 방향 랜덤 가중치
        up = random.random()
        down = random.random()
        left = random.random()
        right = random.random()

        for i in xapos:
            for j in yapos:
                for apple in apple_list:
                    if Pos(i, j) == apple.pos:
                        if Pos(xhead, yhead) <= apple.pos:
                            right += 20
                            down += 20
                        if xhead <= apple.pos.x and yhead >= apple.pos.y:
                            right += 20
                            up += 20
                        if xhead >= apple.pos.x and yhead <= apple.pos.y:
                            left += 20
                            down += 20
                        if Pos(xhead, yhead) >= apple.pos:
                            left += 20
                            up += 20

        for i in xabpos:
            for j in yabpos:
                for apple in apple_list:
                    if Pos(i,j) == apple.pos:
                        if Pos(xhead, yhead) <= apple.pos:
                            right += 200
                            down += 200
                        if xhead <= apple.pos.x and yhead >= apple.pos.y:
                            right += 200
                            up += 200
                        if xhead >= apple.pos.x and yhead <= apple.pos.y:
                            left += 200
                            down += 200
                        if Pos(xhead, yhead) >= apple.pos:
                            left += 200
                            up += 200

        for i in xpos:
            for j in ypos:
                for apple in apple_list:
                    if Pos(i,j) == apple.pos:
                        if Pos(xhead, yhead) <= apple.pos:
                            right += 80
                            down += 80
                        if xhead <= apple.pos.x and yhead >= apple.pos.y:
                            right += 80
                            up += 80
                        if xhead >= apple.pos.x and yhead <= apple.pos.y:
                            left += 80
                            down += 80
                        if Pos(xhead, yhead) >= apple.pos:
                            left += 80
                            up += 80

                for enemy in enemyList:
                    if Pos(i, j) == enemy:
                        if xhead < enemy.x and yhead < enemy.y:
                            right -= 600 / abs(enemy.x - xhead)
                            down -= 600 / abs(enemy.y - yhead)
                        if xhead < enemy.x and yhead > enemy.y:
                            right -= 600 / abs(enemy.x - xhead)
                            up -= 600 / abs(enemy.y - yhead)
                        if xhead > enemy.x and yhead < enemy.y:
                            left -= 600 / abs(enemy.x - xhead)
                            down -= 600 / abs(enemy.y - yhead)
                        if xhead > enemy.x and yhead > enemy.y:
                            left -= 600 / abs(enemy.x - xhead)
                            up -= 600 / abs(enemy.y - yhead)

                for body in snake_list:
                    if Pos(i, j) == body:
                        if xhead <= body.x and yhead <= body.y:
                            right -= 100 / (abs(body.x - xhead) + 20)
                            down -= 100 / (abs(body.y - yhead) + 20)
                        if xhead <= body.x and yhead >= body.y:
                            right -= 100 / (abs(body.x - xhead) + 20)
                            up -= 100 / (abs(body.y - yhead) + 20)
                        if xhead >= body.x and yhead <= body.y:
                            left -= 100 / (abs(body.x - xhead) + 20)
                            down -= 100 / (abs(body.y - yhead) + 20)
                        if xhead >= body.x and yhead >= body.y:
                            left -= 100 / (abs(body.x - xhead) + 20)
                            up -= 100 / (abs(body.y - yhead) + 20)

        if Pos(xhead, yhead - BLOCK_SIZE) in snake_list:
            up -= 10000
        if Pos(xhead, yhead + BLOCK_SIZE) in snake_list:
            down -= 10000
        if Pos(xhead - BLOCK_SIZE, yhead) in snake_list:
            left -= 10000
        if Pos(xhead + BLOCK_SIZE, yhead) in snake_list:
            right -= 10000

        if Apple(xhead, yhead - BLOCK_SIZE) in apple_list:
            up += 2000
        if Apple(xhead, yhead + BLOCK_SIZE) in apple_list:
            down += 2000
        if Apple(xhead - BLOCK_SIZE, yhead) in apple_list:
            left += 2000
        if Apple(xhead + BLOCK_SIZE, yhead) in apple_list:
            right += 2000

        if yhead - BLOCK_SIZE < 0:
            up -= 1000
        if yhead + BLOCK_SIZE >= self.display_height:
            down -= 1000
        if xhead - BLOCK_SIZE < self.display_width:
            left -= 1000
        if xhead + BLOCK_SIZE >= self.display_width:
            right -= 1000

        # print("up: " + str(up) + ", down: " + str(down) + ", left: " + str(left) + ", right: " + str(right))
        if up > down and up > left and up > right:
            return 1
        elif down > up and down > left and down > right:
            return 2
        elif left > up and left > down and left > right:
            return 3
        elif right > up and right > down and right > left:
            return 4

        direction = round(random.randrange(0, 5) / 4) * 4 + 1
        return direction

    def _prepare_display(self):
        # TODO: 수정 예정

        pygame.init()
        self.font = pygame.font.SysFont('Ubuntu', 20, True)
        self.fps = 15
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("SLITHER.IO")

        self.img = get_image("snakeHead")
        self.clock = pygame.time.Clock()

    def _get_state(self):
        # TODO: 값 세부 수정 예정 (사과 0, 바닥 0.25, 자기자신 0.5, 다른 지렁이 0.75, 벽 1)
        state = np.zeros((self.screen_width, self.screen_height))
        state.fill(0.25)

        # 자기 자신 1로 표현
        for points in self.snakes[0].trunk:
            # 맵 밖으로 나가서 죽은 뱀들 처리
            if 0 <= round(points.x / BLOCK_SIZE) < self.screen_height and \
                    0 <= round(points.y / BLOCK_SIZE) < self.screen_width:
                state[round(points.x / BLOCK_SIZE)][round(points.y / BLOCK_SIZE)] = 0.5

        # 다른 지렁이 0.25 로 표현
        for snake in self.snakes[1:]:
            for points in snake.trunk:
                # 맵 밖으로 나가서 죽은 뱀들 처리
                if 0 <= round(points.x / BLOCK_SIZE) < self.screen_height and \
                        0 <= round(points.y / BLOCK_SIZE) < self.screen_width:
                    state[round(points.x / BLOCK_SIZE)][round(points.y / BLOCK_SIZE)] = 0.75

        # 사과 0.75로 표현
        for apple in self.apple_list:
            points = apple.pos
            # 맵 밖 사과 처리
            if 0 <= round(points.x / BLOCK_SIZE) < self.screen_height and \
                    0 <= round(points.y / BLOCK_SIZE) < self.screen_width:
                state[round(points.x / BLOCK_SIZE)][round(points.y / BLOCK_SIZE)] = 0

        # 벽 0.5로 표현


        # 머리 주변의 값 보내주기
        current_state = np.zeros((self.model_width, self.model_height))
        current_state.fill(1)

        xhead = round(self.snakes[0].head.x / BLOCK_SIZE)
        yhead = round(self.snakes[0].head.y / BLOCK_SIZE)

        #print([xhead, yhead])

        xmiddle = round(self.model_width / 2 + 0.1)
        ymiddle = round(self.model_height / 2 + 0.1)

        #print([xmiddle, ymiddle])

        for i in range(xhead - (xmiddle - 1), xhead + xmiddle):
            for j in range(yhead - (ymiddle - 1), yhead + ymiddle):
                if 0 <= i < self.screen_width and 0 <= j < self.screen_width:
                    current_state[i - (xhead - (xmiddle - 1))][j - (yhead - (ymiddle - 1))] = state[i][j]

        return current_state

    # 스네이크 표현해 주는 부분
    def draw_snake(self, snake, slot):
        if self.fancy_graphic:
            # 예쁘게 그려주기
            body = get_image('snakeBody'+str(slot))
            shader = get_image("snakeShader40")

            # 1/2 지점 생성
            body_list = []
            for i in range(len(snake)):
                if i < len(snake) - 1:
                    body_list.append(Pos((snake.trunk[i].x + snake.trunk[i + 1].x) / 2,
                                         (snake.trunk[i].y + snake.trunk[i + 1].y) / 2))

            snake_body = []
            if len(snake) > 0:
                snake_body.append(snake.trunk[0])
            for i in range(len(body_list)):
                snake_body.append(body_list[i])

                if i < len(body_list) - 1:
                    snake_body.append(Pos((body_list[i].x + body_list[i + 1].x) / 2,
                                          (body_list[i].y + body_list[i + 1].y) / 2))
            snake_body.append(snake.head)

            body_list2 = []
            for i in range(len(snake_body)):
                if i < len(snake_body) - 1:
                    body_list2.append(Pos((snake_body[i].x + snake_body[i+1].x) / 2,
                                          (snake_body[i].y + snake_body[i+1].y) / 2))
            snake_body2 = []
            snake_body2.append(snake_body[0])
            for i in range(len(body_list2)):
                snake_body2.append(body_list2[i])

                if i < len(body_list2) - 1:
                    snake_body2.append(Pos((body_list2[i].x + body_list2[i+1].x) / 2,
                                           (body_list2[i].y + body_list2[i+1].y) / 2))
            snake_body2.append(snake_body[len(snake_body) - 1])

            for i in range(len(snake_body2)):
                if not i % 2 == 1:
                    self.gameDisplay.blit(shader, (snake_body2[i].x - 10, snake_body2[i].y - 8))

            for pos in snake_body2:
                self.gameDisplay.blit(body, (pos.x - 2, pos.y - 2))

            if len(snake) > 1:
                if snake_body2[len(snake_body2) - 1].x == snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y < snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[0], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x > snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y < snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[1], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x > snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y == snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[2], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x > snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y > snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[3], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x == snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y > snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[4], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x < snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y > snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[5], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x < snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y == snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[6], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[len(snake_body2) - 1].x < snake_body2[len(snake_body2) - 3].x and \
                        snake_body2[len(snake_body2) - 1].y < snake_body2[len(snake_body2) - 3].y:
                    self.gameDisplay.blit(eyes[7], (snake.head.x - 2, snake.head.y - 2))
            else:
                self.gameDisplay.blit(eyes[0], (snake.head.x - 2, snake.head.y - 2))

        else:
            color = WHITE
            if slot != 1:
                color = BLUE
            for pos in snake.trunk:
                pygame.draw.rect(self.gameDisplay, color, [pos.x, pos.y, BLOCK_SIZE, BLOCK_SIZE])
            self.gameDisplay.blit(self.img, (snake.head.x, snake.head.y))

    def _draw_text(self, message, pos, color=WHITE):
        self.gameDisplay.blit(self.font.render(message, True, color), pos)

    def _draw_score(self):
        self._draw_text("SCOREBOARD", (self.screen_width / 2,self.screen_height / 2))
        score_list = []
        score_list.append([len(self.snakes[0]), 'ME'])

        for i in range(1,8):
            score_list.append([len(self.snakes[i]), 'bot'+str(i+1)])

        def getKey(item):
            return item[0]



        print(score_list)
        i = 1
        for score, name in reversed(sorted(score_list, key=getKey)):
            self._draw_text(str(i) + ". " + str(name) + ": " + str(score),
                            (self.screen_width / 2,self.screen_height / 2 + i * BLOCK_SIZE))
            i+=1

    def _draw_screen(self):

        # 게임 화면에 구현
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.gameDisplay.fill(BLACK)
        if self.fancy_graphic:
            self.gameDisplay.blit(bg, (0, 0))

        for apple in self.apple_list:
            if self.fancy_graphic:
                adjust = 2
                if apple.is_big:
                    adjust = 7

                self.gameDisplay.blit(apple.shape, (int(apple.pos.x -adjust), int(apple.pos.y - adjust)))
                # pygame.draw.circle(self.gameDisplay, apple.color, (int(apple.pos.x), int(apple.pos.y)), 7)
            else:
                pygame.draw.rect(self.gameDisplay, (255, 0, 0), [apple.pos.x, apple.pos.y, BLOCK_SIZE, BLOCK_SIZE])


        for i in range(8):
            self.draw_snake(self.snakes[i], i + 1)

        self._draw_score()

        # 화면 업데이트
        pygame.display.update()

        # 다음 틱까지 대기
        self.clock.tick(self.fps)


    def reset(self):
        # 게임 판 초기화
        self.game_over = False

        # 지렁이 정의
        self.snakes = []
        for i in range(8):
            self.snakes.append(Snake())

        self.lead_x_change = 0
        self.lead_y_change = 0

        self.apple_list = []
        # 지렁이들의 위치 생성
        snake_idx = 0
        for snake in self.snakes:
            while len(snake) == 0:
                rand_pos = self.get_random_pos()
                is_snake_exist = False
                for other in self.snakes:
                    for pos in other.trunk:
                        if rand_pos == pos:
                            is_snake_exist = True
                if not is_snake_exist:
                    snake.append_head(rand_pos)
                if snake_idx == 0:
                    self.lead_x = rand_pos.x
                    self.lead_y = rand_pos.y
                snake_idx += 1


        # 사과 생성
        while len(self.apple_list) <= APPLE_COUNT:
            gen_apple = Apple(pos=self.get_random_pos())

            # 같은 위치에 사과가 생기지 않도록 함
            is_apple_exist = False
            for apple in self.apple_list:
                if gen_apple == apple:
                    is_apple_exist = True
            # 뱀 위에 사과가 생기지 않도록 함
            for snake in self.snakes:
                for pos in snake.trunk:
                    if gen_apple.pos == pos:
                        is_apple_exist = True

            if not is_apple_exist:
                self.apple_list.append(gen_apple)

        self.current_reward = 0
        self.total_game += 1
        self._update_board()
        return self._get_state()

    def _update_snake(self, move):
        # 4방위 정의
        #    1
        # 4  0  2
        #    3
        print(move, end="")

        # 사용자 입력 처리문
        if move == 4:
            self.lead_x_change = -BLOCK_SIZE
            self.lead_y_change = 0
        elif move == 2:
            self.lead_x_change = BLOCK_SIZE
            self.lead_y_change = 0
        elif move == 1:
            self.lead_y_change = -BLOCK_SIZE
            self.lead_x_change = 0
        elif move == 3:
            self.lead_y_change = BLOCK_SIZE
            self.lead_x_change = 0

        # 머리의 위치 추가
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change

        # 머리 이동,리스트 추가 및 맨 마지막 꼬리 제거
        # print(self.lead_x, self.lead_y)
        self.snakes[0].append_head(Pos(self.lead_x, self.lead_y))
        self.snakes[0].maybe_remove_tail()

    # 봇과 사과를 업데이트 한다.
    def _update_board(self):
        # TODO: 수정 예정
        reward = 0
        remove_apple = []
        # 먹은 사과 제거
        for apple in self.apple_list:
            i = 0
            for snake in self.snakes:
                if snake.head == apple.pos:
                    snake.length += 1
                    if i == 0:
                        reward += 1
                    if apple not in remove_apple:
                        remove_apple.append(apple)
                i += 1

        for apple in remove_apple:
            self.apple_list.remove(apple)

        total_snake_length = 0
        for snake in self.snakes:
            total_snake_length += len(snake)

        # 사과 생성
        while len(self.apple_list) <= APPLE_COUNT and len(self.apple_list) + total_snake_length \
                < self.screen_width * self.screen_height * 0.9:
            gen_apple = Apple(pos=self.get_random_pos())

            # 같은 위치에 사과가 생기지 않도록 함
            is_apple_exist = False
            for apple in self.apple_list:
                if gen_apple == apple:
                    is_apple_exist = True

            # 뱀 위에 사과가 생기지 않도록 함
            for snake in self.snakes:
                for pos in snake.trunk:
                    if gen_apple.pos == pos:
                        is_apple_exist = True

            if not is_apple_exist:
                self.apple_list.append(gen_apple)

        for snake in self.snakes[1:]:
            tmp = self.snakes[:]
            tmp.remove(snake)
            status = self.get_bot_action(snake, self.apple_list, tmp)
            snake.append_head(Pos(snake.head.x + dx[status] * BLOCK_SIZE, snake.head.y + dy[status] * BLOCK_SIZE))
            snake.maybe_remove_tail()

        # 자기 자신 게임이 끝났는지 체크
        self._check_game_over()

        # 뱀들 체크
        snake_idx = 0
        is_snake_dead = []
        is_snake_crash_wall = []
        for i in range(8):
            is_snake_dead.append(False)
            is_snake_crash_wall.append(False)
        for snake in self.snakes[1:]:
            snake_idx += 1
            is_snake_dead[snake_idx] = False
            is_snake_crash_wall[snake_idx] = False
            if snake.is_self_crash():
                is_snake_dead[snake_idx] = self.self_crash
            if snake.is_crash_wall(self.display_width, self.display_height):
                is_snake_dead[snake_idx] = True
                is_snake_crash_wall[snake_idx] = True
            for other_snake in self.snakes:
                if other_snake == snake:
                    continue
                if other_snake.is_crash(snake.head):
                    is_snake_dead[snake_idx] = True

        for i in range(1, 8):
            if is_snake_dead[i] and not is_snake_crash_wall[i]:
                for pos in self.snakes[i].trunk:
                    if random.randint(0, 3) >= 2:
                        apple = Apple(pos.x, pos.y)
                        if apple not in self.apple_list:
                            self.apple_list.append(apple)
            if is_snake_dead[i]:
                self.snakes[i] = Snake()

        for snake in self.snakes:
            while len(snake) == 0:
                rand_pos = self.get_random_pos()
                is_snake_exist = False
                for other_snake in self.snakes:
                    for pos in other_snake.trunk:
                        if rand_pos == pos:
                            is_snake_exist = True
                if not is_snake_exist:
                    snake.append_head(rand_pos)

        return reward

    def _check_game_over(self):
        # 플레이어의 머리와 타 플레이어의 몸통이 부딛힐 경우 게임 종료
        if self.snakes[0].is_self_crash():
            self.game_over = self.self_crash
        for snake in self.snakes[1:]:
            if snake.is_crash(self.snakes[0].head):
                self.game_over = True
        if self.lead_x >= self.display_width or self.lead_x < 0 or self.lead_y >= self.display_height or self.lead_y < 0:
            self.game_over = True

        if self.game_over:
            self.total_reward += self.current_reward



    def step(self, action):
        # action: 0: 상, 1: 오, 2: 하, 3: 왼
        # 게임 진행
        self._update_snake(action + 1)

        # 뱀과 사과를 업데이트 합니다.
        escape_reward = self._update_board()

        # 움직임이 적을 경우에도 보상을 줘서 안정적으로 이동하는 것 처럼 보이게 만듭니다.
        #stable_reward = 1. / self.screen_height if action == 1 else 0
        stable_reward = 0

        if self.game_over:
            # 장애물에 충돌한 경우 -4점을 보상으로 줍니다.
            reward = -4
        else:
            reward = escape_reward + stable_reward
            self.current_reward += reward

        if self.show_game:
            self._draw_screen()

        return self._get_state(), reward, self.game_over
