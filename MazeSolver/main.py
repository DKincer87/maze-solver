import cv2
import threading
from maze import Maze, MazeSettings
from node import Node
from search import Search


# Allows the user to put the start and endpoint on the img
def mouse_event(event, pX, pY, flags, param):
    global maze, img
    if event == cv2.EVENT_LBUTTONUP:
        if not maze.start:
            cv2.rectangle(img, (pX - MazeSettings.NODE_SIZE, pY - MazeSettings.NODE_SIZE),
                          (pX + MazeSettings.NODE_SIZE, pY + MazeSettings.NODE_SIZE), MazeSettings.START_NODE_COLOR, -1)
            maze.set_start_node(Node(pX, pY, True))
            print("start = ", maze.start.x, maze.start.y)
        elif not maze.end:
            cv2.rectangle(img, (pX - MazeSettings.NODE_SIZE, pY - MazeSettings.NODE_SIZE),
                          (pX + MazeSettings.NODE_SIZE, pY + MazeSettings.NODE_SIZE), MazeSettings.END_NODE_COLOR, -1)
            maze.set_end_node(Node(pX, pY))
            print("end = ",  maze.end.x, maze.end.y)

# displays the map and allows drawing updates.


def disp():
    global img

    cv2.imshow(MazeSettings.NAME, img)
    cv2.setMouseCallback(MazeSettings.NAME, mouse_event)
    while True:
        cv2.imshow(MazeSettings.NAME, img)
        cv2.waitKey(1)


# Load in the image
img = cv2.imread('mazes/maze-4.jpg', cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# Setup the Maze
maze = Maze(img)

# Set the cv2 image on another thread to update drawing in real time
t = threading.Thread(target=disp, args=())
t.daemon = True
t.start()

# Wait for the user to draw start and end points
while not maze.ready():
    pass

# Solve the maze
search = Search(maze)
search.a_star_search()
input("Press Enter to continue...")
