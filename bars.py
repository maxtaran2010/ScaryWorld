import pygame


class Bar:
    def __init__(self, position, start_value, max_value, screen, color=(0, 255, 0)):
        self.value = start_value
        self.pos = position
        self.color = color
        self.screen = screen
        self.max_value = max_value

    def update(self, value):
        self.value = value

    def draw(self):
        pass


class HealthBar(Bar):
    def draw(self):
        width = 230
        bar_width = self.value*200//self.max_value
        height = 30
        pos = self.pos
        pygame.draw.rect(self.screen, (255, 255, 255), (*pos, width, height), 5)
        pygame.draw.rect(self.screen, self.color, (pos[0]+15, pos[1]+10, bar_width, height-20))


class RechargeBar(Bar):
    def draw(self):
        width = 100
        height = 10
        line_width = 4
        percentage = self.value * width // self.max_value
        line_pos = self.pos[0]+percentage, self.pos[1]-height//2
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pos[0]-line_width//2, self.pos[1], line_width, height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pos[0]-line_width//2+width, self.pos[1], line_width, height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pos[0], self.pos[1]-line_width//2+height//2, 100, line_width))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pos[0]-line_width//2+percentage, self.pos[1], line_width, height))


class MonsterBar(Bar):
    def __init__(self, *args, app):
        super().__init__(*args)
        self.app = app

    def draw(self):
        mwidth = self.app.width
        width = self.value * mwidth // self.max_value
        height = 50
        pygame.draw.rect(self.screen, (48, 56, 67), (self.pos[0]-mwidth//2, self.pos[1]-height//2, mwidth, height))
        pygame.draw.rect(self.screen, (50, 67, 48), (self.pos[0]-mwidth//2, self.pos[1]-height//2, width, height))
        r = self.app.font.render(f'level 1       killed: {self.value}', True, (255, 255, 255))
        self.screen.blit(r, (self.app.width//2-r.get_width()//2, 10))
