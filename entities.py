DEBUG = False

class PlayerObject:

    def __init__(self, name=None):
        self.x = 0
        self.y = 0
        self.alive = True
        self.moving = False
        self.score = 0
        self.move = False
        self.time = 30
        self.name = name
        self.locked = False


player = PlayerObject(True)
