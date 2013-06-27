from PySide.QtCore import *
from PySide.QtGui import *


class MainWindow(object):
    '''
    Contains the implementation for building and displaying the 
    application's main window.
    '''

    def __init__(self, model, alg):
        self._window = QMainWindow()
        self._window.setWindowTitle("Reverse A*")
        self._worldWidget = WorldWidget(model, alg)
        self._model = model
        self._alg = alg
        self._spdSetting = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._onStep)        
        self._buildGUI()
        self._window.show()

    def _buildGUI(self):
        centerWidget = QWidget()
        self._window.setCentralWidget(centerWidget)
        
        worldLayout = QHBoxLayout()
        worldLayout.addWidget(self._worldWidget)
        grpBx = QGroupBox("2D World")
        grpBx.setLayout(worldLayout)
        grpBx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        ctrlPan = self._buildControlPanel()
        layout = QHBoxLayout()
        layout.addWidget(ctrlPan)
        layout.addWidget(grpBx)
        layout.setAlignment(ctrlPan, Qt.AlignLeft | Qt.AlignTop)
        centerWidget.setLayout(layout)

        
    def _buildControlPanel(self):
        layout = QVBoxLayout()
        layout.addWidget(self._buildSetupPanel())
        layout.addWidget(self._buildSpeedPanel())
        layout.addWidget(self._buildResultsPanel())
        layout.addWidget(self._buildRenderingOptions())
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        #grpBx = QGroupBox("Controls")
        #grpBx.setLayout(layout)
        #return grpBx
        #grpBx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        ctrlWidget = QWidget(self._window)
        ctrlWidget.setLayout(layout)
        ctrlWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return ctrlWidget        
    
    def _buildSetupPanel(self):
        self._percentLbl = QLabel("%")
        self._setupBtn = QPushButton("Setup", self._window)
        self._setupBtn.clicked.connect(self._onSetup)
        
        self._percentObstacleSldr = QSlider(Qt.Horizontal, self._window)
        self._percentObstacleSldr.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._percentObstacleSldr.setTickInterval(10)
        self._percentObstacleSldr.setMinimum(0)
        self._percentObstacleSldr.setMaximum(100)
        self._percentObstacleSldr.valueChanged.connect(self._onPercentSlideChange)
        self._percentObstacleSldr.setValue(33)
        
        layout = QGridLayout()
        layout.addWidget(self._setupBtn, 0, 0, 1, 2)
        layout.addWidget(QLabel("Percent Occupied:"), 1, 0)
        layout.addWidget(self._percentLbl, 1, 1)
        layout.addWidget(self._percentObstacleSldr, 2, 0, 1, 2)
        
        grpBx = QGroupBox("Setup Controls")
        grpBx.setLayout(layout)
        grpBx.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return grpBx        
        
    def _buildSpeedPanel(self):
        self._runBtn = QPushButton("Run", self._window)
        self._stepBtn = QPushButton("Step Once", self._window)        
        self._runBtn.clicked.connect(self._onRun)
        self._stepBtn.clicked.connect(self._onStep)        
        
        slowRadio = QRadioButton('Slow', self._window)
        medRadio = QRadioButton('Medium', self._window)
        fastRadio = QRadioButton('Fast', self._window)
        notVisRadio = QRadioButton('Not visible', self._window)
        slowRadio.setChecked(True)        
        
        self._speedGroup = QButtonGroup(self._window)
        self._speedGroup.addButton(slowRadio, 0)
        self._speedGroup.addButton(medRadio, 1)
        self._speedGroup.addButton(fastRadio, 2)
        self._speedGroup.addButton(notVisRadio, 3)
        self._speedGroup.buttonClicked.connect(self._onSpeedChange)
          
        layout = QVBoxLayout()
        layout.addWidget(self._runBtn)
        layout.addWidget(self._stepBtn)
        layout.addWidget(slowRadio)
        layout.addWidget(medRadio)
        layout.addWidget(fastRadio)
        layout.addWidget(notVisRadio)
        
        grpBx = QGroupBox("Run Controls")
        grpBx.setLayout(layout)
        grpBx.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return grpBx
    
    def _buildResultsPanel(self):
        self._doneLbl = QLabel("No", self._window)
        self._solvableLbl = QLabel("Yes", self._window)
        
        pal = self._doneLbl.palette()
        pal.setColor(QPalette.Window, Qt.green)
        self._doneLbl.setPalette(pal)

        pal = self._solvableLbl.palette()
        pal.setColor(QPalette.Window, Qt.red)
        self._solvableLbl.setPalette(pal)          
        
        layout = QGridLayout()
        layout.addWidget(QLabel("Path Found:"), 0, 0)
        layout.addWidget(self._doneLbl, 0, 1)
        layout.addWidget(QLabel("Is Solvable:"), 1, 0)
        layout.addWidget(self._solvableLbl, 1, 1)
        
        grpBx = QGroupBox("Results")
        grpBx.setLayout(layout)
        grpBx.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return grpBx
    
    def _buildRenderingOptions(self):
        self._openChk = QCheckBox("Active Cells")
        self._visitedChk = QCheckBox("Visited Cells")
        self._pathChk = QCheckBox("Draw Path")
        self._costChk = QCheckBox("Draw Estimated Costs")
        
        pal = self._openChk.palette()
        pal.setColor(QPalette.WindowText, Qt.green)
        self._openChk.setPalette(pal)
        
        pal = self._visitedChk.palette()
        pal.setColor(QPalette.WindowText, Qt.cyan)
        self._visitedChk.setPalette(pal)
        
        pal = self._pathChk.palette()
        pal.setColor(QPalette.WindowText, Qt.red)
        self._pathChk.setPalette(pal)
        
        self._visitedChk.setChecked(True)
        self._pathChk.setChecked(True)
        self._costChk.setChecked(True)
        
        self._openChk.stateChanged.connect(self._renderingOptionChanged)
        self._visitedChk.stateChanged.connect(self._renderingOptionChanged)
        self._pathChk.stateChanged.connect(self._renderingOptionChanged)
        self._costChk.stateChanged.connect(self._renderingOptionChanged)
        
        layout = QVBoxLayout()
        layout.addWidget(self._openChk)
        layout.addWidget(self._visitedChk)
        layout.addWidget(self._pathChk)
        layout.addWidget(self._costChk)
        
        grpBx = QGroupBox("Rendering Options")
        grpBx.setLayout(layout)
        grpBx.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return grpBx        
    
    @Slot()
    def _renderingOptionChanged(self, value):
        self._worldWidget.setDrawActiveCells(self._openChk.isChecked())
        self._worldWidget.setDrawVisitedCells(self._visitedChk.isChecked())
        self._worldWidget.setDrawPath(self._pathChk.isChecked())
        self._worldWidget.setDrawCosts(self._costChk.isChecked())
        self._worldWidget.repaint()
    
    @Slot()
    def _onPercentSlideChange(self, value):
        #Add extra padding to the front of the string to help prevent
        #gui layout resizing
        if value < 10:
            self._percentLbl.setText("  " + str(value) + "%")
        elif value < 100:
            self._percentLbl.setText(" " + str(value) + "%")
        else:
            self._percentLbl.setText(str(value) + "%")
    
    @Slot()
    def _onSpeedChange(self, value):
        self._spdSetting = self._speedGroup.checkedId()
        if self._timer.isActive():
            self._resetTimer()            
         
    @Slot()
    def _onSetup(self):
        self._timer.stop()
        self._runBtn.setText('Run')
        self._model.reset(self._percentObstacleSldr.value() / 100.0)
        self._alg.reset()
        self._doneLbl.setText("No")
        self._solvableLbl.setText("Yes")
        self._doneLbl.setAutoFillBackground(False)
        self._solvableLbl.setAutoFillBackground(False)
        self._worldWidget.repaint()
    
    @Slot()
    def _onRun(self):
        if self._timer.isActive():
            self._timer.stop()
            self._runBtn.setText("Run")
        else:
            self._resetTimer()
            self._runBtn.setText("Stop")
    
    @Slot()
    def _onStep(self):
        self._alg.step()
        self._worldWidget.repaint()
        
        if self._alg.isDone() or not self._alg.isSolvable():
            self._timer.stop()
            self._runBtn.setText('Run')
        
        self._checkTerminalConditions()
            
    def _checkTerminalConditions(self):
        if self._alg.isDone():
            self._doneLbl.setText("Yes")
            self._doneLbl.setAutoFillBackground(True)

        if not self._alg.isSolvable():
            self._solvableLbl.setAutoFillBackground(True)
            self._solvableLbl.setText("No")

    def _resetTimer(self):
        if self._spdSetting == 3:
            while not self._alg.isDone() and self._alg.isSolvable():
                self._alg.step()
                
            self._worldWidget.repaint()
            self._timer.stop()
            self._runBtn.setText("Run")
            
            self._checkTerminalConditions()            
        else:
            timeOut = 1
            if self._spdSetting == 0:
                timeOut = 500
            elif self._spdSetting == 1:
                timeOut = 250
            elif self._spdSetting == 2:
                timeOut = 1            
            self._timer.start(timeOut)

