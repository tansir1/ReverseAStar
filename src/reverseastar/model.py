import random
import copy

class WorldCell(object):
    '''
    Simple structure to hold the row and column coordinates
    of a world grid cell.
    '''
    
    def __init__(self):
        self._row = -1
        self._col = -1
        self._isObstacle = False
        self._distTraveled = 0.0
        self._pathCost = 0.0
        self._cameFrom = None
        
    @property
    def row(self):
        return self._row
    
    @row.setter
    def row(self, value):
        self._row = value
        
    @property
    def column(self):
        return self._col
    
    @column.setter
    def column(self, value):
        self._col = value
    
    #@property
    def isObstacle(self):
        return self._isObstacle
    
    #@isObstacle.setter
    def setObstacle(self, value):
        self._isObstacle = value
        
    @property
    def distanceTraveledToCell(self):
        return self._distTraveled
    
    @distanceTraveledToCell.setter
    def distanceTraveledToCell(self, value):
        self._distTraveled = value
        
    @property
    def estimatedPathCostToCell(self):
        return self._pathCost
    
    @estimatedPathCostToCell.setter
    def estimatedPathCostToCell(self, value):
        self._pathCost = value
    
    @property
    def prevCellInPath(self):
        return self._cameFrom
    
    @prevCellInPath.setter
    def prevCellInPath(self, value):
        self._cameFrom = value
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._col == other._col
                and self._row == other._row)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return '{0},{1},{2}'.format(self._row, self._col, self._isObstacle)

