import pygame, sys
from pygame.locals import *
pygame.init()

class Object:
    def __init__(self, pos, size, vels):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        self.false_pos = [self.rect.x, self.rect.y]
        self.vels = vels

    def render(self, surf):
        pygame.draw.rect(
            surf, (255, 255, 255), self.rect, 1
        )

    def test_hit(self, objects):
        hit_list = []
        for obj in objects:
            if obj.rect != self.rect:
                if obj.rect.colliderect(self.rect):
                    hit_list.append((obj.rect, obj.vels))
        return hit_list

    def colli(self, objects, dt):

        self.false_pos[0] += self.vels[0] * dt
        self.rect.x = self.false_pos[0]
        hit_list = self.test_hit(objects)
        for rect in hit_list:
            if self.vels[0] > 0 or self.vels[0] < 0:
                self.vels[0] = (rect[1][0] * .75) * -1

        self.false_pos[1] += self.vels[1] * dt
        self.rect.y = self.false_pos[1]
        hit_list = self.test_hit(objects)
        for rect in hit_list:
            if self.vels[1] > 0 or self.vels[1] < 0:
                self.vels[1] = (rect[1][1] * .75) * -1

def main():
    WINDOW_SIZE = (600, 600)
    window = pygame.display.set_mode(WINDOW_SIZE)

    clock = pygame.time.Clock()

    xdens = 10
    ydens = 10
    object_size = 10
    x = ((WINDOW_SIZE[0]/2)-(object_size/2))-(xdens*object_size)/2
    y = ((WINDOW_SIZE[1]/2)-(object_size/2))-(ydens*object_size)/2
    objects = []
    for i in range(xdens):
        for j in range(ydens):
            obj = Object([x+(object_size*i), y+(object_size*j)], object_size, [0, 0])
            objects.append(obj)

    moving_obj = Object([0, 0], object_size, [3, 3])
    objects.append(moving_obj)

    while 1:
        dt = clock.tick(10_000) * .001 * 60
        window.fill((0, 0, 0))

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        for obj in objects:
            obj.colli(objects, dt)
            obj.render(window)

        pygame.display.update()

if __name__ == '__main__':
    main()