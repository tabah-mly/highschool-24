import pygame


class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def follow(self, target_rect):
        self.offset.x = target_rect.centerx - self.width // 2
        # self.offset.y = target_rect.centery

    def apply(self, target):
        if isinstance(target, pygame.Rect):
            return target.move(-self.offset.x, -self.offset.y)
        else:
            return (target[0] - self.offset.x, target[1] - self.offset.y)
