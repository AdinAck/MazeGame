import png
from PIL import Image
import numpy as np
import random as r



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
        im = Image.fromarray(np.uint8(array))
        im.save("mapTest.png")

    def makeGrid(self,width,height):
        return [[Cell(i,j) for i in range(width)] for j in range(height)]

    def getUnvisitedNeighbors(self, grid, cell):
        left = cell.x==0
        right = cell.x==len(grid[0])-1
        top = cell.y==0
        bottom = cell.y==len(grid)-1
        #print(left, right, top, bottom)

        unvisited = []
        if not left:
            #print(grid[cell.y][cell.x-1].visited)
            if not grid[cell.y][cell.x-1].visited:
                unvisited.append(grid[cell.y][cell.x-1])
                #print(f"Appending to unvisited: {str(grid[cell.y][cell.x-1])}")
        if not right:
            #print(grid[cell.y][cell.x+1].visited)
            if not grid[cell.y][cell.x+1].visited:
                unvisited.append(grid[cell.y][cell.x+1])
                #print(f"Appending to unvisited: {str(grid[cell.y][cell.x+1])}")
        if not top:
            #print(grid[cell.y-1][cell.x].visited)
            if not grid[cell.y-1][cell.x].visited:
                unvisited.append(grid[cell.y-1][cell.x])
                #print(f"Appending to unvisited: {str(grid[cell.y-1][cell.x])}")
        if not bottom:
            #print(grid[cell.y+1][cell.x].visited)
            if not grid[cell.y+1][cell.x].visited:
                unvisited.append(grid[cell.y+1][cell.x])
                #print(f"Appending to unvisited: {str(grid[cell.y+1][cell.x])}")
        #print(f"unvisited len = {len(unvisited)}")
        #print("Unvisited Appending: ")
        #[print(str(i)) for i in unvisited]
        return unvisited

    def selectNextPath(self, grid, currentX, currentY, uncheckedCells):
        #print(f"unchecked len = {len(uncheckedCells)}")
        #print("UncheckedList: ")
        #[print(str(i)) for i in uncheckedCells]
        currentCell = grid[currentY][currentX]
        #print(f"currentCell: {str(currentCell)}")
        currentCell.visited = True
        unvisitedList = self.getUnvisitedNeighbors(grid, currentCell)
        #print("Unvisited: ")
        #[print(str(i)) for i in unvisitedList]
        if len(uncheckedCells)>1000:
            return
        if len(unvisitedList) > 0:
            random = unvisitedList[r.randint(0,len(unvisitedList)-1)]
            #print("Random one used: ")
            #print(str(random))
            if not random.visited:
                #print("hello")
                uncheckedCells.append(random)
            #print("UncheckedList: ")
            #[print(str(i)) for i in uncheckedCells]
            #print(f"Removing walls between {str(random)} and {str(currentCell)}")
            self.removeWalls(random, currentCell)
            currentCell = random
            self.selectNextPath(grid, currentCell.x, currentCell.y, uncheckedCells)
        elif len(uncheckedCells) != 0:
            popped = uncheckedCells[-1]
            uncheckedCells.pop()
            #print(f"unchecked{len(uncheckedCells)}")
            currentCell = popped
            self.selectNextPath(grid, currentCell.x, currentCell.y, uncheckedCells)


    def removeWalls(self, cell1, cell2):
        x1 = cell1.x
        y1 = cell1.y
        x2 = cell2.x
        y2 = cell2.y
        #print(x1,y1,x2,y2)

        if x1==x2:
            if (y1+1)==y2:
                cell1.southWall = False
                cell2.northWall = False
                #print("up down")
            if (y1-1)==y2:
                cell1.northWall = False
                cell2.southWall = False
                #print("down up")
        if y1==y2:
            if (x1-1)==x2:
                cell1.westWall = False
                cell2.eastWall = False
                #print("right left")
            if (x1+1)==x2:
                cell1.eastWall = False
                cell2.westWall = False
                #print("left right")

    #scale is the distance between walls
    def drawGrid(self, grid, scale):
        scale+=1
        width = scale*len(grid)+1
        height = scale*len(grid[0])+1
        map = np.zeros((width,height))



        for r in range(len(grid)):
            for c in range(len(grid[0])):
                k = grid[r][c]
                if k.northWall:
                    map[scale*r,scale*c+1:scale*c+scale] = 1
                if k.southWall:
                    map[scale*r+scale,scale*c+1:scale*c+scale] = 1
                if k.westWall:
                    map[scale*r+1:scale*r+scale,scale*c] = 1
                if k.eastWall:
                    map[scale*r+1:scale*r+scale,scale*c+scale] = 1

        for r in range(np.size(map,0)):
            for c in range(np.size(map,1)):
                if r%scale == 0 and c%scale ==0:
                    isIsolated = True
                    if r!=0:
                        if map[r-1,c]!=0:
                            isIsolated = False
                    if c!=0:
                        if map[r,c-1]!=0:
                            isIsolated = False
                    if r!=np.size(map,0)-1:
                        if map[r+1,c]!=0:
                            isIsolated = False
                    if c!=np.size(map,1)-1:
                        if map[r,c+1]!=0:
                            isIsolated = False
                    if not isIsolated:
                        map[r,c] = 1

        return map

    def removeRandomWall(self, grid, cellx, celly):
        cell = grid[celly][cellx]
        possibleCells = []
        if celly != len(grid)-1:
            if cell.southWall:
                possibleCells.append(grid[celly+1][cellx])
        if cellx != len(grid[0])-1:
            if cell.eastWall:
                possibleCells.append(grid[celly][cellx+1])
        if celly != 0:
            if cell.northWall:
                possibleCells.append(grid[celly-1][cellx])
        if cellx != 0:
            if cell.westWall:
                possibleCells.append(grid[celly][cellx-1])
        if len(possibleCells):
            firstCell = grid[celly][cellx]
            otherCell = possibleCells[r.randint(0,len(possibleCells)-1)]
            self.removeWalls(firstCell,otherCell)



class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.northWall = True
        self.southWall = True
        self.eastWall = True
        self.westWall = True

    def __str__(self):
        return f"x: {self.x} y: {self.y} visited: {self.visited}"





mm = MapMaker()
defaultScale = 2
# Current Maximum total Cell count is 499
defaultWidth = 21
defaultHeight = 21
mainGrid = mm.makeGrid(defaultWidth,defaultHeight)
mm.selectNextPath(mainGrid, 0, 0, [])
for i in range(defaultWidth*defaultHeight//15):
    mm.removeRandomWall(mainGrid, r.randint(0,defaultWidth-1), r.randint(0,defaultHeight-1))
# [[print(str(j)) for j in i] for i in mainGrid]
mm.makePNG(mm.drawGrid(mainGrid,defaultScale))
