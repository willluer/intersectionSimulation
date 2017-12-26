import pygame as pg
import time
from random import randint

from global_vars import BACKGROUND_COLOR, Direction, Traffic_Signal, \
    h, w, laneW
from Car import Car

# WRL next steps
# 1. Add current number of cars on the screen
# 2. Add stoplight graphic to frame so we can see who is supposed to stoplight
# 4. Stop all cars in lane at red light
# 5. Research adjusting sprite speed
# 6. For AI we will need:
# - Car positions
# - Car velocity
# - Number of collisions
# - Time taken for each car to cross (so AI doesn't just stop
# two lanes of traffic the whole time)

total_collisions = 0
total_cars = 0
car_pos = []


def debug_text(main_surface, text_list):
    main_surface.fill(BACKGROUND_COLOR)
    for i in range(0, len(text_list)):
        main_surface.blit(font.render(
            str(text_list[i]), True, (0, 0, 255)), (10, 10 + (10 * i)))


class Game:

    def __init__(self):
        self.cooldown = 0
        self.light_change = 0

        self.screen = pg.display.set_mode((w, h))
        self.cars = pg.sprite.Group()

        self.done = False
        self.fps = 60.0
        self.clock = pg.time.Clock()

        self.green_lights = [Direction.North, Direction.South,
                             Direction.East, Direction.West]

    def event_loop(self):
        global total_cars
        # every 5th frame have a chance at adding a car
        self.cooldown = (self.cooldown + 1) % 5

        # every 20 frames, change lights
        self.light_change = (self.light_change + 1) % 150

        if self.cooldown == 0:
            add_car = randint(0, 10)
            newCar = None

            if add_car == 0:
                newCar = Car(Direction.North, int(
                    w / 2 + laneW / 2), h, self.cars)
                total_cars += 1
            elif add_car == 1:
                newCar = Car(Direction.South, int(
                    w / 2 - laneW / 2), 0, self.cars)
                total_cars += 1
            elif add_car == 2:
                newCar = Car(Direction.East, 0, int(
                    h / 2 + laneW / 2), self.cars)
                total_cars += 1
            elif add_car == 3:
                newCar = Car(Direction.West, w, int(
                    h / 2 - laneW / 2), self.cars)
                total_cars += 1
            # If the newCar would collide, don't add it
            if newCar is not None and \
                    len(pg.sprite.spritecollide(newCar, self.cars, False)) > 1:
                newCar.kill()
                newCar.image.fill(BACKGROUND_COLOR)
                total_cars -= 1

        if self.light_change < 40:
            self.green_lights = [Direction.North, Direction.South]
        elif self.light_change < 80:
            self.green_lights = []
        elif self.light_change < 120:
            self.green_lights = [Direction.East, Direction.West]
        else:
            self.green_lights = []

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
            car.update_position(self.cars, light)

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

                    # mark the cars involved in the collsion for removal
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
