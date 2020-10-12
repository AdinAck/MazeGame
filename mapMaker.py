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
        for i in range(np.size(map,0)):
            for j in range(np.size(map,1)):
                if map[j,i] == 1:
                    array[j,i] = [255,255,255]
                if map[j,i] == 0:
                    array[j,i] = [0,0,0]
        print(array)
        im = Image.fromarray(np.uint8(array))
        im.save("mapTest.png")

    def makeGrid(self,width,height):
        return [[Cell() for i in range(width)] for i in range(height)]

    # def fillCorners(x,y):
    #     if x%3 == 0 and y%3 == 0:
    #         return 1
    #     return 0

    def drawGrid(self, grid):
        width = 3*len(grid)+1
        height = 3*len(grid[0])+1
        map = np.zeros((width,height))

        # corners = np.vectorize(MapMaker.fillCorners)
        # corners(map)

        for i in range(np.size(map,0)):
            for j in range(np.size(map,1)):
                if i%3 == 0 and j%3 ==0:
                    map[j,i] = 1

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                k = grid[j][i]
                if k.northWall:
                    map[3*i,3*j+1] = 1
                    map[3*i,3*j+2] = 1
                if k.southWall:
                    map[3*i+3,3*j+1] = 1
                    map[3*i+3,3*j+2] = 1
                if k.westWall:
                    map[3*j+1,3*i] = 1
                    map[3*j+2,3*i] = 1
                if k.eastWall:
                    map[3*j+1,3*i+3] = 1
                    map[3*j+2,3*i+3] = 1


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
mm.makePNG(mm.drawGrid(mm.makeGrid(10,10)))
