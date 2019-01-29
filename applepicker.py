'''

Apple Picker! A game by Will Larson
Current Version:
2.1.2
- added some sounds
2.1.1
- Added jetpack and animation
- added orange timer for golden apple message
2.1
- added draw_score for bad apples
2.0
- added golden apples
1.0
- added WASD key movement
- changed apple hitboxes
- added high score memory
- added easter egg
- and everything else
'''

import random
import pyxel
import math as m
from os import path

WIDTH = 200
HEIGHT = 160
PLAYER_SPEED = 2
pyxel.mouse(visible=True)
intro = True
version = "2.1.2"

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 13
        self.height = 16
        self.score = 0

class Apple(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BadApple(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xspeed = random.randint(1,3)
        self.yspeed = random.randint(1,3)

class GoldenApple(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xspeed = random.randint(1, 2)
        self.yspeed = random.randint(1, 2)

class App:
    def __init__(self):
        pyxel.init(WIDTH,HEIGHT, caption="Apple Picker!", fps=30)
        self.player = Player(WIDTH/2, 4*HEIGHT/5)
        self.applelist = []
        self.badapplelist = []
        self.goldenapplelist = []
        self.totalapples = 0
        self.totalgoldenapples = 0
        self.totalbadapples = 0
        self.maxapple = 0
        self.caneat = False
        pyxel.load("my_resource.pyxel")

        # loading high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, "applepickerhs"), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # easter egg
        r = random.randint(1,2)
        if r == 1:
            self.race = False
        if r == 2:
            self.race = True

        self.facingright = True
        self.flying = False
        self.atebadapple = False
        pyxel.run(self.update,self.draw)

    def spawn_apple(self):
        if not self.applelist:
            self.applelist.append(Apple(random.randint(2, WIDTH - 5), random.randint(10, HEIGHT - 6)))

    def spawn_bad_apple(self):
        if len(self.badapplelist) < self.maxapple:
            b = random.randint(0,100)
            if b in range(0,1):
                bax = random.randint(2, WIDTH - 5)
                bay = random.randint(10, HEIGHT - 6)
                if m.sqrt((self.player.x - bax)**2 + (self.player.y - bay)**2 > 20):
                    self.badapplelist.append(BadApple(bax, bay))

    def spawn_golden_apple(self):
        if self.player.score > 0:
            if not self.goldenapplelist:
                c = random.randint(0,1000)
                if c in range(0,m.floor((m.log(self.player.score**2))/3)):
                    self.goldenapplelist.append(GoldenApple(random.randint(2, WIDTH - 5), random.randint(10, HEIGHT - 6)))
                    self.goldennow = pyxel.frame_count

    def draw_player(self):
        # Draw the player
        if not self.race:
            if self.flying:
                if self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 16, 0, self.player.width, self.player.height, 7)
                if not self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 16, 0, -self.player.width, self.player.height, 7)
            if not self.flying:
                if self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 27, 16, self.player.width,self.player.height, 7)
                if not self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 27, 16, -self.player.width, self.player.height, 7)
        if self.race:
            if self.flying:
                if self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 0, 16, self.player.width, self.player.height, 0)
                if not self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 0, 16, -self.player.width, self.player.height, 0)
            if not self.flying:
                if self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 14, 16, self.player.width, self.player.height, 0)
                if not self.facingright:
                    pyxel.blt(self.player.x, self.player.y, 1, 14, 16, -self.player.width, self.player.height, 0)

    def draw_apple(self):
        # draw the apples
        for apple in self.applelist:
            pyxel.blt(apple.x,apple.y, 1, 29, 0, 5, 7, 0)

    def draw_bad_apple(self):
        # draw the bad apples
        for badapple in self.badapplelist:
            pyxel.blt(badapple.x,badapple.y, 1, 29, 8, 5, 7, 0)

    def draw_golden_apple(self):
        # draw the golden apples
        for goldenapple in self.goldenapplelist:
            pyxel.blt(goldenapple.x,goldenapple.y, 1, 35, 0, 5, 7, 0)

    def applecollide(self):
        # good apple collision detection
        for apple in self.applelist:
            if apple.x + 2 >= self.player.x and apple.x + 2 <= self.player.x + self.player.width:
                if apple.y + 3 >= self.player.y and apple.y + 3<= self.player.y + self.player.height:
                    pyxel.play(0,2,loop=False)
                    self.applelist.remove(apple)
                    self.player.score += 1
                    self.atebadapple = False
                    self.totalapples += 1

        # bad apple collision detection
        for badapple in self.badapplelist:
            if badapple.x + 2 >= self.player.x and badapple.x + 2 <= self.player.x + self.player.width:
                if badapple.y + 3 >= self.player.y and badapple.y + 3 <= self.player.y + self.player.height:

                    if self.caneat == False:
                        # update the highscore
                        if self.player.score > self.highscore:
                            self.highscore = self.player.score
                            with open(path.join(self.dir, "applepickerhs"), 'w') as f:
                                f.write(str(self.player.score))

                        pyxel.play(0,1,loop=False)
                        self.badapplelist.remove(badapple)
                        self.player.score = 0
                        self.totalapples = 0
                        self.totalgoldenapples = 0
                        self.totalbadapples = 0
                        self.atebadapple = True

                    if self.caneat == True:
                        pyxel.play(0,2)
                        self.badapplelist.remove(badapple)
                        self.player.score += 2
                        self.totalbadapples += 1


        # golden apple collision detection
        for goldenapple in self.goldenapplelist:
            if goldenapple.x + 2 >= self.player.x and goldenapple.x + 2 <= self.player.x + self.player.width:
                if goldenapple.y + 3 >= self.player.y and goldenapple.y + 3 <= self.player.y + self.player.height:
                    pyxel.play(0,2)
                    self.player.score += 5
                    self.totalgoldenapples += 1
                    self.goldenapplelist.remove(goldenapple)
                    self.caneat = True
                    self.ateapple = pyxel.frame_count

    def draw_score(self):
        # draw the mini apples in the top right corner
        for x in range(0,self.totalapples + 1):
          x *= 3
          pyxel.pix(WIDTH - x, 3, 8)
          pyxel.pix(WIDTH - x + 1, 3, 8)
          pyxel.pix(WIDTH - x, 4, 8)
          pyxel.pix(WIDTH - x + 1, 4, 8)
          pyxel.pix(WIDTH - x + 1, 2, 11)

        for x in range(0,self.totalgoldenapples + 1):
          x *= 3
          pyxel.pix(WIDTH - x, 7, 10)
          pyxel.pix(WIDTH - x + 1, 7, 10)
          pyxel.pix(WIDTH - x, 8, 10)
          pyxel.pix(WIDTH - x + 1, 8, 10)
          pyxel.pix(WIDTH - x + 1, 6, 11)

        for x in range(0, self.totalbadapples + 1):
            x *= 3
            pyxel.pix(WIDTH - x, 11, 0)
            pyxel.pix(WIDTH - x + 1, 11, 0)
            pyxel.pix(WIDTH - x, 12, 0)
            pyxel.pix(WIDTH - x + 1, 12, 0)
            pyxel.pix(WIDTH - x + 1, 10, 7)

    def draw(self):

        global intro
        if intro:
            pyxel.cls(12)
            pyxel.blt(52, 62, 1, 0, 56, 96, 36, 0)
            pyxel.text(2, HEIGHT - 15, "A game by Will Larson", 7)
            pyxel.text(2, HEIGHT - 7, "Press space to start", 7)
            pyxel.text(WIDTH - 60,HEIGHT - 7,"HIGHSCORE: " + str(self.highscore), 7)
            pyxel.text(2, 2, "Version " + version, 7)
            self.draw_player()

        if not intro:
            pyxel.cls(12)
            # Draw score
            self.draw_score()
            pyxel.text(2,HEIGHT - 7,"SCORE: " + str(self.player.score), 7)
            if self.atebadapple == True:
                pyxel.text(2, HEIGHT - 15, "You ate a bad apple!", 8)
            pyxel.text(WIDTH - 60, HEIGHT - 7, "HIGHSCORE: " + str(self.highscore), 7)
            self.draw_apple()
            self.draw_bad_apple()
            self.draw_golden_apple()

            if self.caneat == True:
                if pyxel.frame_count - self.ateapple <= 165:
                    pyxel.text(2, HEIGHT - 15, "Eat the bad apples!", 10)
                elif 165 < pyxel.frame_count - self.ateapple < 210:
                    pyxel.text(2, HEIGHT - 15, "Eat the bad apples!", 9)

            self.draw_player()

    def events(self):
        global intro

        self.spawn_apple()
        self.spawn_bad_apple()
        self.spawn_golden_apple()
        self.applecollide()

        # player movement
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player.x -= PLAYER_SPEED
            self.facingright = False
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player.x += PLAYER_SPEED
            self.facingright = True
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.player.y -= PLAYER_SPEED
            self.flying = True
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.player.y += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_B):
            self.race = False

        if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.KEY_W):
            self.flying = False

        # easter egg
        if pyxel.btn(pyxel.KEY_E):
            self.race = True

        # boundaries
        if self.player.x < 0:
            self.player.x = 0
        if self.player.x > WIDTH - self.player.width:
            self.player.x = WIDTH - self.player.width
        if self.player.y < 0:
            self.player.y = 0
        if self.player.y > HEIGHT - self.player.height:
            self.player.y = HEIGHT - self.player.height

        for b in self.badapplelist:
            if b.x < 0:
                b.x = 0
                b.xspeed *= -1
            if b.x > WIDTH - 5:
                b.x = WIDTH - 5
                b.xspeed *= -1
            if b.y < 0:
                b.y = 0
                b.yspeed *= -1
            if b.y > HEIGHT - 5:
                b.y = HEIGHT - 5
                b.yspeed *= -1

        for b in self.goldenapplelist:
            if b.x < 0:
                b.x = 0
                b.xspeed *= -1
            if b.x > WIDTH - 5:
                b.x = WIDTH - 5
                b.xspeed *= -1
            if b.y < 0:
                b.y = 0
                b.yspeed *= -1
            if b.y > HEIGHT - 5:
                b.y = HEIGHT - 5
                b.yspeed *= -1

        # let the player eat the bad apples
        if self.caneat == True:
            # 210 frames = 7 seconds
            if pyxel.frame_count - self.ateapple > 210:
                self.caneat = False

        # make the golden apple time out
        if self.goldenapplelist:
            if pyxel.frame_count - self.goldennow > 150:
                self.goldenapplelist.clear()

        # increasing difficulty based on score
        self.maxapple = (self.player.score + 5)//10

        # start screen
        if pyxel.btn(pyxel.KEY_SPACE):
            intro = False

    def update(self):
        self.events()

        # move the moving apples
        for b in self.badapplelist:
            b.x += b.xspeed
            b.y += b.yspeed

        for b in self.goldenapplelist:
            b.x += b.xspeed
            b.y += b.yspeed

        if pyxel.btn(pyxel.KEY_ESCAPE):
            pyxel.quit()

App()