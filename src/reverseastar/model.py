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

class WorldModel(object):
    
    def __init__(self):
        self._NUM_COLS = 33
        self._NUM_ROWS = 33
        self._data = {}
        self._startCell = None
        self._endCell = None
        
    def getNumRows(self):
        return self._NUM_ROWS
    
    def getNumColumns(self):
        return self._NUM_COLS
    
    def getStartCell(self):
        return self._startCell
    
    def getEndCell(self):
        return self._endCell
    
    def reset(self, density):
        self._data.clear()
        self._startCell = None
        self._endCell = None
        
        #Randomly set all cells in the world to an obstacle or not
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if random.random() < density:
                    self._addObstacle(row, col)

        unedited = copy.deepcopy(self._data)

        #Now try to clump together obstacles and free paths
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                obstacleNeighborCnt = self._countObstacleNeighbors(unedited, row, col)
                if obstacleNeighborCnt > 3:
                    self._addObstacle(row, col)
                elif obstacleNeighborCnt < 2:
                    self._clearObstacle(row, col)
                    
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
        
        print 'start {0},{1}'.format(start.row, start.column)
        print 'end {0},{1}'.format(end.row, end.column)
        
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
        
        #Check row above
        if self.isObstacle(row-1, col-1, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1
        if self.isObstacle(row-1, col, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1
        if self.isObstacle(row-1, col+1, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1
            
        #Check left and right sides
        if self.isObstacle(row, col-1, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1                        
        if self.isObstacle(row, col+1, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1
        
        #Check row below                
        if self.isObstacle(row+1, col-1, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1            
        if self.isObstacle(row+1, col, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1            
        if self.isObstacle(row+1, col+1, data):
            obstacleNeighborCnt = obstacleNeighborCnt + 1
            
        return obstacleNeighborCnt
                
    def _addObstacle(self, row, col):
        rowData = None
        if row in self._data:
            rowData = self._data[row]
        else:
            rowData = {}
            self._data[row] = rowData
        
        cell = None
        if col in rowData:
            cell = rowData[col]
        else:
            cell = WorldCell()
            cell.row = row
            cell.column = col
            rowData[col] = cell

    def _clearObstacle(self, row, col):
        if row in self._data:
            rowData = self._data[row]
            if col in rowData:
                del rowData[col]            
            
    def isObstacle(self, row, col, data = None):
        
        if data is None:
            data = self._data
        
        blocked = False
        if row in data:
            rowData = data[row]
            if col in rowData:
                cell = rowData[col]
                if cell != None:
                    blocked = True
        return blocked
    
    def isClear(self, row, col):
        blocked = self.isObstacle(row, col)
        return not blocked
    