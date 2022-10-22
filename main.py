import pygame
import animations
import settings
import player
import world


class App:
    def __init__(self):
        self.res = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.FPS = 55
        self.settings = settings.Settings()
        self.world = world.World(self)
        self.temp_settings = settings.TempSettings()
        self.tick = 0
        self.player = player.Player(self)
        pygame.mouse.set_visible(False)
        self.cursor = animations.Animation('assets/cursor.gif', self, 2)

    def update(self):
        self.tick += 1
        self.screen.fill(self.settings.bg)
        self.player.update()
        self.world.update()
        pygame.display.set_caption('FPS: '+str(round(self.clock.get_fps())))

    def draw(self):
        self.world.draw()
        self.player.draw()
        self.cursor.draw(*pygame.mouse.get_pos())
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(self.FPS)
            [quit() for i in pygame.event.get() if i.type == pygame.QUIT]

            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
