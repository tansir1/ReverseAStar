from math import sqrt

class ReverseAStarAlgorithm(object):
    
    def __init__(self, model):
        self._worldModel = model
        self._closedSet = []
        self._openSet = []
        self._current = None
        self._done = False
        self._isSolvable = True
        self._startCell = None
        self._endCell = None
        
    def reset(self):
        '''
        Reset the algorithm to solve another world model.
        '''
        self._closedSet = []
        self._openSet = []
        self._current = None
        self._done = False
        self._isSolvable = True
        
        #Reverse A* is just like A*, but with the start and end cells swapped
        startCell = self._worldModel.getEndCell()
        self._endCell = self._worldModel.getStartCell()
        
        startCell.distanceTraveledToCell = 0
        startCell.estimatedPathCostToCell = 0 + self._heuristic(self._endCell)
        self._openSet.append(startCell)
    
    def step(self):
        '''
        Run a single iteration of the A* algorithm.  Will set the 'done' and
        'solvable' flags if needed at the end of each iteration.  This method
        does nothing if algorithm has already solved the world puzzle.
        '''
        #Check if we still have cells to investigate
        if len(self._openSet) > 0 and not self._done:
            self._current = self._lowestEstimatedCost()
            #Bail out of the algorithm if we find the goal
            if self._current == self._endCell:
                self._done = True
                
            #Move the currently estimated lowest cost path/cell from active to
            #inactive.
            self._openSet.remove(self._current)
            self._closedSet.append(self._current)
            
            #Compute path costs for all the traversable neighbors of the current cell 
            for neighbor in self._worldModel.getTraversableNeighbors(self._current.row, self._current.column):
                currentDist = self._current.distanceTraveledToCell + self._distBetweenCells(self._current, neighbor)
                
                #If the neighbor has already been investigated and our current
                #cost is greater, then this is not the optimal path. Bail out
                #early and try another neighbor.
                if neighbor in self._closedSet and currentDist >= neighbor.distanceTraveledToCell:
                    continue
                
                #If the neighbor is not active or our current path is cheaper than
                #the neighbor then we need to continue investigating this path.
                if neighbor not in self._openSet or currentDist < neighbor.distanceTraveledToCell:
                    neighbor.prevCellInPath = self._current
                    neighbor.distanceTraveledToCell = currentDist
                    neighbor.estimatedPathCostToCell = currentDist + self._heuristic(neighbor)
                    if neighbor not in self._openSet:
                        self._openSet.append(neighbor)
        elif len(self._openSet) == 0 and not self._done:
            #If we're not done and we have no more active cells then the
            #world puzzle isn't solvable.
            self._isSolvable = False
    
    def _lowestEstimatedCost(self):
        '''
        Examines the currently active cells and returns the cell with the lowest
        estimated cost to the goal.
        '''
        lowestCost = None
        
        for cell in self._openSet:
            if lowestCost == None:
                lowestCost = cell
            elif cell.estimatedPathCostToCell < lowestCost.estimatedPathCostToCell:
                lowestCost = cell
        
        return lowestCost
    
    def _heuristic(self, fromCell):
        '''
        A simple heuristic that just computes the distance from the given cell
        to the goal cell.
        '''
        return self._distBetweenCells(fromCell, self._worldModel.getEndCell())
        
    def _distBetweenCells(self, src, dest):
        '''
        Computes the cartesian distance (hypotenuse of a right triangle)
        between two cells.
        '''
        vert = src.row - dest.row
        horz = src.column - dest.column
        
        #Square and convert to floating point
        vert = vert * vert * 1.0
        horz = horz * horz * 1.0
        
        return sqrt(vert + horz)
    
    def getVisitedCells(self):
        '''
        Get a set of all the world cells that have been visited and fully
        explored.  These cells are no longer part of the active path search.
        '''
        return self._closedSet
    
    def getActiveCells(self):
        '''
        Get a set of all currently active cells that are part of the current
        path search.  These cells and their neighbors are not yet fully explored.
        '''
        return self._openSet
    
    def getCurrentCell(self):
        return self._current
    
    def isSolvable(self):
        '''
        Returns a boolean flag indicating if the algorithm believes the world
        model is still solvable.
        '''
        return self._isSolvable
    
    def isDone(self):
        '''
        Returns a boolean flag indicating if the algorithm has found a path from
        the start node to the end node.
        '''
        return self._done