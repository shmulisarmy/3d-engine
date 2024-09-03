class Position:
    def __init__(self, y: int, x: int):
        self.x = x
        self.y = y

    def pair(self):
        return (self.x, self.y)