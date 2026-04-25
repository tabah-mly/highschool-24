import pygame


class EnemyBase:
    def initialize(self, x, y, player):
        self.player = player
        self.state = "idle"
        self.facing_right = True
        self.moving = True
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))
        self.offset = 100

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def move(self, dt):
        self.facing_right = self.player.rect.centerx > self.rect.centerx
        self.moving = abs(self.player.rect.centerx - self.rect.centerx) > 100

        if self.moving:
            self.set_state("walk")
            direction_x = 1 if self.facing_right else -1
            self.pos.x += direction_x * self.stats["speed"] * dt
        else:
            self.set_state("idle")

        self.rect.center = self.pos

    def update_sprites(self, dt):
        self.animator.update(dt)

    def draw_sprites(self, screen, camera):
        image = self.animator.image

        # print(f"Player: {self.player.rect.centerx} \t Enemy: {self.rect.centerx}")
        # print(f"Player: {self.player.rect} \t Enemy: {self.rect}")

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        player_rect = camera.apply(self.rect)
        screen.blit(image, player_rect)
