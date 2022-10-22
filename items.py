import animationStore
import hitboxes
import random
import pygame


class Heart:
    def __init__(self, app):
        self.app = app
        self.world = app.world
        self.animation = animationStore.HeartAnimation(app).main
        self.size = self.animation.get_pygame_surface().get_size()
        self.hitbox = hitboxes.Hitbox(self.size, self.world)
        self.pos = random.randint(0, self.app.width-self.size[0]), random.randint(0, self.app.height-self.size[1])
        self.screen = app.screen
        self.temp_settings = self.app.temp_settings
        self.deleted = False

    def update(self):
        self.hitbox.update(self.pos)
        if self.hitbox.hits(self.app.player.hitbox):
            self.app.player.hp += 3
            if self.app.player.hp > self.app.player.max_hp:
                self.app.player.hp = self.app.player.max_hp
            self.delete()

    def draw(self):
        self.animation.draw(*self.pos)

    def delete(self):
        self.world.remove(self)
        self.world.hearts -= 1
