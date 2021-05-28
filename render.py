# type:ignore

import pygame as pg
import threading
import socket
import random
from PIL import Image
import numpy as np
import pyautogui
# from mapMaker import MapMaker
import random as r
from server import Server
from typing import *


class World:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0

    def update(self, player):
        self.x = -int(player.x)+pg.display.get_surface().get_size()[0]//2
        self.y = -int(player.y)+pg.display.get_surface().get_size()[1]//2


class Player:
    def __init__(self, win, x, y, world, name="UNKNOWN", color=None):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.size = [(tileSize//5), (tileSize//5)]
        self.name = name
        if color == None:
            self.color = random.randint(120, 255), random.randint(
                120, 255), random.randint(120, 255)
        else:
            self.color = color

        self.f = pg.font.SysFont("Arial", tileSize//2)
        self.label = self.f.render(self.name, True, self.color)
        self.label_rect = self.label.get_rect()

    def newScreenSize(self):
        self.f = pg.font.SysFont("Arial", tileSize//2)
        self.label = self.f.render(self.name, True, self.color)
        self.label_rect = self.label.get_rect()

        self.x = int(self.x*(tileSize/old))
        self.y = int(self.y*(tileSize/old))
        self.size[0] = int(self.size[0]*(tileSize/old))
        self.size[1] = int(self.size[1]*(tileSize/old))

    def update(self):
        # print("updating "+self.name)
        if self.name == user:
            changeX = 0
            if self.dx != 0:
                iterator = self.dx/abs(self.dx)
                for i in range(int(abs(self.dx))):
                    if Player.checkCollision(self.x+self.size[0]/2-self.size[0] % 2+changeX+iterator+self.size[0]*iterator/2, self.y, tileSize, grid) or Player.checkCollision(self.x+self.size[0]/2+changeX+iterator+self.size[0]*iterator/2, self.y+self.size[1], tileSize, grid):
                        self.dx = 0
                        break
                    changeX += iterator
            changeY = 0
            if self.dy != 0:
                iterator = self.dy/abs(self.dy)
                for i in range(int(abs(self.dy))):
                    if Player.checkCollision(self.x, self.y+self.size[1]/2-self.size[1] % 2+changeY+iterator+self.size[1]*iterator/2, tileSize, grid) or Player.checkCollision(self.x+self.size[0], self.y+self.size[1]/2+changeY+iterator+self.size[1]*iterator/2, tileSize, grid):
                        self.dy = 0
                        break
                    changeY += iterator
            self.x += int(changeX)
            self.y += int(changeY)
        else:
            self.x += int(self.dx)
            self.y += int(self.dy)

        # self.x = int(self.x+self.dx)
        # self.y = int(self.y+self.dy)
        win.blit(self.label, (self.x+world.x+(tileSize//10)-self.label_rect.width //
                 2, self.y+world.y-(tileSize//2)-self.label_rect.height//2))
        self.rect = pg.draw.rect(
            win, self.color, (self.x+world.x, self.y+world.y, self.size[0], self.size[1]))

    def checkCollision(posX, posY, tileSize, grid):
        if sum(grid[int(posY//tileSize), int(posX//tileSize)]) == 255*3:
            return True
        return False


class Renderer:
    def __init__(self, client):
        self.client = client
        self.players: Dict[str, Player] = {}

    def main(self):
        # variables
        global tileSize, s, old, win, keys, p1, maxVelocity, accel, deAccel, wallBounce, renderDistance, collisionDistance, lightSpread, lightIntensity, world, grid, colors, user, d, luminocity
        tileSize = 50
        maxVelocity = 8
        accel = .6
        deAccel = .25
        wallBounce = 0.2
        renderDistance = 32
        collisionDistance = 2
        lightSpread = 20
        lightIntensity = .02

        # create map
        # generateMap()

        # make grid
        im = Image.open("map1.png")
        grid = np.array(im, dtype=float)

        grid = grid[:, :, 0: 3]
        n = np.zeros((np.size(grid, 0)+renderDistance,
                      np.size(grid, 1)+renderDistance, 3))
        n[renderDistance//2: renderDistance//2+grid.shape[0],
            renderDistance//2: renderDistance//2+grid.shape[1]] = grid
        grid = n.copy()
        colors = grid.copy()

        win = pg.display.set_mode(
            size=(1280, 720), flags=(pg.DOUBLEBUF | pg.RESIZABLE))
        win.set_alpha(None)

        pg.font.init()

        menuFont = pg.font.SysFont("Arial", 48)

        world = World()

        doSocket = True

        # generate luminocity matte
        luminocity = np.zeros((10, 10, renderDistance, renderDistance, 3))
        for x in range(10):
            for y in range(10):
                for i in range(renderDistance):
                    for j in range(renderDistance):
                        d = distance((i*tileSize+tileSize, j*tileSize+tileSize), (renderDistance//2 *
                                                                                  tileSize+5*(x+(tileSize//10)), renderDistance//2*tileSize+5*(y+(tileSize//10))))
                        for k in range(3):
                            luminocity[x, y, i, j, k] = min(
                                1, max(0, (lightSpread-d/10)*lightIntensity))

        # collision arr
        side = np.zeros((np.size(grid, 0), np.size(grid, 1)))

        # begin thread
        user = pyautogui.prompt(text='Username:', title='')
        if user == "test":
            ip = 'localhost'
            port = 1234
            s = Server(port)
            threading.Thread(
                target=s.main,
                daemon=True
            ).start()
        elif user == "g":
            ip = 'localhost'
            port = 1234
        else:
            d = pyautogui.confirm(text='', title='', buttons=[
                'Join room', 'Host room'])
            if d == 'Join room':
                ip = pyautogui.prompt(text='IP:', title='')
                port = int(pyautogui.prompt(text='PORT:', title=''))

            elif d == 'Host room':
                ip = 'localhost'
                port = int(pyautogui.prompt(text='PORT:', title=''))
                s = Server(port)
                threading.Thread(
                    target=s.main,
                    daemon=True
                ).start()
            else:
                exit()

        # create player
        # user = "Adin"
        p1 = Player(win, (np.size(grid, 0)+1)*tileSize//2,
                    (np.size(grid, 1)+1)*tileSize//2, world, user)
        self.players[p1.name] = p1

        self.client.connect(ip, port, self.players)
        self.client.initialize(p1.x, p1.y, p1.name, p1.color)

        # tell server the username and color

        # main pygame loop
        clock = pg.time.Clock()
        run = True
        while run:
            # Close window when X is clicked
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.VIDEORESIZE:
                    win = pg.display.set_mode(
                        size=(event.w, event.h), flags=(pg.DOUBLEBUF | pg.RESIZABLE))
                    old = tileSize
                    tileSize = event.w//25
                    if tileSize % 10:
                        tileSize -= tileSize % 10
                    maxVelocity *= (tileSize/old)
                    accel *= (tileSize/old)
                    deAccel *= (tileSize/old)
                    for player in self.players.values():
                        player.newScreenSize()

            keys = pg.key.get_pressed()

            # in game
            win.fill((0, 0, 0))

            # movement mechanics
            if keys[pg.K_w] and p1.dy > -maxVelocity:
                p1.dy -= accel
            if keys[pg.K_s] and p1.dy < maxVelocity:
                p1.dy += accel
            if not (keys[pg.K_w] or keys[pg.K_s]):
                if p1.dy < -deAccel:
                    p1.dy += deAccel
                elif p1.dy > deAccel:
                    p1.dy -= deAccel
                else:
                    p1.dy = 0

            if keys[pg.K_a] and p1.dx > -maxVelocity:
                p1.dx -= accel
            if keys[pg.K_d] and p1.dx < maxVelocity:
                p1.dx += accel
            if not (keys[pg.K_a] or keys[pg.K_d]):
                if p1.dx < -deAccel:
                    p1.dx += deAccel
                elif p1.dx > deAccel:
                    p1.dx -= deAccel
                else:
                    p1.dx = 0

            world.update(p1)

            # render tiles
            colors = grid.copy()
            lumApply = np.zeros((np.size(grid, 0), np.size(grid, 1), 3))
            try:
                for player in self.players.values():
                    slice1 = max(0, player.y//tileSize-renderDistance //
                                 2), min(np.size(grid, 0), player.y//tileSize+renderDistance//2)
                    slice2 = max(0, player.x//tileSize-renderDistance //
                                 2), min(np.size(grid, 1), player.x//tileSize+renderDistance//2)
                    lumApply[slice1[0]: slice1[1], slice2[0]: slice2[1]] += luminocity[player.y % tileSize // (tileSize//10), player.x % tileSize // (
                        tileSize//10)]*(luminocity[player.y % tileSize // (tileSize//10), player.x % tileSize // (tileSize//10)]+np.asarray(player.color)/255)/2
            except Exception as e:
                print(e)
            slice1 = max(0, p1.y//tileSize-renderDistance //
                         2), min(np.size(grid, 0), p1.y//tileSize+renderDistance//2)
            slice2 = max(0, p1.x//tileSize-renderDistance //
                         2), min(np.size(grid, 1), p1.x//tileSize+renderDistance//2)
            colors[slice1[0]: slice1[1], slice2[0]: slice2[1]
                   ] *= lumApply[slice1[0]: slice1[1], slice2[0]: slice2[1]]
            colors[slice1[0]: slice1[1], slice2[0]: slice2[1]] = np.minimum(np.ones(
                colors[slice1[0]: slice1[1], slice2[0]: slice2[1]].shape)*255, colors[slice1[0]: slice1[1], slice2[0]: slice2[1]])

            for i in range(max(0, p1.x//tileSize-renderDistance//2), min(np.size(grid, 1), p1.x//tileSize+renderDistance//2)):
                for j in range(max(0, p1.y//tileSize-renderDistance//2), min(np.size(grid, 0), p1.y//tileSize+renderDistance//2)):
                    # final = min(255,luminocity[j,i,0]*colors[j,i,0]),min(255,luminocity[j,i,1]*colors[j,i,1]),min(255,luminocity[j,i,2]*colors[j,i,2])
                    # pg.draw.rect(win, final, (world.x+i*tileSize,world.y+j*tileSize,tileSize,tileSize))
                    # print(colors)
                    pg.draw.rect(win, (colors[j, i, 0], colors[j, i, 1], colors[j, i, 2]), (
                        world.x+i*tileSize, world.y+j*tileSize, tileSize, tileSize))
                    # win.blit(wall1, (world.x+i*tileSize,world.y+j*tileSize))
            # print(len(self.players))
            for player in self.players.values():
                player.update()

            # send position
            self.client.toSend.put(
                (('update-coords', intToShort(p1.x)+intToShort(p1.y)), {'header': False}))

            # release client sender
            with self.client.condition:
                self.client.condition.notify()

            pg.display.update()
            clock.tick(60)
            # print(clock.get_fps())

        pg.quit()


def distance(p1, p2):
    dx = abs(p2[0]-p1[0])
    dy = abs(p2[1]-p1[1])
    d = (dx**2+dy**2)**(1/2)
    return d


def generateMap():
    mm = MapMaker()
    defaultScale = 2
    defaultWidth = 5
    defaultHeight = 5
    mainGrid = mm.makeGrid(defaultWidth, defaultHeight)
    mm.selectNextPath(mainGrid, 0, 0, [])
    for i in range(defaultWidth*defaultHeight//15):
        mm.removeRandomWall(mainGrid, r.randint(
            0, defaultWidth-1), r.randint(0, defaultHeight-1))
    mm.makePNG(mm.drawGrid(mainGrid, defaultScale))


def intToShort(x: int) -> Union[bytes, bytearray]:
    return int.to_bytes(x, 2, 'big')


def shortToInt(x: Union[bytes, bytearray]) -> int:
    return int.from_bytes(x, 'big')
