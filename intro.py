import tkinter as tk
import time
import random
import math

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

def appendLists(b, xV, yV, xP, yP):
    ballList.append(b)
    xVel.append(xVelTemp)
    yVel.append(yVelTemp)
    xPos.append(xPosTemp)
    yPos.append(yPosTemp)

def deleteOldBall(b):
    i = ballList.index(b)
    #print("Removing Index: ", i)
    #print("Length of ballList: ", len(ballList))
    #print("ballList: ", ballList)
    canvas.delete(b)
    del ballList[i]
    del xVel[i]
    del yVel[i]
    del xPos[i]
    del yPos[i]

def checkCollision(x1,x2,y1,y2):
    if 6*r > math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)):
        return 1
    else:
        return 0

def checkCollision2(b1,b2):
    pos = canvas.coords(b1)
    pos2 = canvas.coords(b2)
    x1 = (pos[0]+pos[2])/2
    y1 = (pos[1]+pos[3])/2
    x2 = (pos2[0]+pos2[2])/2
    y2 = (pos[1]+pos2[3])/2

    if 2*r > math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)):
        canvas.create_circle(x1, y1, r, fill="red", width=0)
        print("Crash, removing balls: ", b1,b2)
        deleteOldBall(b1)
        deleteOldBall(b2)

        return 1
    else:
        return 0

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
    create = random.randint(1, 10)
    return create, xPosTemp, yPosTemp, xVelTemp, yVelTemp


r = 5
laneW = 50
xVel = []
yVel = []
xPos = []
yPos = []
ballList = []
collisionCount = 0

streets = canvas.draw_streets(laneW)
s = '# balls: %i \n# crashes: %i' % (len(ballList) , 100)
text = canvas.create_text(100, 100, text = s)
startTime = time.time()

while True:
    #UPDATE TEXT DISPLAY
    s = '    Number of balls: %i \n\
    Number of collisions: %i \n\
    Time(s): %i' \
    % (len(ballList) , collisionCount, time.time() - startTime)
    canvas.itemconfig(text, text = s)

    #CREATE RANDOM AGENT
    create, xPosTemp, yPosTemp, xVelTemp, yVelTemp = randomAgent()

    # MAKE ALL SAME SPEED (not necessary but simplifies problem)
    if xVelTemp > 0:
        xVelTemp = 4
    if xVelTemp < 0:
        xVelTemp = -4
    if yVelTemp > 0:
        yVelTemp = 4
    if yVelTemp < 0:
        yVelTemp = -4

    #DRAW NEW CIRCLE
    if create == 1:
        if len(ballList) == 0: #if no balls yet just draw it
            newBall = canvas.create_circle(xPosTemp, yPosTemp, r, fill="green", width=0)
            appendLists(newBall, xVelTemp, yVelTemp, xPosTemp, yPosTemp)
            #print("First ball added", newBall)

        else:
            add = True
            for oldBall in ballList:
                pos = canvas.coords(oldBall)
                x = (pos[0]+pos[2])/2
                y = (pos[1]+pos[3])/2
                if checkCollision(x,xPosTemp,y,yPosTemp) == 1:
                    add = False
            if(add):
                newBall = canvas.create_circle(xPosTemp, yPosTemp, r, fill="green", width=0)
                appendLists(newBall, xVelTemp, yVelTemp, xPosTemp, yPosTemp)
                #print("New ball added", newBall)
    i = 0
    for b, xV, yV in zip(ballList, xVel, yVel):
        #CHECK FOR COLLISIONS
        j = i+1
        while j < len(ballList):
            b2 = ballList[j]
            val = checkCollision2(b, b2)
            collisionCount = collisionCount + val
            if val == 1:
                break;
            j = j + 1

        #UPDATE LOCATION
        canvas.move(b, xV, yV)

        # DELETE OLD BALLS
        pos = canvas.coords(b)
        if len(pos) == 4:
            if pos[0] < -10 or pos[1] < -10 or pos[2] > w + 10 or pos[3] > h + 10:
                # print "should delete: ", pos
                deleteOldBall(b)
        i = i + 1

    canvas.bind("<Button-1>", callback)
    root.update()
    time.sleep(0.001)
root.mainloop()
