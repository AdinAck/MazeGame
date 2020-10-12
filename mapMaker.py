import png
from PIL import Image
import numpy as np



class MapMaker:
    def __init__(self):
        print("making mapMaker")


    def testMethod(self):
        s=[[1,2,1],[1,2,1],[0,1,0]]
        palette=[(0x55,0x55,0x55), (0xff,0x99,0x99), (0xf4,0x92,0x11)]
        w = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=2)

        f = open('mapTest.png','wb')
        w.write(f,s)
        f.close()

    def makePNG(self,map):
        array = np.zeros((np.size(map,0),np.size(map,1),3))
        for r in range(np.size(map,0)):
            for c in range(np.size(map,1)):
                if map[r,c] == 1:
                    array[r,c] = [255,255,255]
                if map[r,c] == 0:
                    array[r,c] = [0,0,0]
        print(array)
        im = Image.fromarray(np.uint8(array))
        im.save("mapTest.png")

    def makeGrid(self,width,height):
        return [[Cell() for i in range(width)] for i in range(height)]

    #scale is the distance between walls
    def drawGrid(self, grid, scale):
        scale+=1
        width = scale*len(grid)+1
        height = scale*len(grid[0])+1
        map = np.zeros((width,height))

        for r in range(np.size(map,0)):
            for c in range(np.size(map,1)):
                if r%scale == 0 and c%scale ==0:
                    map[r,c] = 1

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                k = grid[r][c]
                i = r
                j = c
                # if k.northWall:
                #     map[scale*r,scale*c+1] = 1
                #     map[scale*r,scale*c+2] = 1
                # if k.southWall:
                #     map[scale*r+scale,scale*c+1] = 1
                #     map[scale*r+scale,scale*c+2] = 1
                # if k.westWall:
                #     map[scale*r+1,scale*c] = 1
                #     map[scale*r+2,scale*c] = 1
                # if k.eastWall:
                #     map[scale*r+1,scale*c+scale] = 1
                #     map[scale*r+2,scale*c+scale] = 1

                if k.northWall:
                    map[scale*r,scale*c+1:scale*c+scale] = 1
                if k.southWall:
                    map[scale*r+scale,scale*c+1:scale*c+scale] = 1
                if k.westWall:
                    map[scale*r+1:scale*r+scale,scale*c] = 1
                if k.eastWall:
                    map[scale*r+1:scale*r+scale,scale*c+scale] = 1

        print(map)
        return map


class Cell:
    def __init__(self):
        self.visited = False
        self.northWall = True
        self.southWall = True
        self.eastWall = True
        self.westWall = True






mm = MapMaker()
defaultScale = 2
defaultWidth = 5
defaultHeight = 7
mm.makePNG(mm.drawGrid(mm.makeGrid(defaultWidth,defaultHeight),defaultScale))
