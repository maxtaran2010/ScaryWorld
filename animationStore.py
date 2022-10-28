import animations


class PlayerAnimation:
    def __init__(self, app):
        self.down = animations.Animation(file='assets/players/player_artur_down.gif', app=app, scale_coef=4, delay=10)
        self.up = animations.Animation(file='assets/players/player_artur_up.gif', app=app, scale_coef=4, delay=10)
        self.left = animations.Animation(file='assets/players/player_artur_left.gif', app=app, scale_coef=4, delay=10)
        self.right = animations.Animation(file='assets/players/player_artur_right.gif', app=app, scale_coef=4, delay=10)
        self.stay_down = animations.Animation(file='assets/players/player_artur_stay_down.gif', app=app, scale_coef=2, delay=10)
        self.stay_up = animations.Animation(file='assets/players/player_artur_stay_up.gif', app=app, scale_coef=2, delay=10)
        self.stay_left = animations.Animation(file='assets/players/player_artur_stay_left.gif', app=app, scale_coef=2, delay=10)
        self.stay_right = animations.Animation(file='assets/players/player_artur_stay_right.gif', app=app, scale_coef=2, delay=10)
        self.bullet = animations.Animation(file='assets/attacks/bullet_player.gif', app=app, scale_coef=3, delay=2)
        self.shotgun = animations.Animation('assets/guns/shotgun.gif', app, 2)
        self.shotgun_recharge = animations.Animation('assets/guns/shotgun_recharging.gif', app, 2, (0, 0, 0), 7)
        self.items = [self.up, self.right, self.down, self.left, self.stay_up, self.stay_right, self.stay_down, self.stay_left]

    def __getitem__(self, item):
        return self.items[item]


class HeartAnimation:
    def __init__(self, app):
        self.main = animations.Animation('assets/heart/heart.gif', app, 3, (0, 0, 0))


class DragonAnimation:
    def __init__(self, app):
        self.main = animations.Animation('assets/dragon/attack.gif', app, 2, (0, 0, 0), 7)
        self.bullet = animations.Animation('assets/attacks/electric_ball.gif', app, 2)
        self.bbullet = animations.Animation('assets/attacks/darkpink_electric_ball.gif', app, 2)


class Background:
    def __init__(self, app):
        self.default = animations.Animation('assets/background/default.gif', app, 2)
        self.default2 = animations.Animation('assets/background/default#2.gif', app, 2)
        self.default3 = animations.Animation('assets/background/default#3.gif', app, 2)
        self.defaults = [self.default, self.default2, self.default3]

        self.grass = animations.Animation('assets/background/grass.gif', app, 1)
        self.grass1 = animations.Animation('assets/background/grass#1.gif', app, 1.1)
        self.grass2 = animations.Animation('assets/background/grass#2.gif', app, 1.2)
        self.grass3 = animations.Animation('assets/background/grass#3.gif', app, 1.1)

        self.stone1 = animations.Animation('assets/background/stone#1.gif', app, 1)
        self.stone2 = animations.Animation('assets/background/stone#2.gif', app, 0.5)
        self.stone3 = animations.Animation('assets/background/stone#3.gif', app, 0.5)

        self.tiles = [
            self.grass, self.grass1, self.grass2, self.grass3,
            self.stone1, self.stone2, self.stone3
        ]


class UI:
    def __init__(self, app):
        self.button_start = animations.Animation(file='assets/ui/button_start.gif', app=app, scale_coef=4, pc=False)
        self.button_center = animations.Animation(file='assets/ui/button_center.gif', app=app, scale_coef=4, pc=False)
        self.button_end = animations.Animation(file='assets/ui/button_end.gif', app=app, scale_coef=4, pc=False)


class GrootAnimation:
    def __init__(self, app):
        self.stay = animations.Animation(file='assets/groot/groot_stay.gif', app=app, scale_coef=4, pc=True, delay=7)
        self.walk = animations.Animation(file='assets/groot/groot_going.gif', app=app, scale_coef=4, delay=8)