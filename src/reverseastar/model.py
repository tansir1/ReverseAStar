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
        self._data.clear()
        
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if random.random() < density:
                    
                    rowData = None
                    if row in self._data:
                        rowData = self._data[row]
                    else:
                        rowData = {}
                        self._data[row] = rowData
                    
                    cell = None
                    if col in self._data:
                        cell = rowData[col]
                    else:
                        cell = WorldCell()
                        cell.row = row
                        cell.column = col
                        rowData[col] = cell
                    
    def isObstacle(self, row, col):
        blocked = False
        if row in self._data:
            rowData = self._data[row]
            if col in rowData:
                cell = rowData[col]
                if cell != None:
                    blocked = True
        return blocked