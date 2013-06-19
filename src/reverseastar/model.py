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
        
    def getNumRows(self):
        return self._NUM_ROWS
    
    def getNumColumns(self):
        return self._NUM_COLS
    
    def reset(self, density):
        self._data.clear()
        
        #Randomly set all cells in the world to an obstacle or not
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if random.random() < density:
                    self._addObstacle(row, col)

        unedited = copy.deepcopy(self._data)

        #Now try to clump together obstacles or free paths
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                obstacleNeighborCnt = self._countObstacleNeighbors(unedited, row, col)
                if obstacleNeighborCnt > 3:
                    self._addObstacle(row, col)
                elif obstacleNeighborCnt < 2:
                    self._clearObstacle(row, col)
                    
                    
    def _countObstacleNeighbors(self, data, row, col):
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