import chances
from hitboxes import Hitbox
from animationStore import GrootAnimation
import math


class Groot:
    def __init__(self, app):
        self.app = app
        self.animations = GrootAnimation(app)
        self.current_animation = self.animations.stay
        self.size = self.current_animation.real_size
        self.pos = chances.pos(self.size, app.res)
        self.player = self.app.player
        self.hp = 10
        self.world = self.app.world
        self.speed = 2.3
        self.hitbox = Hitbox(self.size, self.world)
        self.attack_timeout = 0
        self.attack = False

    def update(self):
        self.attack_timeout -= 1
        dx, dy = self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.pos[0] += self.speed * dx
        self.pos[1] += self.speed * dy

        if not self.attack:
            if dx == 0 and dy == 0:
                self.current_animation = self.animations.stay
            else:
                self.current_animation = self.animations.walk

        if self.hp <= 0:
            self.world.remove(self)
            self.world.killed += 1
            self.restore()

        self.hitbox.update(self.pos)

        if dx > 0:
            self.current_animation.flip = 0, 0

        if dx < 0:
            self.current_animation.flip = 1, 0

        if self.hitbox.hits(self.player.hitbox) and self.attack_timeout <= 0:
            self.player.give_damage(1*self.app.temp_settings.hardness)
            self.attack_timeout = 100
            self.current_animation = self.animations.attack
            self.current_animation.set_frame(0)
            self.current_animation.playing = True
            self.attack = True

        if self.attack and self.current_animation.frame == self.current_animation.len_frames:
            self.current_animation.playing = False
            self.current_animation = self.animations.walk
            self.attack = False

    def draw(self):
        self.current_animation.draw(*self.pos)

    def give_damage(self, dmg):
        self.hp -= dmg

    def restore(self):
        self.hp = 10
        self.pos = chances.pos(self.size, self.app.res)
