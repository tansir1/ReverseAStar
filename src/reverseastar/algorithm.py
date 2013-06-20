from math import sqrt

class ReverseAStarAlgorithm(object):
    
    def __init__(self, model):
        self._worldModel = model
        self._closedSet = []
        self._openSet = []
        self._current = None
        
    def reset(self):
        self._closedSet = []
        self._openSet = []
        self._current = None
        self._worldModel.getStartCell().gScore = 0
        self._worldModel.getStartCell().fScore = 0 + self._heuristic(self._worldModel.getStartCell())
    
    def step(self):
        
        #Check if we still have cells to investigate
        if not self._openSet:
            self._current = self._lowestFscoreInOpenSet()
            if self._current == self._worldModel.getEndCell():
                pass
                #Bail out, time to start path reconstruction
                
            self._openSet.remove(self._current)
            self._closedSet.append(self._current)
            for neighbor in self._worldModel.getTraversableNeighbors(self._current.row, self._current.column):
                currentGScore = self._computeGScore(self._current) + self._distBetweenCells(self._current, neighbor)
                if neighbor in self._closedSet and currentGScore >= neighbor.gScore:
                    continue
                
                if neighbor not in self._openSet or currentGScore < neighbor.gScore:
                    #came_from[neighbor] = current
                    neighbor.gScore = currentGScore
                    neighbor.fScore = currentGScore + self._heuristic(neighbor)
                    if neighbor not in self._openSet:
                        self._openSet.append(neighbor)
    
    def _lowestFscoreInOpenSet(self):
        lowestCost = None
        
        for cell in self._openSet:
            if lowestCost == None:
                lowestCost = cell
            elif cell.fScore < lowestCost.fScore:
                lowestCost = cell
        
        return lowestCost
    
    def _heuristic(self, fromCell):
        #cost from fromCell to goal
        return 1 
    
    def _computeGScore(self, cell):
        pass
    
    def _distBetweenCells(self, src, dest):
        vert = src.row - dest.row
        horz = src.column - dest.column
        
        #Square and convert to floating point
        vert = vert * vert * 1.0
        horz = horz * horz * 1.0
        
        return sqrt(vert + horz)
    
    def getVisitedCells(self):
        self._closedSet
    
    def getCurrentCell(self):
        return self._current