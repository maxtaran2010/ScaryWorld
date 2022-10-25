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
        self.hp = 20
        self.max_hp = 20
        self.bar = HealthBar((10, 10), self.hp, self.max_hp, self.screen)
        self.animation = 0
        self.shot_timeout = 60
        self.speed = 3
        self.max_cartridges = 7
        self.world = self.app.world
        self.bullet_animation = PlayerAnimation(self.app).bullet
        self.hitbox = Hitbox(self.animations.up.get_pygame_surface().get_size(), self.world)
        self.gun = PlayerAnimation(self.app).shotgun
        self.temp_settings = self.app.temp_settings
        self.size = self.animations[0].get_pygame_surface().get_size()
        self.recharge_delay = 1 if self.temp_settings.cheats else 20
        self.cartridges = 7
        self.cartridges_bar = RechargeBar((0, 0), self.cartridges, self.max_cartridges, self.screen)
        self.recharging = False
        self.staying = False
        self.gun.playing = False
        self.directionx = 1
        self.direction = 0
        self.directiony = 1
        self.gun_pos = [0, 0]
        self.angles = {0: 180, 1: 90, 2: 0, 3: -90}

    def update(self):
        self.bar.update(self.hp)
        self.pos = self.x, self.y
        self.shot_timeout -= 1
        self.staying = True
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.direction = 3
            self.directionx = -1
            self.x -= self.speed
            self.staying = False
        if key[pygame.K_d]:
            self.direction = 1
            self.directionx = 1
            self.x += self.speed
            self.staying = False
        if key[pygame.K_w]:
            self.direction = 0
            self.directiony = 1
            self.y -= self.speed
            self.staying = False
        if key[pygame.K_s]:
            self.direction = 2
            self.directiony = -1
            self.y += self.speed
            self.staying = False
        if key[pygame.K_r]:
            self.recharging = True
        if key[pygame.K_SPACE] and self.shot_timeout <= 0 < self.cartridges and not self.recharging:
            angle = self.angles[self.direction]
            offset = 5
            speed = 20
            damage = 10
            time = 20
            self.world.add_object(PlayerBullet, self, self.bullet_animation, speed, damage, time, angle)
            self.world.add_object(PlayerBullet, self, self.bullet_animation, speed, damage, time, angle-offset)
            self.world.add_object(PlayerBullet, self, self.bullet_animation, speed, damage, time, angle+offset)
            self.world.add_object(PlayerBullet, self, self.bullet_animation, speed, damage, time, angle+offset*2)
            self.world.add_object(PlayerBullet, self, self.bullet_animation, speed, damage, time, angle-offset*2)
            self.cartridges -= 1
            self.shot_timeout = 60
            self.gun.playing = True
        if self.hp <= 0 and not self.temp_settings.cheats:
            print('ended')
            self.hp = 20

        if self.cartridges <= 0:
            self.recharging = True
        if self.cartridges >= self.max_cartridges:
            self.recharging = False

        if self.recharging:
            if self.app.tick % self.recharge_delay == 0:
                self.cartridges += 1
            self.cartridges_bar.pos = self.pos[0]-50, self.pos[1] - self.size[1]//2 - 20
            self.cartridges_bar.update(self.cartridges)

        if self.gun.frame == self.gun.len_frames:
            self.gun.playing = False

        self.animation = self.direction if not self.staying else self.direction + 4
        self.hitbox.update(self.pos)
        offset = 30
        if self.directionx == 1:
            self.gun.flip = (0, 0)
            self.gun_pos[0] = self.pos[0]+offset
        if self.directionx == -1:
            self.gun.flip = (1, 0)
            self.gun_pos[0] = self.pos[0]-offset

        self.gun_pos[1] = self.pos[1]+15

    def draw(self):
        if self.recharging:
            self.cartridges_bar.draw()
        self.bar.draw()
        self.gun.draw(*self.gun_pos)
        self.animations[self.animation].draw(*self.pos)

    def give_damage(self, damage):
        if not self.temp_settings.cheats:
            self.hp -= damage
