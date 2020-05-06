class Node(object):
    def __init__(self, x=0, y=0, visited=False, parent=None):
        self.id = f"{x}{y}"
        self.x = x
        self.y = y
        self.visited = visited
        self.parent = parent
        self.totalTravel = 0 if parent is None else parent.totalTravel + 1
        self.score = 0
        self.remainingDistance = None

    def distance(self, other):
        a = (self.x - other.x) ** 2
        b = (self.y - other.y) ** 2
        c = a + b
        return c

    def setScore(self, endpoint):
        self.score = self.totalTravel + self.distance(endpoint)

    def point(self):
        return(self.x, self.y)

    def describe(self):
        return f"x:{self.x} y:{self.y} visited:{self.visited} traveled:{self.totalTravel}"

    def __eq__(self, other):

        return (self.x == other.x and self.y == other.y)

    def __str__(self):
        return self.describe()
