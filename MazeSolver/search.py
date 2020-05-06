from maze import Maze, MazeSettings
from node import Node
import colorsys


class Search:

    def __init__(self, maze: Maze):
        self.maze = maze
        print("maze: ", maze.start, maze.end)
        self.queue = []
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def a_star_search(self):

        # check if we are at the end
        if(self.maze.start == self.maze.end):
            print("We did it")
        self.queue.append(self.maze.start)

        # create a 2d array to track where we have been
        visited = [[0 for x in range(self.maze.width)]
                   for y in range(self.maze.height)]

        # Start looking
        finished = False
        while len(self.queue) > 0 and not finished:
            node = self.queue.pop(0)
            if(node == self.maze.end):
                finished = True
            for d in self.directions:
                newNode = Node(node.x + d[0], node.y + d[1], True, node)
                try:
                    if(newNode.x < self.maze.width and newNode.x > 0 and newNode.y < self.maze.height and newNode.y > 0 and visited[newNode.y][newNode.x] != 1):
                        color = list(self.maze.img[newNode.y, newNode.x])
                        visited[node.y][node.x] = 1
                        if(color != MazeSettings.MAZE_WALL):
                            newNode.setScore(self.maze.end)
                            self.maze.img[newNode.y,
                                          newNode.x] = MazeSettings.VISITED_NODE_COLOR
                            if(len(self.queue) == 0):
                                self.queue.append(newNode)
                            else:
                                inserted = False
                                # TODO: This portion can be optimized
                                if(newNode not in self.queue):
                                    # N Search seems slow.
                                    for q in self.queue:
                                        if(newNode.score < q.score):
                                            self.queue.insert(
                                                self.queue.index(q), newNode)
                                            inserted = True
                                            break
                                    if not inserted:
                                        self.queue.append(newNode)

                except IndexError:
                    print("new node:", newNode)
                    print("maze: ", self.maze.width, self.maze.height)
