from animationStore import PlayerAnimation
from hitboxes import Hitbox
from bars import *
from bullet import PlayerBullet


class Player:
    def __init__(self, app):
        self.screen = app.screen
        self.res = self.width, self.height = app.res
        self.pos = self.x, self.y = 500, 500
        self.app = app
        self.animations = PlayerAnimation(self.app)
        self.direction = 0
        self.hp = 20
        self.max_hp = 20
        self.bar = HealthBar((10, 10), self.hp, self.max_hp, self.screen)
        self.animation = 0
        self.shot_timeout = 0
        self.speed = 3
        self.max_cartridges = 10
        self.world = self.app.world
        self.bullet_animation = PlayerAnimation(self.app).bullet
        self.hitbox = Hitbox(self.animations.staying.get_pygame_surface().get_size(), self.world)
        self.temp_settings = self.app.temp_settings
        self.size = self.animations[0].get_pygame_surface().get_size()
        self.recharge_delay = 1 if self.temp_settings.cheats else 7
        self.cartridges = 10
        self.cartridges_bar = RechargeBar((0, 0), self.cartridges, self.max_cartridges, self.screen)
        self.recharging = False

    def update(self):
        self.bar.update(self.hp)
        self.pos = self.x, self.y
        self.shot_timeout -= 1
        key = pygame.key.get_pressed()
        walking = True
        if key[pygame.K_w]:
            self.direction = 0
            self.y -= self.speed
            walking = False
        if key[pygame.K_s]:
            self.direction = 2
            self.y += self.speed
            walking = False
        if key[pygame.K_a]:
            self.direction = 3
            self.x -= self.speed
            walking = False
        if key[pygame.K_d]:
            self.direction = 1
            self.x += self.speed
            walking = False
        if key[pygame.K_r]:
            self.recharging = True
        if pygame.mouse.get_pressed()[0] and self.shot_timeout <= 0 < self.cartridges and not self.recharging:
            self.world.add_object(PlayerBullet, self, pygame.mouse.get_pos(), self.bullet_animation, 30, 5)
            self.cartridges -= 1
            self.shot_timeout = 10
        if self.hp <= 0 and not self.temp_settings.cheats:
            quit()

        if self.cartridges <= 0:
            self.recharging = True
        if self.cartridges >= self.max_cartridges:
            self.recharging = False

        if self.recharging:
            if self.app.tick % self.recharge_delay == 0:
                self.cartridges += 1
            self.cartridges_bar.pos = self.pos[0]-50, self.pos[1] - self.size[1]//2 - 20
            self.cartridges_bar.update(self.cartridges)

        self.animation = not walking
        self.hitbox.update(self.pos)

    def draw(self):
        if self.recharging:
            self.cartridges_bar.draw()
        self.bar.draw()
        self.animations[self.animation].draw(*self.pos)

    def damage(self, damage):
        if not self.temp_settings.cheats:
            self.hp -= damage
