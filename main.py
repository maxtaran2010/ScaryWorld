import pygame
import animations
import settings
import player
from background import Background
import world
from threading import Thread
import ui


pygame.font.init()


class App:
    def __init__(self):
        self.bars = []
        self.running = True
        self.res = self.width, self.height = 1216, 800-32
        self.screen = pygame.display.set_mode(self.res, pygame.SCALED)
        img = pygame.image.load('assets/logo.png')
        img = pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
        self.screen.blit(img, (self.width//2-img.get_width()//2, self.height//2-img.get_height()//2))
        pygame.display.flip()
        self.loading_process = 0
        self.max_loading_process = 0
        self.ended = False
        self.win = False
        self.threads = []
        self.threads.append(Thread(target=self.loading))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        pygame.display.set_icon(pygame.image.load('assets/icon.ico'))
        self.settings = settings.Settings()
        self.world = world.World(self)
        self.temp_settings = settings.TempSettings()
        self.tick = 0
        self.player = player.Player(self)
        self.font = pygame.font.Font('assets/font.ttf', 28)
        pygame.mouse.set_visible(False)
        self.background = Background(self).screen
        self.cursor = animations.Animation('assets/cursor.gif', self, 2)
        self.playing = False
        self.win_render = self.font.render('You Won!', True, (255, 241, 118))
        self.lose_render = self.font.render('You lose!', True, (255, 241, 118))
        self.win_render = pygame.transform.scale(self.win_render, (self.win_render.get_width()*5, self.win_render.get_height()*5))
        self.lose_render = pygame.transform.scale(self.lose_render, (self.lose_render.get_width()*5, self.lose_render.get_height()*5))
        self.ui = ui.UI(self, self.font)
        logo = ui.Image(animations.Animation(file='assets/logogame.png', app=self, scale_coef=2, pc=False))
        self.ui.add(logo)
        scene_settings = [logo, ui.Slider(self.ui, 1, 10, 'Difficulty', self.temp_settings.change_difficulty),
                          ui.Button(self.ui, 'Cheats: off', self.temp_settings.enable_cheats, tuple()),
                          ui.Button(self.ui, 'Back', lambda obj: obj.switch_scene(0), (self.ui,)),
                          ]
        self.ui.add_scene(False, scene_settings)
        self.ui.add(ui.Button(self.ui, 'Play', self.start, tuple()))
        self.ui.add(ui.Button(self.ui, 'Settings', lambda obj: obj.switch_scene(1), (self.ui,)))
        self.ui.add(ui.Button(self.ui, 'Quit', self.quit, tuple()))
        self.is_loading = False
        self.need_to_load = True

    def start(self):
        self.playing = True
        self.is_loading = True
        self.threads.append(Thread(target=self.loading))

    def quit(self):
        self.running = False

    def update(self):
        self.tick += 1
        self.screen.fill(self.settings.bg)
        if self.playing:
            self.player.update()
            self.world.update()
        pygame.display.set_caption('Scary World           FPS: '+str(round(self.clock.get_fps())))

    def draw(self):
        if self.playing:
            self.screen.blit(self.background, (0, 0))
            self.world.draw()
            self.player.draw()
            for i in self.bars:
                i.draw()
        else:
            self.ui.draw()
        self.cursor.draw(*pygame.mouse.get_pos())
        pygame.display.flip()

    def end(self):
        self.screen.fill((0, 0, 0))
        if self.win:
            self.screen.blit(self.win_render, (self.width//2-self.win_render.get_width()//2, self.height//3-self.win_render.get_height()//2))
        else:
            self.screen.blit(self.lose_render, (self.width//2-self.lose_render.get_width()//2, self.height//3-self.lose_render.get_height()//2))
        rr = self.font.render('Press enter...', False, (255, 241, 118))
        self.screen.blit(rr, (self.width // 2 - rr.get_width() // 2, self.height // 3*2 - rr.get_height() // 2))
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.ended = False
            self.player.hp = self.player.max_hp
            self.win = False
            self.playing = False
            self.is_loading = False
            self.loading_process = 0
            self.threads = []
            self.world.killed = 0
            self.max_loading_process = 0
        pygame.display.flip()

    def loading(self):
        loading = pygame.image.load('assets/loading.png')
        half_size = loading.get_size()
        loading = pygame.transform.scale(loading, (half_size[0]*2, half_size[1]*2))
        num_items = 5
        loading_pos = self.width//2 - 200, self.height//num_items*3 - 20
        while (self.loading_process != self.max_loading_process or self.max_loading_process == 0) and self.running:
            self.clock.tick(1)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.running = False
            if self.max_loading_process != 0:
                value = self.loading_process * 400 // self.max_loading_process
            else:
                value = 0
            self.screen.fill((0, 0, 0))
            self.screen.blit(loading, (self.width//2-half_size[0], self.height//num_items*2-half_size[1]))
            render = self.font.render(f'{self.loading_process*100//self.max_loading_process}%', False, (255, 241, 118))
            self.screen.blit(render, (self.width//2-render.get_width()//2, self.height//num_items*4-render.get_height()))
            pygame.draw.rect(self.screen, (255, 241, 118), (*loading_pos, value, 40))
            pygame.draw.rect(self.screen, (255, 241, 118), (loading_pos[0]-10, loading_pos[1]-10, 420, 60), 5)
            pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.running = False
                if i.type == pygame.KEYUP:
                    if i.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.threads = []

            if self.is_loading:
                if self.need_to_load:
                    self.threads.append(Thread(target=self.world.on_ready))
                else:
                    self.loading_process = self.max_loading_process
                for t in self.threads:
                    t.start()

                for t in self.threads:
                    t.join()
                self.is_loading = False

            if not self.ended:
                self.update()
                self.draw()
            else:
                self.end()


if __name__ == '__main__':
    app = App()
    app.run()
