import pygame, random
from utils.spritesheet import SpriteSheet


class EnemyBase:
    shared_animations = None

    def initialize(self, x, y, player):
        if EnemyBase.shared_animations is None:
            _anim_temp = {}
            for key in self.animations:
                _is_loop = True if len(self.animations[key]) < 4 else False
                _anim_temp[key] = SpriteSheet(
                    self.animations[key][0],
                    self.animations[key][1],
                    self.animations[key][2],
                    _is_loop,
                )
            EnemyBase.shared_animations = _anim_temp

        self.animations = {
            key: anim.copy() for key, anim in EnemyBase.shared_animations.items()
        }

        self.player = player
        self.state = "idle"
        self.facing_right = True
        self.moving = True
        self.animator = self.animations[self.state]
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(center=(x, y))
        self.hurtbox = pygame.Rect(0, 0, 120, 250)
        self.hurtbox.center = self.rect.center
        self.chase_offset = 120
        self.attack_range = random.randint(50, 150)
        self.attack_timer = 0
        self.has_hit = False
        self.dead = False
        self.debug = False
        self.font = pygame.font.Font("assets/fonts/monogram.ttf", 60)
        self.attack_cooldown = 0.5

    def take_damage(self, amount):
        self.stats["hp"] -= amount
        if self.stats["hp"] <= 0:
            self.dead = True

    def get_hitbox(self):
        width = 200
        height = 200
        x_offset = -280
        y_offset = 10

        y = self.rect.centery - (height // 2) + y_offset
        if self.facing_right:
            x = self.rect.right + x_offset
        else:
            x = self.rect.left - width - x_offset

        return pygame.Rect(x, y, width, height)

    def do_damage(self):
        attack_rect = self.get_hitbox()

        if attack_rect.colliderect(self.player.hurtbox):
            self.player.take_damage(self.stats["damage"])

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def get_target_x(self):
        self.facing_right = self.player.rect.centerx - self.rect.centerx > 0
        if self.facing_right:
            self.target_x = self.player.rect.centerx - self.chase_offset
        else:
            self.target_x = self.player.rect.centerx + self.chase_offset

    def attack(self, dt):
        distance = abs(self.target_x - self.rect.centerx)

        if self.attack_timer > 0:
            self.attack_timer -= dt

        if self.state == "attack":
            if distance > self.attack_range:
                self.set_state("idle")
                return

            if not self.has_hit and self.animator.frame_index == 4:
                self.do_damage()
                self.has_hit = True

            if self.animator.finished:
                self.set_state("idle")
            return True

        if distance <= self.attack_range and self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown
            self.has_hit = False
            self.set_state("attack")
            return True

        return False

    def move(self, dt):
        distance_to_target = self.target_x - self.rect.centerx

        if abs(distance_to_target) > 500:
            self.dead = True

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
        self.hurtbox.center = self.rect.center

    def update_sprites(self, dt):
        self.animator.update(dt)

    def draw_sprites(self, screen, camera):
        image = self.animator.image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        rect = camera.apply(self.rect)
        screen.blit(image, rect)

        if self.debug:
            text_surface = self.font.render(f"{self.stats['hp']}", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(rect.x + 300, rect.y))
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(self.get_hitbox()), 2)
            pygame.draw.rect(screen, (0, 0, 255), camera.apply(self.hurtbox), 2)
