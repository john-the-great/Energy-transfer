from email.mime import base
import pygame, sys
from pygame.locals import *
pygame.init()

class Object:
    def __init__(self, pos, size, vels, type):
        self.type = type
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.false_pos = [self.rect.x, self.rect.y]
        self.vels = vels

    def render(self, surf):
        pygame.draw.rect(
            surf, (255, 255, 255), self.rect, 1
        )

    def test_hit(self, objects):
        hit_list = []
        for id, obj in enumerate(objects):
            if obj.rect != self.rect:
                if obj.rect.colliderect(self.rect):
                    hit_list.append(obj)
        return hit_list

    def colli(self, objects, dt):
        self.false_pos[0] += self.vels[0] * dt
        self.rect.x = self.false_pos[0]
        hit_list = self.test_hit(objects)
        colli_dis = 3
        for obj in hit_list:
            if self.vels[0] > 0:
                if abs(self.rect.right - obj.rect.left) < colli_dis:
                    self.rect.right = obj.rect.left
                    obj.vels[0] = self.vels[0] * .75
                    self.vels[0] = (self.vels[0] * .35) * -1
                    #y
                    obj.vels[1] += self.vels[1] * .20
            elif self.vels[0] < 0:
                if abs(self.rect.left - obj.rect.right) < colli_dis:
                    self.rect.left = obj.rect.right
                    obj.vels[0] = self.vels[0] * .75
                    self.vels[0] = (self.vels[0] * .35) * -1
                    #y
                    obj.vels[1] += self.vels[1] * .20

        self.false_pos[1] += self.vels[1] * dt
        self.rect.y = self.false_pos[1]
        hit_list = self.test_hit(objects)
        colli_dis = 3
        for obj in hit_list:
            if self.vels[1] > 0:
                if abs(self.rect.bottom - obj.rect.top) < colli_dis:
                    self.rect.bottom = obj.rect.top
                    obj.vels[1] = self.vels[1] * .75
                    self.vels[1] = (self.vels[1] * .35) * -1
                    #x
                    obj.vels[0] += self.vels[0] * .20
            elif self.vels[1] < 0:
                if abs(self.rect.top - obj.rect.bottom) < colli_dis:
                    self.rect.top = obj.rect.bottom
                    obj.vels[1] = self.vels[1] * .75
                    self.vels[1] = (self.vels[1] * .35) * -1
                    #x
                    obj.vels[0] += self.vels[0] * .20

def main():
    WINDOW_SIZE = (600, 600)
    window = pygame.display.set_mode(WINDOW_SIZE)

    clock = pygame.time.Clock()

    xdens = 10
    ydens = 10
    object_size = 10
    base_size = 10
    base_x = ((WINDOW_SIZE[0]/2)-(object_size/2))-(xdens*object_size)/2
    base_y = ((WINDOW_SIZE[1]/2)-(object_size/2))-(ydens*object_size)/2
    x, y = base_x, base_y
    objects = []
    type = 0
    offsetx = 0
    offsety = 0
    for i in range(xdens):
        for j in range(ydens):
            obj = Object([x+(object_size)+offsetx, y+(object_size)+offsety], base_size, [0, 0], type)
            objects.append(obj)
            type += 1
            x += base_size + 3
        y += base_size + 3
        x = base_x

    moving_obj = Object([0, 0], base_size, [3, 3], type+1)
    objects.append(moving_obj)

    while 1:
        dt = clock.tick(10_000) * .001 * 60
        window.fill((0, 0, 0))

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        objects[len(objects)-1].colli(objects, dt)
        for obj in objects:
            obj.colli(objects, dt)
            obj.render(window)

        pygame.display.update()


if __name__ == '__main__':
    main()