class WorldWidget(QWidget):
        
    def __init__(self, model, alg):
        super(WorldWidget, self).__init__()
        self._NUM_COLS = model.getNumColumns()
        self._NUM_ROWS = model.getNumRows()
        self._GRID_SIZE = 1
        self.setMinimumSize(400,200)
        self._model = model
        self._alg = alg
        self._drawActive = False
        self._drawVisited = True
        self._drawCheapestPath = True
        self._drawCosts = True
    
    def setDrawActiveCells(self, doDraw):
        self._drawActive = doDraw
        
    def setDrawVisitedCells(self, doDraw):
        self._drawVisited = doDraw
        
    def setDrawPath(self, doDraw):
        self._drawCheapestPath = doDraw
        
    def setDrawCosts(self, doDraw):
        self._drawCosts = doDraw
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        width = self.width()
        height = self.height()
        
        #Blank out the world
        painter.fillRect(0, 0, width, height, Qt.white)

        #Compute width/height of the columns and rows
        
        #Reserve pixels for the grid lines
        colWidth = (width - (self._NUM_COLS - 1) * self._GRID_SIZE) / self._NUM_COLS
        rowHeight = (height - (self._NUM_ROWS - 1) * self._GRID_SIZE) / self._NUM_ROWS
        
        colWidth = max(1, colWidth)
        rowHeight = max(1, rowHeight)

        self._drawGrid(width, height, colWidth, rowHeight, painter)
        self._drawObstacles(colWidth, rowHeight, painter)
        if self._drawVisited:
            self._drawVisitedCells(colWidth, rowHeight, painter)
        if self._drawActive:
            self._drawActiveCells(colWidth, rowHeight, painter)
        self._drawStartAndEndCells(colWidth, rowHeight, painter)
        self._drawCurrentCell(colWidth, rowHeight, painter)
        if self._drawCheapestPath:
            self._drawPath(colWidth, rowHeight, painter)
        
        painter.end()

    def _drawObstacles(self, colWidth, rowHeight, painter):
        '''
        Fills in all obstacle cells as fully black.
        '''
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if self._model.getCell(row, col).isObstacle():
                    painter.fillRect(col * (colWidth + self._GRID_SIZE),
                                     row * (rowHeight + self._GRID_SIZE),
                                     colWidth, rowHeight, QColor('black'))
        
    def _drawGrid(self, width, height, colWidth, rowHeight, painter):
        '''
        Draws the grid lines over the 2D world.
        '''
        painter.drawRect(0, 0, width-1, height-1)
        
        #Paint the grid lines
        brush = QBrush(QColor('black'))
        painter.setBrush(brush)
        
        for row in range(0, self._NUM_ROWS):
            painter.drawLine(1, row * (rowHeight + self._GRID_SIZE),
                             width, row * (rowHeight + self._GRID_SIZE))

            for col in range(1, self._NUM_COLS):
                painter.drawLine(col * (colWidth + self._GRID_SIZE), 0,
                             col * (colWidth + self._GRID_SIZE), height)
                
    def _drawStartAndEndCells(self, colWidth, rowHeight, painter):
        '''
        Fills the algorithm's starting cell as fully green and ending cell
        as fully red.
        '''           
        start = self._model.getStartCell()
        end = self._model.getEndCell()
        
        if start != None:
            painter.fillRect(start.column * (colWidth + self._GRID_SIZE),
                             start.row * (rowHeight + self._GRID_SIZE),
                             colWidth, rowHeight, Qt.darkGreen)

        if end != None:
            painter.fillRect(end.column * (colWidth + self._GRID_SIZE),
                             end.row * (rowHeight + self._GRID_SIZE),
                             colWidth, rowHeight, Qt.red)
            
    def _drawVisitedCells(self, colWidth, rowHeight, painter):
        '''
        Fills the algorithm's visited/non-active cells as fully blue.
        '''         
        visited = self._alg.getVisitedCells()
        
        if visited != None:
            for cell in visited:
                painter.fillRect(cell.column * (colWidth + self._GRID_SIZE),
                                 cell.row * (rowHeight + self._GRID_SIZE),
                                 colWidth, rowHeight, Qt.cyan)
                
                if self._drawCosts:
                #Draw the estimated cost value of the current cell
                    textLoc = QPoint((cell.column + .1) * (colWidth + self._GRID_SIZE), 
                                 #Row + 3/4 of a row so that text is in the cell
                                 (cell.row + .75) * (rowHeight + self._GRID_SIZE))
                    if self._drawCosts:
                        painter.drawText(textLoc, "{0:.3g}".format(cell.estimatedPathCostToCell))                

    def _drawActiveCells(self, colWidth, rowHeight, painter):
        '''
        Fills the algorithm's active cells as fully green.
        '''        
        visited = self._alg.getActiveCells()
        
        if visited != None:
            for cell in visited:
                painter.fillRect(cell.column * (colWidth + self._GRID_SIZE),
                                 cell.row * (rowHeight + self._GRID_SIZE),
                                 colWidth, rowHeight, Qt.green)
                if self._drawCosts:
                    #Draw the estimated cost value of the current cell
                    textLoc = QPoint((cell.column + .1) * (colWidth + self._GRID_SIZE), 
                                 #Row + 3/4 of a row so that text is in the cell
                                 (cell.row + .75) * (rowHeight + self._GRID_SIZE))
                    painter.drawText(textLoc, "{0:.3g}".format(cell.estimatedPathCostToCell))
                
    def _drawCurrentCell(self, colWidth, rowHeight, painter):
        '''
        Fills the "current" cell as fully yellow.
        '''
        curCell = self._alg.getCurrentCell()
        
        if curCell != None:
            painter.fillRect(curCell.column * (colWidth + self._GRID_SIZE),
                             curCell.row * (rowHeight + self._GRID_SIZE),
                             colWidth, rowHeight, Qt.yellow)
            
            if self._drawCosts:
                #Draw the estimated cost value of the current cell
                textLoc = QPoint((curCell.column + .1) * (colWidth + self._GRID_SIZE), 
                             #Row + 3/4 of a row so that text is in the cell
                             (curCell.row + .75) * (rowHeight + self._GRID_SIZE))
                painter.drawText(textLoc, "{0:.3g}".format(curCell.estimatedPathCostToCell))
            
    def _drawPath(self, colWidth, rowHeight, painter):
        '''
        Draws the cheapest path from the start cell to the current cell.
        '''
        curCell = self._alg.getCurrentCell()
        
        if curCell != None:
            prevCell = curCell.prevCellInPath
            while prevCell != None:
                prevCenter = QPoint((prevCell.column + .5) * (colWidth + self._GRID_SIZE), 
                             #Row + 3/4 of a row so that text is in the cell
                             (prevCell.row + .5) * (rowHeight + self._GRID_SIZE))
                curCenter = QPoint((curCell.column + .5) * (colWidth + self._GRID_SIZE), 
                             #Row + 3/4 of a row so that text is in the cell
                             (curCell.row + .5) * (rowHeight + self._GRID_SIZE))
                
                #Paint line drawing a path from start to current/finish
                painter.setPen(Qt.red)
                painter.drawLine(prevCenter, curCenter)
                
                #Reset for next loop iteration
                curCell = prevCell
                prevCell = curCell.prevCellInPath
