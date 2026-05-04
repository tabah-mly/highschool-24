import pygame


class PlayerBase:
    def initialize(self, x, y):
        self.state = "idle"
        self.facing_right = True
        self.is_run = False
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))
        self.hurtbox = pygame.Rect(0, 0, 100, 200)
        self.hurtbox.center = self.rect.center
        self.has_hit = False
        self.dead = False
        self.debug = False
        self.speed = 0
        self.font = pygame.font.Font("assets/fonts/monogram.ttf", 60)
        self.attack_clicked = False

    def take_damage(self, amount):
        self.stats["hp"] -= amount
        if self.stats["hp"] <= 0:
            self.dead = True

    def get_hitbox(self):
        width = 100
        height = 100
        x_offset = -120
        y_offset = -20

        y = self.rect.centery - (height // 2) + y_offset
        if self.facing_right:
            x = self.rect.right + x_offset
        else:
            x = self.rect.left - width - x_offset

        return pygame.Rect(x, y, width, height)

    def do_damage(self, enemies):
        attack_rect = self.get_hitbox()

        for enemy in enemies:
            if attack_rect.colliderect(enemy.hurtbox):
                enemy.take_damage(self.stats["damage"])

    def handle_attack(self, enemies):
        mouse_pressed = self.attack_clicked
        self.attack_clicked = False

        if mouse_pressed and self.state != "attack":
            self.set_state("attack")
            self.has_hit = False

        if self.state == "attack" and not self.has_hit:
            if self.animator.frame_index == 3:
                self.do_damage(enemies)
                self.has_hit = True

        if self.state == "attack" and self.animator.finished:
            self.set_state("idle")

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def update_sprites(self, dt):
        self.animator.update(dt)

    def draw_sprites(self, screen, camera):
        image = self.animator.image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        rect = camera.apply(self.rect)
        screen.blit(image, rect)

        if self.debug:
            text_surface = self.font.render(f"{self.stats['hp']}", True, (0, 0, 255))
            text_rect = text_surface.get_rect(center=(rect.x + 130, rect.y - 222))
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.get_hitbox()), 2)
            pygame.draw.rect(screen, (0, 0, 255), camera.apply(self.hurtbox), 2)

    def check_run(self, keys):
        if keys[pygame.K_LSHIFT]:
            self.speed = self.stats["run"]
            self.is_run = True
        else:
            self.speed = self.stats["walk"]
            self.is_run = False

    def move(self, keys, direction, dt):
        self.check_run(keys)
        if self.state == "attack":
            return

        if direction.length_squared() > 0:
            direction = direction.normalize()

            if direction[0] < 0:
                self.facing_right = False
            else:
                self.facing_right = True

            self.pos += direction * self.speed * dt
            self.rect.center = self.pos
            self.hurtbox.center = self.rect.center
            self.set_state("run" if self.is_run else "walk")
        else:
            self.set_state("idle")
