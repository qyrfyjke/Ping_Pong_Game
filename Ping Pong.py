import tkinter as tk
import random as rand
import threading
import os

WIDTH = 1000
HEIGHT = 800
MARGIN = 15
VELOCITY = 15


class Ball:
    def __init__(self, canvas, width, velocity, boardwidth, boardheight):
        self.width = width
        self.boardwidth = boardwidth
        self.boardheight = boardheight
        self.topx = boardwidth / 2 - width / 2
        self.topy = boardheight / 2 - width / 2
        self.velocity = velocity
        self.vx = velocity
        self.vy = velocity
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(self.topx, self.topy, self.topx + self.width, self.topy + self.width,
                                               fill='white')

    def draw(self):
        self.canvas.coords(self.id, self.topx, self.topy, self.topx + self.width, self.topy + self.width)

    def restart(self):
        self.topx = self.boardwidth / 2 - self.width / 2
        self.topy = self.boardheight / 2 - self.width / 2
        self.vx = (-1, 1)[rand.random() > 0.5] * self.velocity
        self.vy = (-1, 1)[rand.random() > 0.5] * self.velocity

    def move(self, pong, paddleright, paddleleft):

        if self.topy <= 0 or (self.topy + self.width) >= self.boardheight:
            self.vy = self.vy * -1

        if paddleright.collideright(self) or paddleleft.collideleft(self):
            self.vx = self.vx * -1

        if (self.topx + self.width) >= self.boardwidth:
            pong.leftpoints = pong.leftpoints + 1
            return True

        if self.topx <= 0:
            pong.rightpoints = pong.rightpoints + 1
            return True

        self.topx = self.topx + self.vx
        self.topy = self.topy + self.vy

        return False


class Paddle:
    def __init__(self, canvas, topx, topy, width, height, boardheight):
        self.topx = topx
        self.topy = topy
        self.width = width
        self.height = height
        self.boardheight = boardheight
        self.score = 0
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(self.topx, self.topy, self.topx + self.width, self.topy + self.height,
                                               fill='white')

    def draw(self):
        self.canvas.coords(self.id, self.topx, self.topy, self.topx + self.width, self.topy + self.height)

    def top(self):
        if self.topy - VELOCITY > 0:
            self.topy = self.topy - VELOCITY

    def down(self):
        if (self.topy + self.height + VELOCITY) < self.boardheight:
            self.topy = self.topy + VELOCITY

    def collideright(self, ball):
        if (ball.topx + ball.width) >= self.topx and (
                ball.topy >= self.topy or (ball.topy + ball.width) >= self.topy) and (
                (ball.topy + ball.width) <= (self.topy + self.height) or ball.topy <= (self.topy + self.height)):
            return True

        return False

    def collideleft(self, ball):
        if ball.topx <= (self.topx + self.width) and (
                ball.topy >= self.topy or (ball.topy + ball.width) >= self.topy) and (
                (ball.topy + ball.width) <= (self.topy + self.height) or ball.topy <= (self.topy + self.height)):
            return True

        return False


class Pong:
    def __init__(self, root, width, height, margin):
        paddlewidth = width / 50
        paddleheight = height / 12
        self.leftpoints = 0
        self.lefttxt = None
        self.rightpoints = 0
        self.righttxt = None
        self.render = True

        self.leftup = False
        self.leftdown = False

        self.rightup = False
        self.rightdown = False
        self.width = width
        self.height = height
        self.margin = margin
        self.root = root
        self.root.title("Pong Game")
        self.root.geometry(str(width) + "x" + str(height))

        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='black')
        self.paddleleft = Paddle(self.canvas, margin, height / 2 - paddleheight / 2, paddlewidth, paddleheight, height)
        self.paddleright = Paddle(self.canvas, (width - margin) - paddlewidth, height / 2 - paddleheight / 2,
                                  paddlewidth, paddleheight, height)
        self.ball = Ball(self.canvas, paddlewidth, VELOCITY, width, height)
        self.canvas.pack()
        self.drawmiddlelines()
        self.drawboard()
        self.move()

    def drawmiddlelines(self):
        leftx = self.width / 2 - self.paddleleft.width / 2

        for y in range(0, self.height, int(self.paddleleft.height + self.margin * 2)):
            self.canvas.create_rectangle(leftx, y, leftx + self.paddleleft.width, y + self.paddleleft.height,
                                         fill='grey')

    def drawboard(self):
        try:

            self.paddleleft.draw()
            self.paddleright.draw()

            self.drawpoints()

            self.ball.draw()
        except:
            os._exit(0)

    def drawpoints(self):

        if self.lefttxt != None:
            self.canvas.delete(self.lefttxt)

        self.lefttxt = self.canvas.create_text(self.width / 2 - 50, 50, text=str(self.leftpoints), fill='grey',
                                               font=("Helvetica 35 bold"))

        if self.righttxt != None:
            self.canvas.delete(self.righttxt)

        self.righttxt = self.canvas.create_text(self.width / 2 + 50, 50, text=str(self.rightpoints), fill='grey',
                                                font=("Helvetica 35 bold"))

    def move(self):
        if self.render:
            self.timer = threading.Timer(0.05, self.move)
            self.timer.start()

            # we manage touch events
            if self.leftup:
                self.paddleleft.top()

            if self.leftdown:
                self.paddleleft.down()

            if self.rightup:
                self.paddleright.top()

            if self.rightdown:
                self.paddleright.down()

            state = self.ball.move(self, self.paddleright, self.paddleleft)

            if state:
                self.restart()

            self.drawboard()

    def restart(self):
        self.ball.restart()

    # Управление: w и s для левой - u и j для правой
    def keypress(self, event):
        match event.char:
            case 'w':
                self.leftup = True
            case 's':
                self.leftdown = True
            case 'u':
                self.rightup = True
            case 'j':
                self.rightdown = True

    def keyrelease(self, event):
        match event.char:
            case 'w':
                self.leftup = False
            case 's':
                self.leftdown = False
            case 'u':
                self.rightup = False
            case 'j':
                self.rightdown = False

    def killtimer(self):
        self.render = False
        self.timer.cancel()
        self.root.destroy()


root = tk.Tk()
pong = Pong(root, WIDTH, HEIGHT, MARGIN)

root.bind("<KeyPress>", pong.keypress)
root.bind("<KeyRelease>", pong.keyrelease)

root.wm_protocol("WM_DELETE_WINDOW", pong.killtimer)
root.mainloop()