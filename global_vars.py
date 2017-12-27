from enum import Enum
import pygame as pg


BACKGROUND_COLOR = pg.Color("slategray")
Direction = Enum('Direction', 'North South East West')
Traffic_Signal = Enum('Traffic_Signal', 'Green Yellow Red')
w = 600
h = 600
laneW = 45


current_cars = 0
