import random
import math
import cv2
import numpy

WIDTH, HEIGHT = 1000, 800
NODE_SIZE = 5


def main():
    while True:
        img = numpy.zeros((HEIGHT, WIDTH, 3), numpy.uint8)
        nodes = generateNodes(img)
        start = getRandomNode(nodes)
        end = getRandomNode(nodes)
        start.passable = True
        start.draw(img, (0, 0, 255))
        end.passable = True
        end.draw(img, (255, 0, 255))

        getPath(img, nodes, start, end)
        drawPath(img, start, end)


class Node(object):
    def __init__(self, x, y, passable=True):
        self.x = x
        self.y = y
        self.passable = passable
        self.fCost = 0
        self.gCost = 0
        self.hCost = 0
        self.parent = None

    def draw(self, win, color=None):
        if not color:
            color = (0, 255, 0) if self.passable else (50, 150, 50)
        x, y = getGraphCoords(self.x, self.y)
        drawRect(win, x, y, x + NODE_SIZE, y + NODE_SIZE, color)


def drawPath(win, start, end):
    node = end.parent
    while node and node != start:
        if node == start:
            break
        node.draw(win, (0, 0, 255))
        node = node.parent
        cv2.imshow("A*", win)
        cv2.waitKey(1)
    # win.update()
    cv2.imshow("A*", win)


def drawRect(win, x1, y1, x2, y2, color):
    """Creates a filled rectangle"""
    cv2.rectangle(win, (x1, y1), (x2, y2), color, thickness=-1)


def getPath(win, nodes, start: Node, end: Node):
    nodeList = []

    for nodeX in nodes:
        for nodeY in nodeX:
            nodeY.fCost = getDistanceSquared(start, nodeY) + getDistanceSquared(end, nodeY)
            nodeY.gCost = getDistanceSquared(start, nodeY)
            nodeList.append(nodeY)

    nodeList = sorted(nodeList, key=lambda n: n.fCost)
    biggestCost = nodeList[-1].fCost
    open = [start]
    closed = []

    while open:
        open = sorted(open, key=lambda n: n.fCost)
        current = open[0]
        if current != start and current != end:
            red = current.fCost / biggestCost * 255
            green = current.gCost / biggestCost * 50000
            blue = current.hCost / biggestCost * 5000
            current.draw(win, (blue % 255, green % 255, red % 255))
            # coords = getGraphCoords(current.x, current.y)
            # cv2.putText(win, str(round(math.sqrt(current.fCost))),
            #             (coords[0], coords[1]), cv2.FONT_HERSHEY_SIMPLEX, .25,
            #             (255, 255, 255))
        open.remove(current)
        closed.append(current)

        if current == end:
            return

        for node in getNeighbors(nodes, current):
            if not node.passable or node in closed:
                continue
            newCost = current.gCost + getDistanceSquared(current, node)
            if newCost < node.gCost or node not in open:
                node.gCost = newCost
                node.hCost = getDistanceSquared(node, end)
                node.fCost = node.gCost + node.hCost
                node.parent = current

                if node != end:
                    node.draw(win, (128, 64, 64))
                if node not in open:
                    open.append(node)
                # coords = getGraphCoords(node.x, node.y)
                # cv2.putText(win, str(round(math.sqrt(node.fCost))),
                #             (coords[0], coords[1]), cv2.FONT_HERSHEY_SIMPLEX, .25,
                #             (255, 255, 255))
        # win.update()
        cv2.imshow("A*", win)
        cv2.waitKey(1)

    print("Could not complete pathfinding")


def getNeighbors(nodes, node: Node):
    """Returns all neighbors of a node"""
    # offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (0, 0)]
    offsets = [(-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)]
    neighbors = []
    for offset in offsets:
        x = node.x + offset[0]
        y = node.y + offset[1]

        if x < 0 or y < 0:
            continue

        if x >= WIDTH // NODE_SIZE or y >= HEIGHT // NODE_SIZE:
            continue
        neighbors.append(nodes[x][y])
    return neighbors


def getDistance(node1: Node, node2: Node):
    """
    Returns the difference between two different nodes
    Note that for comparison and speed, getDistanceSquared is better
    """
    return math.sqrt(getDistanceSquared(node1, node2))


def getDistanceSquared(node1: Node, node2: Node):
    """Returns the distance (squared) between two different nodes"""
    return (node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2


def getRandomNode(nodes):
    """Returns a randomly selected node from the 2D array"""
    return nodes[random.randrange(len(nodes))][random.randrange(len(nodes[0]))]


def generateNodes(win):
    """Generates nodes and displays them"""
    nodes = []
    for x in range(0, WIDTH // NODE_SIZE):
        for y in range(0, HEIGHT // NODE_SIZE):
            if len(nodes) <= x:
                nodes.insert(x, [])
            ar = nodes[x]
            ar.append(Node(x, y, True))
            # ar[-1].draw(win)

            nodes[x] = ar

    gridSize = 5

    for x in range(0, WIDTH // NODE_SIZE, gridSize):
        for y in range(0, WIDTH // NODE_SIZE, gridSize):
            if random.random() < .4:
                for i in range(gridSize):
                    if y >= len(nodes[0]) or x + i >= len(nodes):
                        break
                    nodes[x + i][y].passable = False
            if random.random() < .4:
                for i in range(gridSize):
                    if y + i >= len(nodes[0]) or x >= len(nodes):
                        break
                    nodes[x][y + i].passable = False

    for nodeList in nodes:
        for node in nodeList:
            node.draw(win)

    return nodes


def getNodeCoords(x, y):
    """Converts from graphical coordinates to node coordinates"""
    return (x + 1) // NODE_SIZE, (y + 1) // NODE_SIZE


def getGraphCoords(x, y):
    """Converts from node coordinates to graphical coordinates"""
    return x * NODE_SIZE, y * NODE_SIZE


if __name__ == "__main__":
    main()
