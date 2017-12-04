import pygame as pg
from enum import Enum
from random import randint


BACKGROUND_COLOR = pg.Color("slategray")
Direction = Enum('Direction', 'North South East West')
w = 600
h = 600
laneW = 50

total_collisions = 0
car_pos = []


def debug_text(main_surface, text_list):
    main_surface.fill(BACKGROUND_COLOR)
    for i in range(0, len(text_list)):
        main_surface.blit(font.render(
            str(text_list[i]), True, (255, 0, 0)), (10, 10 + (10 * i)))


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
        self.moving = True

    def update_position(self):
        if self.moving:
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
            else:
                self.moving = False

    def draw(self, surface):
        self.rect = self.rect.clamp(surface.get_rect())
        pg.display.draw.circle(self.image, (0, 0, 255),
                               (self.rect.x, self.rect.y), 10, 0)
        surface.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.cooldown = 0
        self.screen = pg.display.set_mode((w, h))
        self.cars = pg.sprite.Group()

        Car(Direction.North, self.cars)

        self.done = False
        self.fps = 60.0
        self.clock = pg.time.Clock()

    def event_loop(self):
        self.cooldown = (self.cooldown + 1) % 5

        if self.cooldown == 0:
            add_car = randint(0, 20)
            if add_car == 0:
                Car(Direction.North, self.cars)
            elif add_car == 1:
                Car(Direction.South, self.cars)
            elif add_car == 2:
                Car(Direction.East, self.cars)
            elif add_car == 3:
                Car(Direction.West, self.cars)

        global car_pos
        car_pos = []
        removed = []
        for car in self.cars:
            car.update_position()
            if not car.moving:
                removed.append(car)
            else:
                car_pos.append((car.rect.x, car.rect.y))
        for car in removed:
            car.kill()
            car.image.fill(BACKGROUND_COLOR)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def check_collide(self):
        global total_collisions
        collision = False
        for car in self.cars:
            if car.moving:
                colliders = pg.sprite.spritecollide(car, self.cars, False)
                if len(colliders) > 1:
                    total_collisions += 1
                    collision = True
                    car.moving = False
                    for other in colliders:
                        other.moving = False

        if collision:
            pg.display.set_caption('collide')
        else:
            pg.display.set_caption('do not collide')

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        debug_text(self.screen, ["Collisions: {0}".format(
            total_collisions)] + car_pos)
        self.cars.draw(self.screen)

    def run(self):
        while not self.done:
            self.event_loop()
            self.check_collide()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    pg.init()
    font = pg.font.Font(None, 20)
    game = Game()
    game.run()

pg.quit()
