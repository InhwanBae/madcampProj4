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

# Define cardinal points
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

        # Apple definition
        self.apple_list = []

        # User worm definition
        self.lead_x = 0
        self.lead_y = 0
        self.lead_x_change = 0
        self.lead_y_change = 0

        self.total_reward = 0.
        self.current_reward = 0.
        self.total_game = 0
        self.show_game = show_game

        # Settings for showing
        if show_game:
            self._prepare_display()

    def get_random_pos(self):
        return Pos(round(random.randrange(0, self.display_width - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
        round(random.randrange(0, self.display_height - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE)

    # Controlling movement of bots
    def get_bot_action(self, snake, _apple_list, _enemyList):
        # Define cardinal points
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

        # Random weights with a random number between 0 and 1
        up = random.random()
        down = random.random()
        left = random.random()
        right = random.random()

        # AI path calculation using weights
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
        # TODO: Modify values (apple 0, bg 0.25, me 0.5, others 0.75, wall 1)
        state = np.zeros((self.screen_width, self.screen_height))

        # bg
        state.fill(0.25)

        # me
        for points in self.snakes[0].trunk:
            # Exception handling
            if 0 <= round(points.x / BLOCK_SIZE) < self.screen_height and \
                    0 <= round(points.y / BLOCK_SIZE) < self.screen_width:
                state[round(points.x / BLOCK_SIZE)][round(points.y / BLOCK_SIZE)] = 0.5

        # others
        for snake in self.snakes[1:]:
            for points in snake.trunk:
                # Exception handling
                if 0 <= round(points.x / BLOCK_SIZE) < self.screen_height and \
                        0 <= round(points.y / BLOCK_SIZE) < self.screen_width:
                    state[round(points.x / BLOCK_SIZE)][round(points.y / BLOCK_SIZE)] = 0.75

        # apples
        for apple in self.apple_list:
            points = apple.pos
            # Exception handling
            if 0 <= round(points.x / BLOCK_SIZE) < self.screen_height and \
                    0 <= round(points.y / BLOCK_SIZE) < self.screen_width:
                state[round(points.x / BLOCK_SIZE)][round(points.y / BLOCK_SIZE)] = 0

        # wall

        # Send values around the snakehead
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

    # Draw snake on the scene
    def draw_snake(self, snake, slot):
        if self.fancy_graphic:
            # Show fancy graphic
            body = get_image('snakeBody'+str(slot))
            shader = get_image("snakeShader40")

            # Generate 1/2 points
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

            # Generate 1/4 points
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

            # Draw snakes
            for i in range(len(snake_body2)):
                if not i % 2 == 1:
                    self.gameDisplay.blit(shader, (snake_body2[i].x - 10, snake_body2[i].y - 8))

            for pos in snake_body2:
                self.gameDisplay.blit(body, (pos.x - 2, pos.y - 2))

            if len(snake) > 1:
                if snake_body2[-1].x == snake_body2[-3].x and snake_body2[-1].y < snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[0], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x > snake_body2[-3].x and snake_body2[-1].y < snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[1], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x > snake_body2[-3].x and snake_body2[-1].y == snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[2], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x > snake_body2[-3].x and snake_body2[-1].y > snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[3], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x == snake_body2[-3].x and snake_body2[-1].y > snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[4], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x < snake_body2[-3].x and snake_body2[-1].y > snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[5], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x < snake_body2[-3].x and snake_body2[-1].y == snake_body2[-3].y:
                    self.gameDisplay.blit(eyes[6], (snake.head.x - 2, snake.head.y - 2))

                if snake_body2[-1].x < snake_body2[-3].x and snake_body2[-1].y < snake_body2[-3].y:
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
            i += 1

    def _draw_screen(self):

        # Implemented on the game screen
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

        # Scene update
        pygame.display.update()

        # Wait till next tick
        self.clock.tick(self.fps)


    def reset(self):
        # Initialize the game board
        self.game_over = False

        # Define snakes
        self.snakes = []
        for i in range(8):
            self.snakes.append(Snake())

        self.lead_x_change = 0
        self.lead_y_change = 0

        self.apple_list = []
        # Create the location of snakes
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


        # Generate apple
        while len(self.apple_list) <= APPLE_COUNT:
            gen_apple = Apple(pos=self.get_random_pos())

            # Avoid apples in the same location
            is_apple_exist = False
            for apple in self.apple_list:
                if gen_apple == apple:
                    is_apple_exist = True
            # Avoiding apples on snakes
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
        # Define cardinal points
        #    1
        # 4  0  2
        #    3
        print(move, end="")

        # User input processing statement
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

        # Add head position
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change

        # Move head, add list and remove last tail
        # print(self.lead_x, self.lead_y)
        self.snakes[0].append_head(Pos(self.lead_x, self.lead_y))
        self.snakes[0].maybe_remove_tail()

    # Update bots and apples
    def _update_board(self):
        # TODO: To be fixed
        reward = 0
        remove_apple = []
        # Remove eaten apples
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

        # Generate apple
        while len(self.apple_list) <= APPLE_COUNT and len(self.apple_list) + total_snake_length \
                < self.screen_width * self.screen_height * 0.9:
            gen_apple = Apple(pos=self.get_random_pos())

            # Avoid apples in the same location
            is_apple_exist = False
            for apple in self.apple_list:
                if gen_apple == apple:
                    is_apple_exist = True

            # Avoiding apples on snakes
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

        # Check the game over
        self._check_game_over()

        # Check snakes
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
        # When the head of the player and the body of the other player are hit, the game ends
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

        escape_reward = self._update_board()

        stable_reward = 0

        if self.game_over:
            reward = -4
        else:
            reward = escape_reward + stable_reward
            self.current_reward += reward

        if self.show_game:
            self._draw_screen()

        return self._get_state(), reward, self.game_over
