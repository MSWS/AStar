import graphics
import random
import math
import time

WIDTH, HEIGHT = 1300, 800
NODE_SIZE = 15


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
            color = "green" if self.passable else "darkgreen"
        x, y = getGraphCoords(self.x, self.y)
        drawRect(win, x, y, x + NODE_SIZE, y + NODE_SIZE, color)


def main():
    win = graphics.GraphWin("A*", WIDTH, HEIGHT)
    win.update()
    while True:
        nodes = generateNodes(win)

        start = getRandomNode(nodes)
        end = getRandomNode(nodes)

        # print(win.checkMouse().x)
        # m = win.getMouse()
        # x, y = getNodeCoords(m.x, m.y)
        # start = nodes[int(x)][int(y)]
        start.passable = True
        start.draw(win, "blue")

        # m = win.getMouse()
        # x, y = getNodeCoords(m.x, m.y)
        # end = nodes[int(x)][int(y)]
        end.passable = True

        end.draw(win, "purple")

        getPath(win, nodes, start, end)
        drawPath(win, start, end)


def drawPath(win, start, end):
    node = end.parent
    while node and node != start:
        if node == start:
            break
        node.draw(win, "grey")
        node = node.parent
    win.update()


def drawRect(win, x1, y1, x2, y2, color=None):
    win.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


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
            current.draw(win, "#{:06x}".format(int(current.fCost / biggestCost * 100000)))
            coords = getGraphCoords(current.x, current.y)
            win.create_text(coords[0] + NODE_SIZE // 2, coords[1] + NODE_SIZE // 2, text=round(math.sqrt(current.fCost)),
                            fill="white")
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
                    node.draw(win, "lightblue")
                if node not in open:
                    open.append(node)
                coords = getGraphCoords(node.x, node.y)
                win.create_text(coords[0] + NODE_SIZE // 2, coords[1] + NODE_SIZE // 2, text=round(math.sqrt(node.fCost)))
        win.update()
        # time.sleep(.05)

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
            p = random.random() < .5
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
