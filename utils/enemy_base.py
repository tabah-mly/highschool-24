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
        self.offset = 150

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def move(self, dt):
        self.facing_right = (self.player.rect.centerx - self.rect.centerx) > 0

        if self.facing_right:
            target_x = self.player.rect.centerx - self.offset
        else:
            target_x = self.player.rect.centerx + self.offset

        distance_to_target = target_x - self.rect.centerx
        self.moving = abs(distance_to_target) > 1

        if self.moving:
            move_dir = 1 if distance_to_target > 0 else -1
            facing_dir = 1 if self.facing_right else -1
            is_moving_backward = move_dir != facing_dir

            if is_moving_backward:
                self.set_state("idle")
            else:
                self.set_state("walk")

            self.pos.x += move_dir * self.stats["speed"] * dt
        else:
            self.set_state("idle")

        self.rect.center = self.pos

    def update_sprites(self, dt):
        self.animator.update(dt)

    def draw_sprites(self, screen, camera):
        image = self.animator.image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        player_rect = camera.apply(self.rect)
        screen.blit(image, player_rect)
