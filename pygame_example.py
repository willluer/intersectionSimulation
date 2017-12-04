import pygame as pg
import time
from enum import Enum
from random import randint


BACKGROUND_COLOR = pg.Color("slategray")
Direction = Enum('Direction', 'North South East West')
Traffic_Signal = Enum('Traffic_Signal', 'Green Yellow Red')
w = 600
h = 600
laneW = 50

total_collisions = 0
total_cars = 0
car_pos = []


def debug_text(main_surface, text_list):
    main_surface.fill(BACKGROUND_COLOR)
    for i in range(0, len(text_list)):
        main_surface.blit(font.render(
            str(text_list[i]), True, (0, 0, 255)), (10, 10 + (10 * i)))


class Car(pg.sprite.Sprite):
    def __init__(self, dir, *groups):
        if dir == Direction.North:
            x, y = int(w / 2 + laneW / 2), h
        elif dir == Direction.South:
            x, y = int(w / 2 - laneW / 2), 0
        elif dir == Direction.East:
            x, y = 0, int(h / 2 + laneW / 2)
        elif dir == Direction.West:
            x, y = w, int(h / 2 - laneW / 2)

        super(Car, self).__init__(*groups)
        self.image = pg.Surface((20, 20)).convert_alpha()
        self.image.fill((255, 0, 0))
        self.rect = pg.Rect(x, y, 20, 20)

        self.dir = dir
        self.remove = False
        self.at_light = False

    def at_intersection(self):
        at_intersection = False

        northward_stop = h / 2 - laneW / 2
        southward_stop = h / 2 + laneW / 2
        eastward_stop = w / 2 - laneW / 2
        westward_stop = w / 2 + laneW / 2

        if self.dir == Direction.North:
            if self.rect.y > (northward_stop + 20) and \
                    self.rect.y < (northward_stop + 25):
                at_intersection = True
        elif self.dir == Direction.South:
            if self.rect.y > (southward_stop - 25) and \
                    self.rect.y < (southward_stop - 20):
                at_intersection = True
        elif self.dir == Direction.East:
            if self.rect.x > (eastward_stop - 25) and \
                    self.rect.x < (eastward_stop - 20):
                at_intersection = True
        elif self.dir == Direction.West:
            if self.rect.x > (westward_stop + 20) and \
                    self.rect.x < (westward_stop + 25):
                at_intersection = True

        return at_intersection

    def update_position(self, light):
        # if at a red light, don't move
        if (self.at_light or self.at_intersection()) and \
                light == Traffic_Signal.Red:
            # set at_light so we don't have to check
            # at_intersection() every frame
            self.at_light = True
        else:
            # check if the car is on screen
            if (self.rect.x >= 0 and self.rect.x <= w and
                    self.rect.y >= 0 and self.rect.y <= h):
                if self.dir == Direction.North:
                    self.rect.y -= 2
                elif self.dir == Direction.South:
                    self.rect.y += 2
                elif self.dir == Direction.East:
                    self.rect.x += 2
                elif self.dir == Direction.West:
                    self.rect.x -= 2
            # remove off screen cars
            else:
                self.remove = True
            self.at_light = False

    def draw(self, surface):
        self.rect = self.rect.clamp(surface.get_rect())
        surface.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.cooldown = 0
        self.screen = pg.display.set_mode((w, h))
        self.cars = pg.sprite.Group()

        self.done = False
        self.fps = 60.0
        self.clock = pg.time.Clock()

        self.green_lights = [Direction.North, Direction.East]

    def event_loop(self):
        global total_cars
        # every 5th frame have a chance at adding a car
        self.cooldown = (self.cooldown + 1) % 5

        if self.cooldown == 0:
            add_car = randint(0, 10)
            if add_car == 0:
                Car(Direction.North, self.cars)
                total_cars += 1
            elif add_car == 1:
                Car(Direction.South, self.cars)
                total_cars += 1
            elif add_car == 2:
                Car(Direction.East, self.cars)
                total_cars += 1
            elif add_car == 3:
                Car(Direction.West, self.cars)
                total_cars += 1

        global car_pos
        car_pos = []
        removed = []
        for car in self.cars:
            # check for green light in the direction this car is travelling
            if car.dir in self.green_lights:
                light = Traffic_Signal.Green
            else:
                light = Traffic_Signal.Red
            # move
            car.update_position(light)

            # if we should remove the car add it to the list
            if car.remove:
                removed.append(car)
            # otherwise track its location
            else:
                car_pos.append((car.rect.x, car.rect.y))
        # remove all the cars in removed
        for car in removed:
            car.kill()
            car.image.fill(BACKGROUND_COLOR)

        for event in pg.event.get():
            # if the user hit the 'X'
            if event.type == pg.QUIT:
                self.done = True

    def check_collide(self):
        global total_collisions
        collision = False
        # check all the cars for collisions
        for car in self.cars:
            # ignore cars already marked for removal
            if not car.remove:
                # returns a list of the cars in self.cars
                # that collided with car _including_ car
                colliders = pg.sprite.spritecollide(car, self.cars, False)
                # car will always collide with itself, so check
                # for more than 1 collision
                if len(colliders) > 1:
                    total_collisions += 1
                    collision = True
                    # mark the car for removal
                    car.remove = True
                    # mark the other cars involved in the collsion for removal
                    for other in colliders:
                        other.remove = True

        if collision:
            pg.display.set_caption('Collision')
        else:
            pg.display.set_caption('No Collide')

    def draw(self):
        elapsed = int(time.time() - start_time)

        self.screen.fill(BACKGROUND_COLOR)

        collisions_str = "Collisions: {}".format(total_collisions)
        total_cars_str = "Total Cars: {}".format(total_cars)
        time_str = "Time        : {}".format(elapsed)

        debug_text(self.screen, [collisions_str,
                                 total_cars_str, time_str] + car_pos)
        self.cars.draw(self.screen)

    def run(self):
        while not self.done:
            self.event_loop()
            self.check_collide()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    global start_time
    pg.init()
    font = pg.font.Font(None, 15)
    game = Game()
    start_time = time.time()
    game.run()

pg.quit()
