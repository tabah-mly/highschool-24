import pygame


class Finish:
    def __init__(self, screen_height, pos_x):
        image_path = "assets/imgs/finish.png"
        original = pygame.image.load(image_path).convert_alpha()
        if screen_height > 0:
            scale = screen_height / original.get_height()

        self.image = pygame.transform.scale(
            original, (original.get_width() * scale, original.get_height() * scale)
        )

        self.w = self.image.get_width()
        self.h = self.image.get_height()

        self.offset = self.w // 2

        self.finish_rect = pygame.Rect(0, 0, 300, self.h * 0.8)

        self.debug = False

        self.on_right = pos_x > 0
        if not self.on_right:
            pos_x -= self.w
            self.image = pygame.transform.flip(self.image, True, False)
        self.pos = (pos_x, 0)

    def update(self):
        self.finish_rect.centerx = self.pos[0] + self.offset
        self.finish_rect.centery = self.pos[1] + self.h // 2

    def draw(self, surface, camera):
        screen_pos = camera.apply(self.pos)
        surface.blit(self.image, screen_pos)

        if self.debug:
            pygame.draw.rect(
                surface, (255, 255, 255), camera.apply(self.finish_rect), 2
            )

    def is_finish(self, player):
        return self.finish_rect.colliderect(player.hurtbox)
