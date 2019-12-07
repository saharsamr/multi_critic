import random
from Codes.Task.Utils.Directions import Dir
from Codes.Task.Utils.GlobalValues import RIGHT_PROB


class Dot:
    def __init__(self, xy, size=5, color=(255, 255, 255), one_direction_prob=0.5, selected_dir=Dir.Right):
        self.size = size
        self.color = color
        self.xy = xy
        self.selected_dir = selected_dir
        self.move_direction = self.selected_dir if random.random() > one_direction_prob \
            else (Dir.Left if self.selected_dir == Dir.Right else Dir.Right)

