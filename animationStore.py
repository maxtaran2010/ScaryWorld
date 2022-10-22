import animations


class PlayerAnimation:
    def __init__(self, app):
        self.staying = animations.Animation(file='assets/player/stay.gif', app=app, scale_coef=5, delay=10)
        self.walk = animations.Animation(file='assets/player/walk.gif', app=app, scale_coef=5, delay=2)
        self.bullet = animations.Animation(file='assets/attacks/bullet_player.gif', app=app, scale_coef=3, delay=2)
        self.items = [self.staying, self.walk]

    def __getitem__(self, item):
        return self.items[item]


class HeartAnimation:
    def __init__(self, app):
        self.main = animations.Animation('assets/heart/heart.gif', app, 3, (0, 0, 0))


class DragonAnimation:
    def __init__(self, app):
        self.main = animations.Animation('assets/dragon/main.gif', app, 5)
        self.bullet = animations.Animation('assets/attacks/electric_ball.gif', app, 3)
