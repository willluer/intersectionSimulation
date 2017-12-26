import pygame as pg
from global_vars import BACKGROUND_COLOR, Direction, Traffic_Signal, \
    h, w, laneW


class Car(pg.sprite.Sprite):
    def __init__(self, dir, x, y, *groups):
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
            if self.rect.y > (northward_stop + 65) and \
                    self.rect.y < (northward_stop + 70):
                at_intersection = True
        elif self.dir == Direction.South:
            if self.rect.y > (southward_stop - 70) and \
                    self.rect.y < (southward_stop - 65):
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

    def update_position(self, cars, light):
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

                    if len(pg.sprite.spritecollide(self, cars, False)) > 1:
                        self.rect.y += 2
                elif self.dir == Direction.South:
                    self.rect.y += 2

                    if len(pg.sprite.spritecollide(self, cars, False)) > 1:
                        self.rect.y -= 2
                elif self.dir == Direction.East:
                    self.rect.x += 2

                    if len(pg.sprite.spritecollide(self, cars, False)) > 1:
                        self.rect.x -= 2
                elif self.dir == Direction.West:
                    self.rect.x -= 2

                    if len(pg.sprite.spritecollide(self, cars, False)) > 1:
                        self.rect.x += 2
            # remove off screen cars
            else:
                self.kill()
                self.image.fill(BACKGROUND_COLOR)
            self.at_light = False

    def draw(self, surface):
        self.rect = self.rect.clamp(surface.get_rect())
        surface.blit(self.image, self.rect)
