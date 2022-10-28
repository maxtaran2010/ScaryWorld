import dragon
import groot


class Preload:
    def __init__(self, app):
        self.to_preload = [dragon.Dragon, groot.Groot]
        self.num_preloads = [5, 5]
        self.preloads = []
        self.app = app

    def preload(self):
        self.app.max_loading_process += sum(self.num_preloads)
        for i in range(len(self.to_preload)):
            x = []
            for ii in range(self.num_preloads[i]):
                x.append(self.to_preload[i](self.app))
                self.app.loading_process += 1
            self.preloads.append(x)
