import chances
from animationStore import DragonAnimation
from hitboxes import Hitbox
from bullet import EnemyBullet


class Dragon:
    def __init__(self, app):
        self.app = app
        self.animation = DragonAnimation(app).main
        self.bullet_animation = DragonAnimation(app).bullet
        self.bbullet_animation = DragonAnimation(app).bbullet
        self.size = self.animation.get_pygame_surface().get_size()
        self.pos = chances.pos(self.size, self.app.res)
        self.world = app.world
        self.hitbox = Hitbox(self.size, self.world)
        self.temp_settings = app.temp_settings
        self.screen = app.screen
        self.hp = 10*self.app.temp_settings.hardness
        self.player = app.player
        self.moving = chances.RandomMoving(self.pos, self.app.res, 2*self.app.temp_settings.hardness, self.size)
        self.animation.playing = False

    def update(self):
        self.hitbox.update(self.pos)
        self.pos = self.moving.increase()
        if self.animation.frame == self.animation.len_frames:
            self.animation.playing = False
            self.animation.set_frame(0)
            if chances.chance(10):
                self.world.add_object(EnemyBullet, self, self.player.pos, self.bbullet_animation, 4, 10*self.app.temp_settings.hardness, True)
            else:
                self.world.add_object(EnemyBullet, self, self.player.pos, self.bullet_animation, 6, 3*self.app.temp_settings.hardness, False)

        if chances.chance(0.5*self.app.temp_settings.hardness):
            self.animation.playing = True

        if self.hp <= 0:
            self.world.killed += 1
            self.world.remove(self)
            self.restore()

    def restore(self):
        self.hp = 10
        self.pos = chances.pos(self.size, self.app.res)
        self.moving.pos = self.pos

    def draw(self):
        self.animation.draw(*self.pos)

    def give_damage(self, dam):
        self.hp -= dam
