import random
from Codes.Task.Utils.Directions import Dir

class Dot:
    def __init__(self, xy, size=5, color=(255, 255, 255), right_prob=0.5):
        self.size = size
        self.color = color
        self.xy = xy
        self.move_direction = Dir.Right if random.random() > right_prob else Dir.Left

