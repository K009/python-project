import pygame as pg
from os import path
import heapq
vec = pg.math.Vector2

TILESIZE = 30
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 30
DARKGREEN = (0, 102, 0)
GREEN = (0, 255, 0)
LAKE = (0, 102, 255)
BROWN = (102, 51, 0)
LIGHTGRAY = (140, 140, 140)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)] #right, left, up, down
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)] #diagonals

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        return neighbors


class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10 # linia prosta
        else:
            return self.weights.get(to_node, 0) + 14 # ukos

    def draw(self):
        for tile in self.weights:
            x, y = tile
            rect = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
            pg.draw.rect(screen, LAKE, rect)

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def draw_icons():
    start_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=start_center))
    goal_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center=goal_center))

def vec2int(v):
    return (int(v.x), int(v.y))

def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0) #start - polozenia smoka, pierwszy wierzcholek koszt dojscia to 0 ofc.
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next) #koszt dojscia tu gdzie jestesmy + dojscia do pola sąsiedniego
            if next not in cost or next_cost < cost[next]: #jesli juz nie bylo liczone w kosztach lub jesli jest koszt calkowitego przejscia na to pole jest mniejszy od samego kosztu przejscia z pola na ktorym jestesmy na to na ktore chcemy pojsc
                cost[next] = next_cost
                priority = next_cost #koszt dojscia do obecnie wyliczonego najdalszego wierzcholka

                frontier.put(next, priority) #wstawienie na kolejke
                path[next] = vec(current) - vec(next) #wyliczona sciezka. obecne pole - kolejne
    return path

icon_dir = path.join(path.dirname(__file__), 'images')
home_img = pg.image.load(path.join(icon_dir, 'castle.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (50, 50))
grass_img = pg.image.load(path.join(icon_dir, 'grass.jpg')).convert_alpha()
grass_img = pg.transform.scale(home_img, (50, 50))
#home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
cross_img = pg.image.load(path.join(icon_dir, 'dragon.png')).convert_alpha()
cross_img = pg.transform.scale(cross_img, (50, 50))
#cross_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)
arrows = {}
arrow_img = pg.image.load(path.join(icon_dir, 'arrowRight.png')).convert_alpha()
arrow_img = pg.transform.scale(arrow_img, (50, 50))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))

g = WeightedGrid(GRIDWIDTH, GRIDHEIGHT)
terrain = [(11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (16, 8), (15, 8), (14, 8), (13, 8), (12, 8), (11, 8), (10, 8), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (12, 11), (13, 11), (14, 11), (12, 5), (13, 5), (14, 5), (11, 5), (15, 5), (12, 4), (13, 4), (14, 4)]
# terrain = []
for tile in terrain:
    g.weights[tile] = 15

goal = vec(14, 12)
#start = vec(16,9)
start = vec(20, 0)
path = dijkstra_search(g, goal, start)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, DARKGREEN, rect)
    draw_grid()
    g.draw()

    current = start + path[vec2int(start)]
    while current != goal:
        x = current.x * TILESIZE + TILESIZE / 2
        y = current.y * TILESIZE + TILESIZE / 2
        img = arrows[vec2int(path[(current.x, current.y)])]
        r = img.get_rect(center=(x, y))
        screen.blit(img, r)

        current = current + path[vec2int(current)]
    draw_icons()
    pg.display.flip()
