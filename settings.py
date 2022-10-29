class Settings:
    def __init__(self):
        self.bg = 0, 0, 0


class TempSettings:
    def __init__(self):
        self.show_hitboxes = 0
        self.cheats = 0
        self.hardness = 1

    def change_difficulty(self, diff):
        self.hardness = diff

    def enable_cheats(self):
        self.cheats = not self.cheats
        return 'Cheats: on' if self.cheats else 'Cheats: off'
