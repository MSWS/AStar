import graphics
import random
import math
import time
import cv2
import numpy

WIDTH, HEIGHT = 1000, 800
NODE_SIZE = 5


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
            color = (0, 255, 0) if self.passable else (50, 205, 50)
        x, y = getGraphCoords(self.x, self.y)
        drawRect(win, x, y, x + NODE_SIZE, y + NODE_SIZE, color)


def main():
    # win = graphics.GraphWin("A*", WIDTH, HEIGHT)

    # win.update()
    while True:
        img = numpy.zeros((HEIGHT, WIDTH, 3), numpy.uint8)
        nodes = generateNodes(img)
        # start = getRandomNode(nodes)
        # end = getRandomNode(nodes)
        start = nodes[0][0]
        end = nodes[len(nodes) - 1][len(nodes[0]) - 1]
        # print(win.checkMouse().x)
        # m = win.getMouse()
        # x, y = getNodeCoords(m.x, m.y)
        # start = nodes[int(x)][int(y)]
        start.passable = True
        start.draw(img, (0, 0, 255))
        # m = win.getMouse()
        # x, y = getNodeCoords(m.x, m.y)
        # end = nodes[int(x)][int(y)]
        end.passable = True

        end.draw(img, (128, 0, 128))
        getPath(img, nodes, start, end)
        drawPath(img, start, end)


def drawPath(win, start, end):
    node = end.parent
    while node and node != start:
        if node == start:
            break
        node.draw(win, (100, 100, 100))
        node = node.parent
        cv2.imshow("A*", win)
        cv2.waitKey(1)
    # win.update()
    cv2.imshow("A*", win)


def drawRect(win, x1, y1, x2, y2, color=None):
    # win.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
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
            red = current.fCost / biggestCost * 2550
            green = current.gCost / biggestCost * 50000
            blue = current.hCost / biggestCost * 50000
            current.draw(win, (blue, green, red))
            # coords = getGraphCoords(current.x, current.y)
            # win.create_text(coords[0] + NODE_SIZE // 2, coords[1] + NODE_SIZE // 2,
            #                 text=round(math.sqrt(current.fCost)),
            #                 fill="white")
            # cv2.putText(win, str(round(math.sqrt(current.fCost))),
            #             (coords[0] + NODE_SIZE // 2, coords[1] + NODE_SIZE // 2), cv2.FONT_HERSHEY_SIMPLEX, .4,
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
                    node.draw(win, (128, 128, 255))
                if node not in open:
                    open.append(node)
                coords = getGraphCoords(node.x, node.y)
                # win.create_text(coords[0] + NODE_SIZE // 2, coords[1] + NODE_SIZE // 2,
                #                 text=round(math.sqrt(node.fCost)))
                # cv2.putText(win, str(round(math.sqrt(node.fCost))),
                #             (coords[0] + NODE_SIZE // 2, coords[1] + NODE_SIZE // 2), cv2.FONT_HERSHEY_SIMPLEX, .4,
                #             (0, 0, 0))
        # win.update()
        cv2.imshow("A*", win)
        cv2.waitKey(1)

    print("Could not complete pathfinding")


def getNeighbors(nodes, node: Node):
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (0, 0)]
    # offsets = [(-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)]
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
    return math.sqrt(getDistanceSquared(node1, node2))


def getDistanceSquared(node1: Node, node2: Node):
    return (node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2


def getRandomNode(nodes):
    x = random.randint(0, WIDTH // NODE_SIZE - 1)
    y = random.randint(0, HEIGHT // NODE_SIZE - 1)
    return nodes[x][y]


def generateNodes(win):
    nodes = []
    for x in range(0, WIDTH // NODE_SIZE):
        for y in range(0, HEIGHT // NODE_SIZE):
            p = random.random() > .6
            gx, gy = getGraphCoords(x, y)
            if len(nodes) <= x:
                nodes.insert(x, [])
            ar = nodes[x]
            ar.append(Node(x, y, p))
            ar[-1].draw(win)

            nodes[x] = ar

    return nodes


def getNodeCoords(x, y):
    """Converts from graphical coordinates to node coordinates"""
    return (x + 1) // NODE_SIZE, (y + 1) // NODE_SIZE


def getGraphCoords(x, y):
    return x * NODE_SIZE, y * NODE_SIZE


if __name__ == "__main__":
    main()
