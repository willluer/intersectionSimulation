import tkinter as tk
import time
import random

root = tk.Tk()
w = 600
h = 600
canvas = tk.Canvas(root, width=w, height=h, borderwidth=0,
                   highlightthickness=0, bg="gray")
canvas.grid()


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tk.Canvas.create_circle = _create_circle


def callback(event):
    print("xVel: ", xVel)
    print("xVel len: ", len(xVel))
    print("xVel: ", yVel)
    print("xVel len: ", len(yVel))
    print("Ball List: ", ballList)
    print("Ball List Len: ", len(ballList))
    print(len(xVel) == len(yVel) and len(xVel) == len(ballList))

    for i in range(len(xVel)):
        if yVel == 0 and xVel == 0:
            print("")
            print("STATIONARY POINT")
            print("")


def _draw_streets(self, laneWidth):
    # vertical lane
    self.create_line(w / 2 - laneWidth, h, w / 2 - laneWidth,
                     h / 2 + laneWidth, fill="black", width=4)
    self.create_line(w / 2 + laneWidth, h, w / 2 + laneWidth,
                     h / 2 + laneWidth, fill="black", width=4)
    self.create_line(w / 2 - laneWidth, 0, w / 2 - laneWidth,
                     h / 2 - laneWidth, fill="black", width=4)
    self.create_line(w / 2 + laneWidth, 0, w / 2 + laneWidth,
                     h / 2 - laneWidth, fill="black", width=4)
    self.create_line(w / 2, 0, w / 2, h / 2 - laneWidth,
                     fill="yellow", width=2, dash=(8, 16))
    self.create_line(w / 2, h / 2 + laneWidth, w / 2, h,
                     fill="yellow", width=2, dash=(8, 16))
    # horizontal lane
    self.create_line(0, h / 2 - laneWidth, w / 2 - laneWidth,
                     h / 2 - laneWidth, fill="black", width=4)
    self.create_line(0, h / 2 + laneWidth, w / 2 - laneWidth,
                     h / 2 + laneWidth, fill="black", width=4)
    self.create_line(w / 2 + laneWidth, h / 2 - laneWidth, w,
                     h / 2 - laneWidth, fill="black", width=4)
    self.create_line(w / 2 + laneWidth, h / 2 + laneWidth, w,
                     h / 2 + laneWidth, fill="black", width=4)
    self.create_line(0, h / 2, w / 2 - laneWidth, h / 2,
                     fill="yellow", width=2, dash=(8, 16))
    self.create_line(w / 2 + laneWidth, h / 2, w, h / 2,
                     fill="yellow", width=2, dash=(8, 16))


tk.Canvas.draw_streets = _draw_streets


def _moveCircle(self, item, x, y):
    print(self.coords(item))
    self.coords(item)[0] = self.coords(item)[0] + x
    self.coords(item)[2] = self.coords(item)[2] + x
    self.coords(item)[1] = self.coords(item)[1] + y
    self.coords(item)[3] = self.coords(item)[3] + y
    print(self.coords(item))


tk.Canvas.moveCircle = _moveCircle


def randomAgent():
    # Randomly generate agents
    start = random.randint(1, 4)
    magnitude = random.randint(1, 4)

    if start == 1:
        xPosTemp = w / 2 + laneW / 2
        yPosTemp = h
        yVelTemp = -magnitude
        xVelTemp = 0
    elif start == 2:
        xPosTemp = w / 2 - laneW / 2
        yPosTemp = 0
        yVelTemp = magnitude
        xVelTemp = 0
    elif start == 3:
        xPosTemp = 0
        yPosTemp = h / 2 + laneW / 2
        yVelTemp = 0
        xVelTemp = magnitude
    else:
        xPosTemp = w
        yPosTemp = h / 2 - laneW / 2
        yVelTemp = 0
        xVelTemp = -magnitude

    # Create agent 5% of the time
    create = random.randint(1, 20)
    return create, xPosTemp, yPosTemp, xVelTemp, yVelTemp


r = 5
laneW = 50
canvas.draw_streets(laneW)

xVel = []
yVel = []
ballList = []

# ball = canvas.create_circle(0, h/2-laneW/2, r, fill="green", width=0)

while True:
    create, xPosTemp, yPosTemp, xVelTemp, yVelTemp = randomAgent()
    # print randomAgent()
    # MAKE ALL SAME SPEED
    if xVelTemp > 0:
        xVelTemp = 2
    if xVelTemp < 0:
        xVelTemp = -2
    if yVelTemp > 0:
        yVelTemp = 2
    if yVelTemp < 0:
        yVelTemp = -2

    if create == 1:
        # print "created"
        b = canvas.create_circle(xPosTemp, yPosTemp, r, fill="green", width=0)
        # print b
        ballList.append(b)
        xVel.append(xVelTemp)
        yVel.append(yVelTemp)

    i = 0
    for b, xV, yV in zip(ballList, xVel, yVel):
        canvas.move(b, xV, yV)

        # DELETE OLD BALLS
        # if len(ballList) % 5 == 0:
        #    print "Number of balls in list: ", len(ballList)
        pos = canvas.coords(b)

        if len(pos) == 4:
            if (pos[0] < -10 or pos[1] < -10 or
                pos[2] > w + 10 or pos[3] > h + 10):
                # print "should delete: ", pos
                canvas.delete(b)
                print("Removing Index: ", i)
                print("Length of ballList: ", len(ballList))
                del ballList[i]
                del xVel[i]
                del yVel[i]
            # Stop Right bound cars at intersection
            elif pos[0] < .4 * w and pos[0] > .39 * w:
                xVel[i] = 0
                yVel[i] = 0
            # Stop Left bound cars at intersection
            elif pos[0] > .59 * w and pos[0] < .6 * w:
                xVel[i] = 0
                yVel[i] = 0

        i = i + 1

    canvas.bind("<Button-1>", callback)
    root.update()
    time.sleep(0.01)
root.mainloop()
