from math import sqrt

class ReverseAStarAlgorithm(object):
    
    def __init__(self, model):
        self._worldModel = model
        self._closedSet = []
        self._openSet = []
        self._current = None
        self._done = False
        self._isSolvable = True
        
    def reset(self):
        self._closedSet = []
        self._openSet = []
        self._current = None
        self._worldModel.getStartCell().distanceTraveledToCell = 0
        self._worldModel.getStartCell().estimatedPathCostToCell = 0 + self._heuristic(self._worldModel.getStartCell())
        self._openSet.append(self._worldModel.getStartCell())
    
    def step(self):
        
        #Check if we still have cells to investigate
        if len(self._openSet) > 0 and not self._done:
            self._current = self._lowestEstimatedCost()
            if self._current == self._worldModel.getEndCell():
                self._done = True
                
            self._openSet.remove(self._current)
            self._closedSet.append(self._current)
            for neighbor in self._worldModel.getTraversableNeighbors(self._current.row, self._current.column):
                currentDist = self._current.distanceTraveledToCell + self._distBetweenCells(self._current, neighbor)
                if neighbor in self._closedSet and currentDist >= neighbor.distanceTraveledToCell:
                    continue
                
                if neighbor not in self._openSet or currentDist < neighbor.distanceTraveledToCell:
                    neighbor.prevCellInPath = self._current
                    neighbor.distanceTraveledToCell = currentDist
                    neighbor.estimatedPathCostToCell = currentDist + self._heuristic(neighbor)
                    if neighbor not in self._openSet:
                        self._openSet.append(neighbor)
        elif len(self._openSet) == 0 and not self._done:
            self._isSolvable = False
    
    def _lowestEstimatedCost(self):
        lowestCost = None
        
        for cell in self._openSet:
            if lowestCost == None:
                lowestCost = cell
            elif cell.estimatedPathCostToCell < lowestCost.estimatedPathCostToCell:
                lowestCost = cell
        
        return lowestCost
    
    def _heuristic(self, fromCell):
        return self._distBetweenCells(fromCell, self._worldModel.getEndCell())
        
    def _distBetweenCells(self, src, dest):
        vert = src.row - dest.row
        horz = src.column - dest.column
        
        #Square and convert to floating point
        vert = vert * vert * 1.0
        horz = horz * horz * 1.0
        
        return sqrt(vert + horz)
    
    def getVisitedCells(self):
        return self._closedSet
    
    def getActiveCells(self):
        return self._openSet
    
    def getCurrentCell(self):
        return self._current
    
    def isSolvable(self):
        return self._isSolvable
    
    def isDone(self):
        return self._done