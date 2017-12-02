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

def appendLists(b, xV, yV, xP, yP):
    ballList.append(b)
    xVel.append(xVelTemp)
    yVel.append(yVelTemp)
    xPos.append(xPosTemp)
    yPos.append(yPosTemp)

def deleteOldBall(i):
    print("Removing Index: ", i)
    print("Length of ballList: ", len(ballList))
    del ballList[i]
    del xVel[i]
    del yVel[i]
    del xPos[i]
    del yPos[i]

#def checkCollision():
#    if

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
xVel = []
yVel = []
xPos = []
yPos = []
ballList = []
crashCount = 0

streets = canvas.draw_streets(laneW)
s = '# balls: %i \n# crashes: %i' % (len(ballList) , 100)
text = canvas.create_text(100, 100, text = s)
startTime = time.time()

while True:
    s = '    Number of balls: %i \n\
    Number of collisions: %i \n\
    Time(s): %i' \
    % (len(ballList) , 100, time.time() - startTime)

    canvas.itemconfig(text, text = s)
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

    #DRAW NEW CIRCLE
    if create == 1:
        # print "created"
        b = canvas.create_circle(xPosTemp, yPosTemp, r, fill="green", width=0)
        appendLists(b, xVelTemp, yVelTemp, xPosTemp, yPosTemp)

    i = 0
    for b, xV, yV in zip(ballList, xVel, yVel):
        #for b2, xP2, yP2
    #        if b.coords
        canvas.move(b, xV, yV)

        # DELETE OLD BALLS
        pos = canvas.coords(b)
        if len(pos) == 4:
            if pos[0] < -10 or pos[1] < -10 or pos[2] > w + 10 or pos[3] > h + 10:
                # print "should delete: ", pos
                canvas.delete(b)
                deleteOldBall(i)
        i = i + 1
    canvas.bind("<Button-1>", callback)
    root.update()
    time.sleep(0.01)
root.mainloop()
