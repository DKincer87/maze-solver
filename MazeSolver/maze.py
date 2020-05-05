import cv2
import numpy as np
import threading
import colorsys
import math

class Node(object):
    def __init__(self, x=0, y=0, visited=False, parent = None):
        self.id = f"{x}{y}"
        self.x = x
        self.y = y 
        self.visited = visited
        self.parent = parent
        self.totalTravel = 0 if parent is None else parent.totalTravel + 1
        self.score = 0
        self.remainingDistance = None
    def distance(self,other):
        a = (self.x - other.x) ** 2
        b = (self.y - other.y) ** 2
        c = a + b
        return c
    
    def setScore(self,endpoint):
        self.score = self.totalTravel + self.distance(endpoint)

    def point(self):
        return(self.x,self.y)

    def describe(self):
        return f"x:{self.x} y:{self.y} visited:{self.visited} traveled:{self.totalTravel}"#, [parent:{self.parent}]"
    
    def __eq__(self, other):

        return (self.x == other.x and self.y == other.y)

    def __str__(self):
        return self.describe()
    

class Maze:
    def __init__(self,start:Node = None,end:Node = None):
        self.start = start
        self.end   = end
    
    def set_start_node(self, node:Node):
        self.start = node

    def set_end_node(self, node:Node):
        self.end = node

    def set_size(self,dimensions):
        self.width = dimensions[1]
        self.height = dimensions[0]
    
    def goal_distance(self):
        return self.start.distance(self.end)

    def ready(self):
        return self.start is not None and self.end is not None

        
def getKey(node:Node):
        return node.score


class MazeSettings:
    START_NODE_COLOR = (0,0,255)
    END_NODE_COLOR = ((0, 200, 50))
    VISITED_NODE_COLOR = ((200, 100, 50))
    NODE_SIZE = 2
    NAME = "Test"
    MAZE_WALL = [0,0,0]
    MAZE_PATH = [255,255,255]


def mouse_event(event, pX, pY, flags, param):
    global maze,img
    if event == cv2.EVENT_LBUTTONUP:
        if not maze.start:
            cv2.rectangle(img, (pX - MazeSettings.NODE_SIZE, pY - MazeSettings.NODE_SIZE),
                          (pX + MazeSettings.NODE_SIZE, pY + MazeSettings.NODE_SIZE), MazeSettings.START_NODE_COLOR, -1)
            maze.set_start_node(Node(pX, pY,True))
            print("start = ", maze.start.x, maze.start.y)
        elif not maze.end:
            cv2.rectangle(img, (pX - MazeSettings.NODE_SIZE, pY - MazeSettings.NODE_SIZE),
                          (pX + MazeSettings.NODE_SIZE, pY + MazeSettings.NODE_SIZE), MazeSettings.END_NODE_COLOR, -1)
            maze.set_end_node(Node(pX, pY))
            print("end = ",  maze.end.x, maze.end.y)


def disp():
    global img
    
    cv2.imshow(MazeSettings.NAME,img)
    cv2.setMouseCallback(MazeSettings.NAME, mouse_event)
    while True:
        cv2.imshow(MazeSettings.NAME,img)
        cv2.waitKey(1)

maze = Maze()
queue = []
directions = [(1,0),(-1,0),(0,1),(0,-1)] 
counter = 0
def a_star_search(maze:Maze):
    global img,counter
    #first find the distance between the start and the end
    # print("start: ",maze.start)
    # print("end: ",maze.end)
    # print("distance: ",maze.goal_distance())
    #color = img[maze.start.y,maze.start.x]
    #print("pixel color ",color)
    #hex = (color[0] << 16) + (color[1] << 8) + (color[2])
    #print("hex ",hex)
    #cv2.line(img,maze.start.point(),maze.end.point(),(0, 255, 0),2)

    #check if we are ate the end
    if(maze.start == maze.end):
        print("We did it")
    queue.append(maze.start)
    print(maze.width,maze.height)
    visited = [[0 for x in range(maze.width)] for y in range(maze.height)]
    finished = False 
    while len(queue) > 0 and not finished:
        node = queue.pop(0)
        if(node == maze.end):
            finished = True
        for d in directions:
            newNode = Node(node.x + d[0],node.y + d[1],True,node)
            try:
                if(newNode.x < maze.width and newNode.x > 0 and newNode.y < maze.height and newNode.y > 0 and visited[newNode.y][newNode.x] != 1):
                    color = list(img[newNode.y,newNode.x])
                    if(color != MazeSettings.MAZE_WALL):
                        newNode.setScore(maze.end)   
                        visited[node.y][node.x] = 1
                        img[newNode.y,newNode.x] = MazeSettings.VISITED_NODE_COLOR
                        if(len(queue) == 0):
                            queue.append(newNode)
                        else:
                            for q in queue:
                                if(newNode.score <= q.score): #if things break mid search for back track it starts here
                                    queue.insert(queue.index(q),newNode)
                                    break
                                else:
                                    queue.append(newNode)
                                    break;
            except IndexError:
                print("new node:", newNode)
                print("maze: ", maze.width,maze.height)
           
                

            
                  
                          






img = cv2.imread('mazes/maze-2.jpg',cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

maze.set_size(img.shape[:2])

t = threading.Thread(target=disp, args=())
t.daemon = True
t.start()

while not maze.ready():
    pass

print(maze.ready())

a_star_search(maze)
input("Press Enter to continue...")
