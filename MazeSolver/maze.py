import math
from node import Node


class Maze:
    def __init__(self, img, start: Node = None, end: Node = None):
        self.start = start
        self.end = end
        self.img = img
        shape = img.shape[:2]
        self.width = shape[1]
        self.height = shape[0]

    def set_start_node(self, node: Node):
        self.start = node

    def set_end_node(self, node: Node):
        self.end = node

    def goal_distance(self):
        return self.start.distance(self.end)

    def ready(self):
        return self.start is not None and self.end is not None


def getKey(node: Node):
    return node.score


class MazeSettings:
    START_NODE_COLOR = (0, 0, 255)
    END_NODE_COLOR = ((0, 200, 50))
    VISITED_NODE_COLOR = ((200, 100, 50))
    NODE_SIZE = 2
    NAME = "Test"
    MAZE_WALL = [0, 0, 0]
    MAZE_PATH = [255, 255, 255]
