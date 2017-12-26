from enum import Enum
import pygame as pg


global BACKGROUND_COLOR
global Direction, Traffic_Signal
global w, h, laneW

BACKGROUND_COLOR = pg.Color("slategray")
Direction = Enum('Direction', 'North South East West')
Traffic_Signal = Enum('Traffic_Signal', 'Green Yellow Red')
w = 600
h = 600
laneW = 45
