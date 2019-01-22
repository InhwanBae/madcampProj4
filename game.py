# 장애물 회피 게임 즉, 자율주행차:-D 게임을 구현합니다.
import numpy as np
import random
import pygame
import time

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import multiprocessing

def getColor():
    return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]


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
    def __init__(self, x, y):
        self.pos = Pos(x, y)


class Apple:
    def __init__(self, x, y):
        self.pos = Pos(x, y)
        self.color = (getColor())

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
    def __init__(self, screen_width, screen_height, model_width, model_height, show_game=True):
        self.block_size = 20
        self.apple_count = 30

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.display_width = screen_width * self.block_size
        self.display_height = screen_height * self.block_size

        self.model_width = model_width
        self.model_height = model_height

        self.gameOver = False

        # 지렁이 정의
        # self.snakes = []
        # for i in range(8):
        #     snake = Snake()
        #     self.snakes.append(snake)

        self.snakeList = []
        self.snakeList2 = []
        self.snakeList3 = []
        self.snakeList4 = []
        self.snakeList5 = []
        self.snakeList6 = []
        self.snakeList7 = []
        self.snakeList8 = []

        # 지렁이 길이 정의
        self.snakeLength = 3
        self.snakeLength2 = 3
        self.snakeLength3 = 3
        self.snakeLength4 = 3
        self.snakeLength5 = 3
        self.snakeLength6 = 3
        self.snakeLength7 = 3
        self.snakeLength8 = 3

        # 사과 정의
        self.appleList = []

        # 사용자 지렁이 정의
        self.lead_x = 0
        self.lead_y = 0
        self.lead_x_change = 0
        self.lead_y_change = 0


        self.total_reward = 0.
        self.current_reward = 0.
        self.total_game = 0
        self.show_game = show_game

        # 멀티프로세싱 전용 bot 저장공간
        self.return_direction = [0, 0, 0, 0, 0, 0, 0]

        # 보여주기 위한 설정
        if show_game:
            self.fig, self.axis = self._prepare_display()

    def snakeBot(self, _snakeList, _appleList, _enemyList):
        # 4방위 정의
        #    1
        # 3  0  4
        #    2

        xhead = _snakeList[len(_snakeList) - 1][0]
        yhead = _snakeList[len(_snakeList) - 1][1]

        xpos = [xhead - self.block_size * 3, xhead - self.block_size * 2, xhead - self.block_size, xhead,
                xhead + self.block_size, xhead + self.block_size * 2, xhead + self.block_size * 3]
        ypos = [yhead - self.block_size * 3, yhead - self.block_size * 2, yhead - self.block_size, yhead,
                yhead + self.block_size, yhead + self.block_size * 2, yhead + self.block_size * 3]
        xapos = [xhead - self.block_size * 5, xhead - self.block_size * 4, xhead - self.block_size * 3, xhead - self.block_size * 2,
                 xhead - self.block_size, xhead, xhead + self.block_size, xhead + self.block_size * 2, xhead + self.block_size * 3,
                 xhead + self.block_size * 4, xhead + self.block_size * 5]
        yapos = [yhead - self.block_size * 5, yhead - self.block_size * 4, yhead - self.block_size * 3, yhead - self.block_size * 2,
                 yhead - self.block_size, yhead, yhead + self.block_size, yhead + self.block_size * 2, yhead + self.block_size * 3,
                 yhead + self.block_size * 4, yhead + self.block_size * 5]
        xabpos = [xhead - self.block_size, xhead, xhead + self.block_size]
        yabpos = [yhead - self.block_size, yhead, yhead + self.block_size]

        snakeList = []
        appleList = []
        enemyList = []

        for i in _snakeList:
            if xhead - self.block_size * 5 <= i[0] <= xhead + self.block_size * 5 and yhead - self.block_size * 5 <= i[1] <= yhead + self.block_size * 5:
                snakeList.append(i)
        for j in _appleList:
            if xhead - self.block_size * 5 <= j.pos.x <= xhead + self.block_size * 5 and yhead - self.block_size * 5 <= j.pos.y <= yhead + self.block_size * 5:
                appleList.append(j)
        for k in _enemyList:
            if xhead - self.block_size * 5 <= k[0] <= xhead + self.block_size * 5 and yhead - self.block_size * 5 <= k[1] <= yhead + self.block_size * 5:
                enemyList.append(k)

        # 숫자 같지 않도록 0~1의 난수로 방향 랜덤 가중치
        up = random.random()
        down = random.random()
        left = random.random()
        right = random.random()


        for i in xapos:
            for j in yapos:
                for apple in appleList:
                    if Pos(i,j) == apple.pos:
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
                for apple in appleList:
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
                for apple in appleList:
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
                    if [i, j] == enemy:
                        if xhead < enemy[0] and yhead < enemy[1]:
                            right -= 600 / abs(enemy[0] - xhead)
                            down -= 600 / abs(enemy[1] - yhead)
                        if xhead < enemy[0] and yhead > enemy[1]:
                            right -= 600 / abs(enemy[0] - xhead)
                            up -= 600 / abs(enemy[1] - yhead)
                        if xhead > enemy[0] and yhead < enemy[1]:
                            left -= 600 / abs(enemy[0] - xhead)
                            down -= 600 / abs(enemy[1] - yhead)
                        if xhead > enemy[0] and yhead > enemy[1]:
                            left -= 600 / abs(enemy[0] - xhead)
                            up -= 600 / abs(enemy[1] - yhead)

                for body in snakeList:
                    if [i, j] == body:
                        if xhead <= body[0] and yhead <= body[1]:
                            right -= 100 / (abs(body[0] - xhead) + 20)
                            down -= 100 / (abs(body[1] - yhead) + 20)
                        if xhead <= body[0] and yhead >= body[1]:
                            right -= 100 / (abs(body[0] - xhead) + 20)
                            up -= 100 / (abs(body[1] - yhead) + 20)
                        if xhead >= body[0] and yhead <= body[1]:
                            left -= 100 / (abs(body[0] - xhead) + 20)
                            down -= 100 / (abs(body[1] - yhead) + 20)
                        if xhead >= body[0] and yhead >= body[1]:
                            left -= 100 / (abs(body[0] - xhead) + 20)
                            up -= 100 / (abs(body[1] - yhead) + 20)

        if [xhead, yhead - self.block_size] in snakeList:
            up -= 10000
        if [xhead, yhead + self.block_size] in snakeList:
            down -= 10000
        if [xhead - self.block_size, yhead] in snakeList:
            left -= 10000
        if [xhead + self.block_size, yhead] in snakeList:
            right -= 10000

        u = False
        d = False
        l = False
        r = False

        if Apple(xhead, yhead - self.block_size) in appleList:
            up += 2000
        if Apple(xhead, yhead + self.block_size) in appleList:
            down += 2000
        if Apple(xhead - self.block_size, yhead) in appleList:
            left += 2000
        if Apple(xhead + self.block_size, yhead) in appleList:
            right += 2000

        if yhead - self.block_size < 0:
            up -= 1000
        if yhead + self.block_size >= self.display_height:
            down -= 1000
        if xhead - self.block_size < self.display_width:
            left -= 1000
        if xhead + self.block_size >= self.display_width:
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

    def snakeBotMulti(self, botData):
        """멀티프로세싱 전용 함수"""
        #print("Process start")
        direction = self.snakeBot(botData[1], botData[2], botData[3])
        #self.return_direction[botData[0]] = direction
        #print("bot", botData[0] + 2, "direction:", direction)
        return direction
        #print("Process end")

    def _prepare_display(self):
        # TODO: 수정 예정
        """게임을 화면에 보여주기 위해 matplotlib 으로 출력할 화면을 설정합니다."""

        fig, axis = plt.subplots(figsize=(self.screen_height, self.screen_width))
        """
        fig.set_size_inches(8, 8)
        # 화면을 닫으면 프로그램을 종료합니다.
        fig.canvas.mpl_connect('close_event', exit)
        plt.axis((0, self.screen_width, 0, self.screen_height))
        plt.tick_params(top='off', right='off',
                        left='off', labelleft='off',
                        bottom='off', labelbottom='off')
        plt.draw()
        # 게임을 진행하며 화면을 업데이트 할 수 있도록 interactive 모드로 설정합니다.
        plt.ion()
        plt.show()
        """

        pygame.init()
        self.fps = 15
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("SLITHER.IO")

        self.img = pygame.image.load("snakeHead.png")
        self.clock = pygame.time.Clock()


        return fig, axis

    def _get_state(self):
        # TODO: 값 세부 수정 예정 (사과 0, 바닥 0.25, 자기자신 0.5, 다른 지렁이 0.75, 벽 1)

        state = np.zeros((self.screen_width, self.screen_height))
        state.fill(0.25)

        # 자기 자신 1로 표현
        for points in self.snakeList:
            # 맵 밖으로 나가서 죽은 뱀들 처리
            if 0 <= round(points[0] / self.block_size) < self.screen_height and \
                    0 <= round(points[1] / self.block_size) < self.screen_width:
                state[round(points[0] / self.block_size)][round(points[1] / self.block_size)] = 0.5

        # 다른 지렁이 0.25 로 표현
        for points in self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + \
                      self.snakeList7 + self.snakeList8:
            # 맵 밖으로 나가서 죽은 뱀들 처리
            if 0 <= round(points[0] / self.block_size) < self.screen_height and \
                    0 <= round(points[1] / self.block_size) < self.screen_width:
                state[round(points[0] / self.block_size)][round(points[1] / self.block_size)] = 0.75

        # 사과 0.75로 표현
        for apple in self.appleList:
            points = apple.pos
            # 맵 밖 사과 처리
            if 0 <= round(points.x / self.block_size) < self.screen_height and \
                    0 <= round(points.y / self.block_size) < self.screen_width:
                state[round(points.x / self.block_size)][round(points.y / self.block_size)] = 0

        # 벽 0.5로 표현


        # 머리 주변의 값 보내주기
        current_state = np.zeros((self.model_width, self.model_height))
        current_state.fill(1)

        xhead = round(self.snakeList[len(self.snakeList) - 1][0] / self.block_size)
        yhead = round(self.snakeList[len(self.snakeList) - 1][1] / self.block_size)

        #print([xhead, yhead])

        xmiddle = round(self.model_width / 2 + 0.1)
        ymiddle = round(self.model_height / 2 + 0.1)

        #print([xmiddle, ymiddle])

        for i in range(xhead - (xmiddle - 1), xhead + xmiddle):
            for j in range(yhead - (ymiddle - 1), yhead + ymiddle):
                if 0 <= i < self.screen_width and 0 <= j < self.screen_width:
                    current_state[i - (xhead - (xmiddle - 1))][j - (yhead - (ymiddle - 1))] = state[i][j]

        """
        print("")
        for k in current_state:
            print(k)
        print("")
        """

        return current_state

    def snake(self, block_size, snakelist, slot):
        if slot == 1:
            color = (255, 255, 255)
        elif slot == 2:
            color = (0, 0, 255)
        elif slot == 3:
            color = (0, 0, 255)
        elif slot == 4:
            color = (0, 0, 255)
        elif slot == 5:
            color = (0, 0, 255)
        elif slot == 6:
            color = (0, 0, 255)
        elif slot == 7:
            color = (0, 0, 255)
        elif slot == 8:
            color = (0, 0, 255)
        self.gameDisplay.blit(self.img, (snakelist[-1][0], snakelist[-1][1]))
        for XnY in snakelist[:-1]:
            pygame.draw.rect(self.gameDisplay, color, [XnY[0], XnY[1], block_size, block_size])

    def _draw_screen(self):
        # TODO: 수정 예정
        """
        title = " Avg. Reward: %d Reward: %d Snake Length: %d Total Game: %d" % (
                        self.total_reward / self.total_game,
                        self.current_reward, self.snakeLength,
                        self.total_game)

        # self.axis.clear()
        self.axis.set_title(title, fontsize=12)

        # 게임판 검은색 표현
        road = patches.Rectangle((0, 0), self.screen_width, self.screen_height, linewidth=0, facecolor="#000000")
        self.axis.add_patch(road)

        # 사과 빨간색 표현
        for points in self.appleList:
            # 맵 밖 사과 처리
            posx = round(points[0] / self.block_size)
            posy = round(points[1] / self.block_size)
            if 0 <= posx < self.screen_height and 0 <= posy < self.screen_width:
                block = patches.Rectangle((posx, self.screen_height - posy - 1), 1, 1, linewidth=0, facecolor="#FF0000")
                self.axis.add_patch(block)

        # 자기 자신 흰색 표현
        for points in self.snakeList:
            # 맵 밖으로 나가서 죽은 뱀들 처리
            posx = round(points[0] / self.block_size)
            posy = round(points[1] / self.block_size)
            if 0 <= posx < self.screen_height and 0 <= posy < self.screen_width:
                block = patches.Rectangle((posx, self.screen_height - posy - 1), 1, 1, linewidth=0, facecolor="#FFFFFF")
                self.axis.add_patch(block)

        # 다른 지렁이 파란색 표현
        for points in self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + \
                      self.snakeList7 + self.snakeList8:
            # 맵 밖으로 나가서 죽은 뱀들 처리
            posx = round(points[0] / self.block_size)
            posy = round(points[1] / self.block_size)
            if 0 <= posx < self.screen_height and 0 <= posy < self.screen_width:
                block = patches.Rectangle((posx, self.screen_height - posy - 1), 1, 1, linewidth=0, facecolor="#0000FF")
                self.axis.add_patch(block)

        self.fig.canvas.draw()
        # 게임의 다음 단계 진행을 위해 matplot 의 이벤트 루프를 잠시 멈춥니다.
        plt.pause(0.0001)
        """
        # 게임 화면에 구현
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.gameDisplay.fill((0, 0, 0))

        for apple in self.appleList:
            # pygame.draw.rect(self.gameDisplay, (255, 0, 0), [apple.pos.x, apple.pos.y, self.block_size, self.block_size])
            pygame.draw.circle(self.gameDisplay, apple.color, (int(apple.pos.x), int(apple.pos.y)), self.block_size)
        self.snake(self.block_size, self.snakeList, 1)
        self.snake(self.block_size, self.snakeList3, 3)
        self.snake(self.block_size, self.snakeList4, 4)
        self.snake(self.block_size, self.snakeList5, 5)
        self.snake(self.block_size, self.snakeList6, 6)
        self.snake(self.block_size, self.snakeList7, 7)
        self.snake(self.block_size, self.snakeList8, 8)

        # 화면 업데이트
        pygame.display.update()

        # 다음 틱까지 대기
        self.clock.tick(self.fps)


    def reset(self):
        # 게임 판 초기화
        self.gameOver = False

        self.return_direction = [0, 0, 0, 0, 0, 0, 0]

        # 지렁이 정의
        self.snakeList = []
        self.snakeList2 = []
        self.snakeList3 = []
        self.snakeList4 = []
        self.snakeList5 = []
        self.snakeList6 = []
        self.snakeList7 = []
        self.snakeList8 = []

        # 지렁이 길이 정의
        self.snakeLength = 3
        self.snakeLength2 = 3
        self.snakeLength3 = 3
        self.snakeLength4 = 3
        self.snakeLength5 = 3
        self.snakeLength6 = 3
        self.snakeLength7 = 3
        self.snakeLength8 = 3

        self.lead_x = round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0
        self.lead_y = round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0
        self.lead_x_change = 0
        self.lead_y_change = 0

        self.appleList = []

        # 지렁이들의 위치 생성
        while True:
            randPosition = [round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0,
                            round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0]

            # 값 지정
            if len(self.snakeList) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList.append([self.lead_x, self.lead_y])
                continue
            if len(self.snakeList2) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList2.append(randPosition)
                continue
            if len(self.snakeList3) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList3.append(randPosition)
                continue
            if len(self.snakeList4) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList4.append(randPosition)
                continue
            if len(self.snakeList5) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList5.append(randPosition)
                continue
            if len(self.snakeList6) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList6.append(randPosition)
                continue
            if len(self.snakeList7) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList7.append(randPosition)
                continue
            if len(self.snakeList8) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList8.append(randPosition)
                continue

            # 종료조건
            if len(self.snakeList) > 0 and len(self.snakeList2) > 0 and len(self.snakeList3) > 0 and \
                    len(self.snakeList4) > 0 and len(self.snakeList5) > 0 and len(self.snakeList6) > 0 and \
                    len(self.snakeList7) > 0 and len(self.snakeList8) > 0:
                break

        # 사과 생성
        while len(self.appleList) <= self.apple_count:
            randAppleX = round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0
            randAppleY = round(random.randrange(0, self.display_height - self.block_size) / 20.0) * 20.0
            genApple = Apple(randAppleX, randAppleY)

            # 같은 위치에 사과가 생기지 않도록 함
            noApple = True
            for apple in self.appleList:
                if genApple == apple:
                    noApple = False
            # 뱀 위에 사과가 생기지 않도록 함
            for snakeAll in [self.snakeList, self.snakeList2, self.snakeList3, self.snakeList4, self.snakeList5,
                             self.snakeList6, self.snakeList7,self.snakeList8]:
                for snakeBody in snakeAll:
                    if genApple.pos.x == snakeBody[0] and genApple.pos.y == snakeBody[1]:
                        noApple = False

            if noApple == True:
                self.appleList.append(genApple)

        self.current_reward = 0
        self.total_game += 1
        self._update_block()
        return self._get_state()

    def _update_car(self, move):
        # 4방위 정의
        #    1
        # 4  0  2
        #    3
        print(move, end="")

        # 사용자 입력 처리문
        if move == 4:
            self.lead_x_change = -self.block_size
            self.lead_y_change = 0
        elif move == 2:
            self.lead_x_change = self.block_size
            self.lead_y_change = 0
        elif move == 1:
            self.lead_y_change = -self.block_size
            self.lead_x_change = 0
        elif move == 3:
            self.lead_y_change = self.block_size
            self.lead_x_change = 0

        # 머리의 위치 추가
        self.lead_x += self.lead_x_change
        self.lead_y += self.lead_y_change

        # 머리 이동,리스트 추가 및 맨 마지막 꼬리 제거
        self.snakeList.append([self.lead_x, self.lead_y])
        if len(self.snakeList) > self.snakeLength:
            del self.snakeList[0]

    def _update_block(self):
        # TODO: 수정 예정
        reward = 0

        removeAppleList = []

        # 사과를 먹었을 때 처리
        for apple in self.appleList:
            if self.snakeList[len(self.snakeList) - 1][0] == [apple.pos.x, apple.pos.y]:
                self.snakeLength += 1
                removeAppleList.append(apple)
                # 리워드 추가
                reward += 1
            if self.snakeList2[len(self.snakeList2) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength2 += 1
                removeAppleList.append(apple)
            if self.snakeList3[len(self.snakeList3) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength3 += 1
                removeAppleList.append(apple)
            if self.snakeList4[len(self.snakeList4) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength4 += 1
                removeAppleList.append(apple)
            if self.snakeList5[len(self.snakeList5) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength5 += 1
                removeAppleList.append(apple)
            if self.snakeList6[len(self.snakeList6) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength6 += 1
                removeAppleList.append(apple)
            if self.snakeList7[len(self.snakeList7) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength7 += 1
                removeAppleList.append(apple)
            if self.snakeList8[len(self.snakeList8) - 1] == [apple.pos.x, apple.pos.y]:
                self.snakeLength8 += 1
                removeAppleList.append(apple)

        # 사과 제거
        for rapple in removeAppleList:
            try:
                self.appleList.remove(rapple)
                break
            except(RuntimeError):
                pass

        # 사과 생성
        while len(self.appleList) <= self.apple_count and len(self.appleList) + len(self.snakeList) + \
                len(self.snakeList2) + len(self.snakeList3) + len(self.snakeList4) + len(self.snakeList5) + \
                len(self.snakeList6) + len(self.snakeList7) + len(self.snakeList8) \
                < self.screen_width * self.screen_height * 0.9:
            randAppleX = round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0
            randAppleY = round(random.randrange(0, self.display_height - self.block_size) / 20.0) * 20.0
            genApple = Apple(randAppleX, randAppleY)

            # 같은 위치에 사과가 생기지 않도록 함
            noApple = True
            for apple in self.appleList:
                if genApple == apple:
                    noApple = False
            # 뱀 위에 사과가 생기지 않도록 함
            for snakeAll in [self.snakeList, self.snakeList2, self.snakeList3, self.snakeList4, self.snakeList5,
                             self.snakeList6, self.snakeList7, self.snakeList8]:
                for snakeBody in snakeAll:
                    if genApple == snakeBody:
                        noApple = False

            if noApple == True:
                self.appleList.append(genApple)

        # Snake Bot 이동
        """
        # 멀티프로세싱
        bot2data = [0, self.snakeList2, self.appleList, self.snakeList + self.snakeList3 + self.snakeList4 +
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8]
        bot3data = [1, self.snakeList3, self.appleList, self.snakeList + self.snakeList2 + self.snakeList4 +
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8]
        bot4data = [2, self.snakeList4, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8]
        bot5data = [3, self.snakeList5, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                    self.snakeList4 + self.snakeList6 + self.snakeList7 + self.snakeList8]
        bot6data = [4, self.snakeList6, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                    self.snakeList4 + self.snakeList5 + self.snakeList7 + self.snakeList8]
        bot7data = [5, self.snakeList7, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                    self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList8]
        bot8data = [6, self.snakeList8, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                    self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7]
        botdata = [bot2data, bot3data, bot4data, bot5data, bot6data, bot7data, bot8data]

        #print("multiprocessing start")
        pool = multiprocessing.Pool(processes=1)
        data = pool.map(self.snakeBotMulti, botdata)

        #pool.close()
        #pool.join()
        #print("multiprocessing end")
        #print(self.return_direction)
        print(data)
        self.return_direction = data
        """
        # bot2
        status = self.snakeBot(self.snakeList2, self.appleList, self.snakeList + self.snakeList3 + self.snakeList4 +
                               self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8)

        #status = self.return_direction[0]
        if status == 1:
            self.snakeList2.append([self.snakeList2[len(self.snakeList2) - 1][0],
                                    self.snakeList2[len(self.snakeList2) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList2.append([self.snakeList2[len(self.snakeList2) - 1][0],
                                    self.snakeList2[len(self.snakeList2) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList2.append([self.snakeList2[len(self.snakeList2) - 1][0] - self.block_size,
                                    self.snakeList2[len(self.snakeList2) - 1][1]])
        elif status == 4:
            self.snakeList2.append([self.snakeList2[len(self.snakeList2) - 1][0] + self.block_size,
                                    self.snakeList2[len(self.snakeList2) - 1][1]])
        if len(self.snakeList2) > self.snakeLength2:
            del self.snakeList2[0]

        # bot3

        status = self.snakeBot(self.snakeList3, self.appleList,self.snakeList + self.snakeList2 + self.snakeList4 +
                               self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8)

        #status = self.return_direction[1]
        if status == 1:
            self.snakeList3.append([self.snakeList3[len(self.snakeList3) - 1][0],
                                    self.snakeList3[len(self.snakeList3) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList3.append([self.snakeList3[len(self.snakeList3) - 1][0],
                                    self.snakeList3[len(self.snakeList3) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList3.append([self.snakeList3[len(self.snakeList3) - 1][0] - self.block_size,
                                    self.snakeList3[len(self.snakeList3) - 1][1]])
        elif status == 4:
            self.snakeList3.append([self.snakeList3[len(self.snakeList3) - 1][0] + self.block_size,
                                    self.snakeList3[len(self.snakeList3) - 1][1]])
        if len(self.snakeList3) > self.snakeLength3:
            del self.snakeList3[0]

        # bot4

        status = self.snakeBot(self.snakeList4, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                               self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8)

        #status = self.return_direction[2]
        if status == 1:
            self.snakeList4.append([self.snakeList4[len(self.snakeList4) - 1][0],
                                    self.snakeList4[len(self.snakeList4) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList4.append([self.snakeList4[len(self.snakeList4) - 1][0],
                                    self.snakeList4[len(self.snakeList4) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList4.append([self.snakeList4[len(self.snakeList4) - 1][0] - self.block_size,
                                    self.snakeList4[len(self.snakeList4) - 1][1]])
        elif status == 4:
            self.snakeList4.append([self.snakeList4[len(self.snakeList4) - 1][0] + self.block_size,
                                    self.snakeList4[len(self.snakeList4) - 1][1]])
        if len(self.snakeList4) > self.snakeLength4:
            del self.snakeList4[0]

        # bot5

        status = self.snakeBot(self.snakeList5, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                               self.snakeList4 + self.snakeList6 + self.snakeList7 + self.snakeList8)

        #status = self.return_direction[3]
        if status == 1:
            self.snakeList5.append([self.snakeList5[len(self.snakeList5) - 1][0],
                                    self.snakeList5[len(self.snakeList5) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList5.append([self.snakeList5[len(self.snakeList5) - 1][0],
                                    self.snakeList5[len(self.snakeList5) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList5.append([self.snakeList5[len(self.snakeList5) - 1][0] - self.block_size,
                                    self.snakeList5[len(self.snakeList5) - 1][1]])
        elif status == 4:
            self.snakeList5.append([self.snakeList5[len(self.snakeList5) - 1][0] + self.block_size,
                                    self.snakeList5[len(self.snakeList5) - 1][1]])
        if len(self.snakeList5) > self.snakeLength5:
            del self.snakeList5[0]

        # bot6

        status = self.snakeBot(self.snakeList6, self.appleList, self.snakeList +self.snakeList2 + self.snakeList3 +
                               self.snakeList4 + self.snakeList5 + self.snakeList7 + self.snakeList8)

        #status = self.return_direction[4]
        if status == 1:
            self.snakeList6.append([self.snakeList6[len(self.snakeList6) - 1][0],
                                    self.snakeList6[len(self.snakeList6) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList6.append([self.snakeList6[len(self.snakeList6) - 1][0],
                                    self.snakeList6[len(self.snakeList6) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList6.append([self.snakeList6[len(self.snakeList6) - 1][0] - self.block_size,
                                    self.snakeList6[len(self.snakeList6) - 1][1]])
        elif status == 4:
            self.snakeList6.append([self.snakeList6[len(self.snakeList6) - 1][0] + self.block_size,
                                    self.snakeList6[len(self.snakeList6) - 1][1]])
        if len(self.snakeList6) > self.snakeLength6:
            del self.snakeList6[0]

        # bot7

        status = self.snakeBot(self.snakeList7, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                               self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList8)

        #status = self.return_direction[5]
        if status == 1:
            self.snakeList7.append([self.snakeList7[len(self.snakeList7) - 1][0],
                                    self.snakeList7[len(self.snakeList7) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList7.append([self.snakeList7[len(self.snakeList7) - 1][0],
                                    self.snakeList7[len(self.snakeList7) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList7.append([self.snakeList7[len(self.snakeList7) - 1][0] - self.block_size,
                                    self.snakeList7[len(self.snakeList7) - 1][1]])
        elif status == 4:
            self.snakeList7.append([self.snakeList7[len(self.snakeList7) - 1][0] + self.block_size,
                                    self.snakeList7[len(self.snakeList7) - 1][1]])
        if len(self.snakeList7) > self.snakeLength7:
            del self.snakeList7[0]

        # bot8

        status = self.snakeBot(self.snakeList8, self.appleList, self.snakeList + self.snakeList2 + self.snakeList3 +
                               self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7)

        #status = self.return_direction[6]
        if status == 1:
            self.snakeList8.append([self.snakeList8[len(self.snakeList8) - 1][0],
                                    self.snakeList8[len(self.snakeList8) - 1][1] - self.block_size])
        elif status == 2:
            self.snakeList8.append([self.snakeList8[len(self.snakeList8) - 1][0],
                                    self.snakeList8[len(self.snakeList8) - 1][1] + self.block_size])
        elif status == 3:
            self.snakeList8.append([self.snakeList8[len(self.snakeList8) - 1][0] - self.block_size,
                                    self.snakeList8[len(self.snakeList8) - 1][1]])
        elif status == 4:
            self.snakeList8.append([self.snakeList8[len(self.snakeList8) - 1][0] + self.block_size,
                                    self.snakeList8[len(self.snakeList8) - 1][1]])
        if len(self.snakeList8) > self.snakeLength8:
            del self.snakeList8[0]

        # 플레이어의 머리와 타 플레이어의 몸통이 부딛힐 경우 게임 종료
        if self.snakeList[len(self.snakeList) - 1] in self.snakeList[:-1] or self.snakeList[len(self.snakeList) - 1] in self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
            self.gameOver = True

        # 컴퓨터끼리 부딛힐 경우, 밖으로 나갈 경우, 사과로 바뀌고 컴퓨터 초기화
        appleAddList = []
        removeSnake2 = removeSnake3 = removeSnake4 = removeSnake5 = removeSnake6 = removeSnake7 = removeSnake8 = False

        if self.snakeList2[len(self.snakeList2) - 1] in self.snakeList2[:-1] or self.snakeList2[len(self.snakeList2) - 1] in self.snakeList + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
            for pos in self.snakeList2:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake2 = True
        if self.snakeList3[len(self.snakeList3) - 1] in self.snakeList3[:-1] or self.snakeList3[len(self.snakeList3) - 1] in self.snakeList + self.snakeList2 + self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
            for pos in self.snakeList3:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake3 = True
        if self.snakeList4[len(self.snakeList4) - 1] in self.snakeList4[:-1] or self.snakeList4[len(self.snakeList4) - 1] in self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
            for pos in self.snakeList4:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake4 = True
        if self.snakeList5[len(self.snakeList5) - 1] in self.snakeList5[:-1] or self.snakeList5[len(self.snakeList5) - 1] in self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList6 + self.snakeList7 + self.snakeList8:
            for pos in self.snakeList5:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake5 = True
        if self.snakeList6[len(self.snakeList6) - 1] in self.snakeList6[:-1] or self.snakeList6[len(self.snakeList6) - 1] in self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList7 + self.snakeList8:
            for pos in self.snakeList6:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake6 = True
        if self.snakeList7[len(self.snakeList7) - 1] in self.snakeList7[:-1] or self.snakeList7[len(self.snakeList7) - 1] in self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList8:
            for pos in self.snakeList7:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake7 = True
        if self.snakeList8[len(self.snakeList8) - 1] in self.snakeList8[:-1] or self.snakeList8[len(self.snakeList8) - 1] in self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7:
            for pos in self.snakeList8:
                appleAddList.append(Apple(pos[0], pos[1]))
            removeSnake8 = True

        if self.snakeList2[len(self.snakeList2) - 1][0] >= self.display_width or \
                self.snakeList2[len(self.snakeList2) - 1][0] < 0 or \
                self.snakeList2[len(self.snakeList2) - 1][1] >= self.display_height or \
                self.snakeList2[len(self.snakeList2) - 1][1] < 0:
            # appleAddList += self.snakeList2
            removeSnake2 = True
        if self.snakeList3[len(self.snakeList3) - 1][0] >= self.display_width or \
                self.snakeList3[len(self.snakeList3) - 1][0] < 0 or \
                self.snakeList3[len(self.snakeList3) - 1][1] >= self.display_height or \
                self.snakeList3[len(self.snakeList3) - 1][1] < 0:
            # appleAddList += self.snakeList3
            removeSnake3 = True
        if self.snakeList4[len(self.snakeList4) - 1][0] >= self.display_width or \
                self.snakeList4[len(self.snakeList4) - 1][0] < 0 or \
                self.snakeList4[len(self.snakeList4) - 1][1] >= self.display_height or \
                self.snakeList4[len(self.snakeList4) - 1][1] < 0:
            # appleAddList += self.snakeList4
            removeSnake4 = True
        if self.snakeList5[len(self.snakeList5) - 1][0] >= self.display_width or \
                self.snakeList5[len(self.snakeList5) - 1][0] < 0 or \
                self.snakeList5[len(self.snakeList5) - 1][1] >= self.display_height or \
                self.snakeList5[len(self.snakeList5) - 1][1] < 0:
            # appleAddList += self.snakeList5
            removeSnake5 = True
        if self.snakeList6[len(self.snakeList6) - 1][0] >= self.display_width or \
                self.snakeList6[len(self.snakeList6) - 1][0] < 0 or \
                self.snakeList6[len(self.snakeList6) - 1][1] >= self.display_height or \
                self.snakeList6[len(self.snakeList6) - 1][1] < 0:
            # appleAddList += self.snakeList6
            removeSnake6 = True
        if self.snakeList7[len(self.snakeList7) - 1][0] >= self.display_width or \
                self.snakeList7[len(self.snakeList7) - 1][0] < 0 or \
                self.snakeList7[len(self.snakeList7) - 1][1] >= self.display_height or \
                self.snakeList7[len(self.snakeList7) - 1][1] < 0:
            # appleAddList += self.snakeList7
            removeSnake7 = True
        if self.snakeList8[len(self.snakeList8) - 1][0] >= self.display_width or \
                self.snakeList8[len(self.snakeList8) - 1][0] < 0 or \
                self.snakeList8[len(self.snakeList8) - 1][1] >= self.display_height or \
                self.snakeList8[len(self.snakeList8) - 1][1] < 0:
            # appleAddList += self.snakeList8
            removeSnake8 = True

        if removeSnake2:
            self.snakeList2.clear()
            self.snakeLength2 = 3
        if removeSnake3:
            self.snakeList3.clear()
            self.snakeLength3 = 3
        if removeSnake4:
            self.snakeList4.clear()
            self.snakeLength4 = 3
        if removeSnake5:
            self.snakeList5.clear()
            self.snakeLength5 = 3
        if removeSnake6:
            self.snakeList6.clear()
            self.snakeLength6 = 3
        if removeSnake7:
            self.snakeList7.clear()
            self.snakeLength7 = 3
        if removeSnake8:
            self.snakeList8.clear()
            self.snakeLength8 = 3

        for apple in appleAddList:
            if apple not in self.appleList:
                self.appleList.append(apple)

        while True:
            randPosition = [round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0,
                            round(random.randrange(0, self.display_width - self.block_size) / 20.0) * 20.0]

            # 컴퓨터 값 지정
            if len(self.snakeList2) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList2.append(randPosition)
                continue
            if len(self.snakeList3) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList3.append(randPosition)
                continue
            if len(self.snakeList4) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList4.append(randPosition)
                continue
            if len(self.snakeList5) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList5.append(randPosition)
                continue
            if len(self.snakeList6) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList6.append(randPosition)
                continue
            if len(self.snakeList7) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList7.append(randPosition)
                continue
            if len(self.snakeList8) == 0 and randPosition not in \
                    self.snakeList + self.snakeList2 + self.snakeList3 + self.snakeList4 + \
                    self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
                self.snakeList8.append(randPosition)
                continue

            # 종료조건
            if len(self.snakeList) > 0 and len(self.snakeList2) > 0 and len(self.snakeList3) > 0 and \
                    len(self.snakeList4) > 0 and len(self.snakeList5) > 0 and len(self.snakeList6) > 0 and \
                    len(self.snakeList7) > 0 and len(self.snakeList8) > 0:
                break

        return reward

    def _is_gameover(self):
        # 플레이어의 머리와 타 플레이어의 몸통이 부딛힐 경우 게임 종료
        if self.snakeList[len(self.snakeList)-1] in self.snakeList2 + self.snakeList3 + self.snakeList4 + self.snakeList5 + self.snakeList6 + self.snakeList7 + self.snakeList8:
            self.total_reward += self.current_reward
            return True
        elif self.lead_x >= self.display_width or self.lead_x < 0 or self.lead_y >= self.display_height or self.lead_y < 0:
            self.total_reward += self.current_reward
            return True
        elif self.gameOver == True:
            self.total_reward += self.current_reward
            return True
        else:
            return False

    def step(self, action):
        # action: 0: 상, 1: 오, 2: 하, 3: 왼
        # 게임 진행
        self._update_car(action + 1)

        # 장애물을 이동시킵니다. 장애물이 자동차에 충돌하지 않고 화면을 모두 지나가면 보상을 얻습니다.
        escape_reward = self._update_block()

        # 움직임이 적을 경우에도 보상을 줘서 안정적으로 이동하는 것 처럼 보이게 만듭니다.
        #stable_reward = 1. / self.screen_height if action == 1 else 0
        stable_reward = 0

        # 게임이 종료됐는지를 판단합니다. 자동차와 장애물이 충돌했는지를 파악합니다.
        gameover = self._is_gameover()

        if gameover:
            # 장애물에 충돌한 경우 -8점을 보상으로 줍니다.
            reward = -4
        else:
            reward = escape_reward + stable_reward
            self.current_reward += reward

        if self.show_game:
            self._draw_screen()

        return self._get_state(), reward, gameover