class WorldModel(object):
    
    def __init__(self):
        self._NUM_COLS = 33
        self._NUM_ROWS = 33
        self._data = {}
        self._startCell = None
        self._endCell = None
        self._resetWorldData()        
        
    def getNumRows(self):
        return self._NUM_ROWS
    
    def getNumColumns(self):
        return self._NUM_COLS
    
    def getStartCell(self):
        '''
        Get the starting point of the world for path finding.
        '''
        return self._startCell
    
    def getEndCell(self):
        '''
        Get the end point of the world for path finding.
        '''
        return self._endCell
    
    def _resetWorldData(self):
        self._data.clear()
        self._startCell = None
        self._endCell = None
        
        for row in range(0, self._NUM_ROWS):
            self._data[row] = {}
            for col in range(0, self._NUM_COLS):
                cell = WorldCell()
                cell.row = row
                cell.column = col
                self._data[row][col] = cell
                
    def reset(self, density):
        '''
        Create a new random 2D world with the given density of obstacles as the
        random seed for obstacle generation.  After the random generation this
        method will attempt to smooth out and cluster the obstacles and free
        paths.
        '''
        self._resetWorldData()
        
        #Randomly set all cells in the world to an obstacle or not
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if random.random() < density:
                    self._data[row][col].setObstacle(True)

        unedited = copy.deepcopy(self._data)

        #Now try to clump together obstacles and free paths
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                obstacleNeighborCnt = self._countObstacleNeighbors(unedited, row, col)
                if obstacleNeighborCnt > 3:
                    self._data[row][col].setObstacle(True)
                elif obstacleNeighborCnt < 2:
                    self._data[row][col].setObstacle(False)
                    
        # This searches for a suitable start cell in the lower left 13% of the grid
        # and an end patch in the upper right 13% of the grid. "Suitable" is defined 
        #as any cell with most neighbors unoccupied which is more likely than most
        # to have reachability
        xLimit = self._NUM_COLS / 8
        yLimit = self._NUM_ROWS / 8
        
        start = self._findOpenCell(xLimit, yLimit, self._NUM_ROWS - xLimit, 0)
        end = self._findOpenCell(xLimit, yLimit, 
                                 0, self._NUM_COLS - yLimit)
        
        while (start.row == -1 and start.column == -1 and 
               end.row == -1 and end.column == -1):
            self.reset(density)
        self._startCell = start
        self._endCell = end
        
    def _findOpenCell(self, xLimit, yLimit, row, col):
        '''
        Searches from coordinate row,col to row+xLimit,col+yLimit for the most
        uncrowded open cell.  If all cells are blocked then the cell returned
        here have a row,col coordinate of -1,-1.
        '''
        mostClearCell = WorldCell()
        #Worst case is all 8 neighbors cells are blocked
        lowestCnt = 8
        
        for x in range(row, row+xLimit):
            for y in range(col, col+yLimit):
                localCnt = self._countObstacleNeighbors(self._data, x, y)
                if localCnt < lowestCnt:
                    lowestCnt = localCnt
                    mostClearCell.row = x
                    mostClearCell.column = y
        return mostClearCell
                    
    def _countObstacleNeighbors(self, data, row, col):
        '''
        Checks the cells around a given location to count the number of obstacles
        around it.  Cells on the border of the world are treated as having clear
        neighbor cells beyond the border.
        '''
        obstacleNeighborCnt = 0
        neighbors = self.getNeighbors(row, col, data)
        for cell in neighbors:
            if cell.isObstacle():
                obstacleNeighborCnt = obstacleNeighborCnt + 1
            
        return obstacleNeighborCnt
    
    def getCell(self, row, col):
        return self._data[row][col]
    
    def getNeighbors(self, row, col, data = None):
        '''
        Gets all the valid (in world bounds) cells surrounding the specified cell.
        '''
        if data is None:
            data = self._data
      
        neighbors = []
        
        #Check row above
        if self._isValidCoordinate(row-1, col-1, data):
            neighbors.append(data[row-1][col-1])
        if self._isValidCoordinate(row-1, col, data):
            neighbors.append(data[row-1][col])
        if self._isValidCoordinate(row-1, col+1, data):
            neighbors.append(data[row-1][col+1])
            
        #Check left and right sides
        if self._isValidCoordinate(row, col-1, data):
            neighbors.append(data[row][col-1])                
        if self._isValidCoordinate(row, col+1, data):
            neighbors.append(data[row][col+1])
        
        #Check row below                
        if self._isValidCoordinate(row+1, col-1, data):
            neighbors.append(data[row+1][col-1])            
        if self._isValidCoordinate(row+1, col, data):
            neighbors.append(data[row+1][col])    
        if self._isValidCoordinate(row+1, col+1, data):
            neighbors.append(data[row+1][col+1])
        
        return neighbors

    def getTraversableNeighbors(self, row, col):
        '''
        Returns a list of all neighbors of the cell at given [row,col] that
        can be traveled across.
        '''
        neighbors = []
        up = None
        down = None
        left = None
        right = None
        
        #Check simple up/down/left/right directions
        if self._isValidCoordinate(row-1, col):
            up = self._data[row-1][col]
        if self._isValidCoordinate(row+1, col):
            down = self._data[row+1][col]    
        if self._isValidCoordinate(row, col-1):
            left = self._data[row][col-1]    
        if self._isValidCoordinate(row, col+1):
            right = self._data[row][col+1]    
            
        if up != None and not up.isObstacle():
            neighbors.append(up)
        if down != None and not down.isObstacle():
            neighbors.append(down)
        if left != None and not left.isObstacle():
            neighbors.append(left)
        if right != None and not right.isObstacle():
            neighbors.append(right)
            
        #Check if diagonals are traversable.  Only passable if one of the
        #component directions are clear.
        if up != None and left != None:
            if not (up.isObstacle() and left.isObstacle()) and not \
            self._data[row-1][col-1].isObstacle():
                neighbors.append(self._data[row-1][col-1])
        if up != None and right != None:
            if not (up.isObstacle() and right.isObstacle()) and not \
            self._data[row-1][col+1].isObstacle():
                neighbors.append(self._data[row-1][col+1])
        if down != None and left != None:
            if not (down.isObstacle() and left.isObstacle()) and not \
            self._data[row+1][col-1].isObstacle():
                neighbors.append(self._data[row+1][col-1])
        if down != None and right != None:
            if not (down.isObstacle() and right.isObstacle()) and not \
            self._data[row+1][col+1].isObstacle():
                neighbors.append(self._data[row+1][col+1])                                        
        
        return neighbors
            
    def _isValidCoordinate(self, row, col, data = None):
        '''
        Checks if the given coordinates are within bounds of the world.
        '''
        if data is None:
            data = self._data
        
        valid = True
        if row < 0 or row >= self._NUM_ROWS:
            valid = False
        if col < 0 or col >= self._NUM_COLS:
            valid = False
        return valid