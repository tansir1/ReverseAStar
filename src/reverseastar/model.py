import random

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
        self._NUM_COLS = 10
        self._NUM_ROWS = 10
        self._data = {}
        
    def getNumRows(self):
        return self._NUM_ROWS
    
    def getNumColums(self):
        return self._NUM_COLS
    
    def reset(self, density):
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if random.random() < density:
                    rowData = self._data[row]
                    if rowData == None:
                        rowData = {}
                        self._data[row] = rowData
                    
                    colData = rowData[col]
                    if colData == None:
                        colData = {}
                        self._data[row][col] = colData
                        
                    cell = WorldCell()
                    cell.row = row
                    cell.column = col
                    self._data[row][col] = cell
                    
    def isObstacle(self, row, col):
        blocked = False
        rowData = self._data[row]
        if rowData != None:
            cell = rowData[col]
            if cell != None:
                blocked = True
        return blocked