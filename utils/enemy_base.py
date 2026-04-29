import pygame, random
from utils.spritesheet import SpriteSheet


class EnemyBase:
    shared_animations = None

    def initialize(self, x, y, player):
        if EnemyBase.shared_animations is None:
            _anim_temp = {}
            for key in self.animations:
                _anim_temp[key] = SpriteSheet(
                    self.animations[key][0],
                    self.animations[key][1],
                    self.animations[key][2],
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
        self.chase_offset = 150
        self.attack_range = random.randint(10, 100)
        self.attack_timer = 0
        self.attacking = False

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
                self.attacking = False
                self.set_state("idle")
                return False
            return True

        if distance <= self.attack_range and self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer = self.stats["attack_cooldown"]
            self.set_state("attack")
            return True

        return False

    def move(self, dt):
        distance_to_target = self.target_x - self.rect.centerx
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
