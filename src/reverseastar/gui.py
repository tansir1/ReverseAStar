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
        self._setupBtn = QPushButton("Setup", self._window)
        self._runBtn = QPushButton("Go", self._window)
        self._stepBtn = QPushButton("Step Once", self._window)
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
        
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self._buildControlPanel(), 0, 0, 1, 1)
        layout.addWidget(grpBx, 0, 1, 1, 5)
        
        centerWidget.setLayout(layout)

        
    def _buildControlPanel(self):
        self._spdLbl = QLabel("Speed?")
        self._percentLbl = QLabel("%")
        
        self._setupBtn.clicked.connect(self._onSetup)
        self._runBtn.clicked.connect(self._onRun)
        self._stepBtn.clicked.connect(self._onStep)

        self._percentObstacleSldr = QSlider(Qt.Horizontal, self._window)
        self._percentObstacleSldr.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._percentObstacleSldr.setTickInterval(10)
        self._percentObstacleSldr.setMinimum(0)
        self._percentObstacleSldr.setMaximum(100)
        self._percentObstacleSldr.valueChanged.connect(self._onPercentSlideChange)
        self._percentObstacleSldr.setValue(33)

        self._spdSlider = QSlider(Qt.Horizontal, self._window)
        self._spdSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._spdSlider.setTickInterval(1)
        self._spdSlider.setMinimum(0)
        self._spdSlider.setMaximum(3)
        self._spdSlider.valueChanged.connect(self._onSpeedSlideChange)
        self._spdSlider.setValue(0)
        
        layout = QGridLayout()
        layout.addWidget(self._setupBtn, 0, 0)
        layout.addWidget(self._runBtn, 1, 0)
        layout.addWidget(self._stepBtn, 2, 0)
        
        layout.addWidget(QLabel("Percent Occupied:"), 3, 0)
        layout.addWidget(self._percentLbl, 3, 1)
        layout.addWidget(self._percentObstacleSldr, 4, 0, 1, 2)
        
        layout.addWidget(QLabel("Update speed:"), 5, 0)
        layout.addWidget(self._spdLbl, 5, 1)
        layout.addWidget(self._spdSlider, 6, 0, 1, 2)
        
        grpBx = QGroupBox("Controls")
        grpBx.setLayout(layout)
        #grpBx.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return grpBx
         
    @Slot()
    def _onPercentSlideChange(self, value):
        self._percentLbl.setText(str(value) + "%")
    
    @Slot()
    def _onSpeedSlideChange(self, value):
        self._spdSetting = value
        if value == 0:
            self._spdLbl.setText("Slow")
        elif value == 1:
            self._spdLbl.setText("Medium")            
        elif value == 2:
            self._spdLbl.setText("Fast")            
        elif value == 3:
            self._spdLbl.setText("Not Visible")
            
        if self._timer.isActive():
            self._resetTimer()            
         
    @Slot()
    def _onSetup(self):
        self._model.reset(self._percentObstacleSldr.value() / 100.0)
        self._alg.reset()
        self._worldWidget.repaint()
    
    @Slot()
    def _onRun(self):
        self._setupBtn.setEnabled(False)
        if self._timer.isActive():
            self._timer.stop()
            self._runBtn.setText("Run")
        else:
            self._resetTimer()
            self._runBtn.setText("Stop")
    
    @Slot()
    def _onStep(self):
        self._alg.step()
        visitedStr = ''
        for cell in self._alg.getVisitedCells():
            visitedStr = '{0}({1},{2}),'.format(visitedStr, cell.column, cell.row)
        print 'visited {0}'.format(visitedStr)
        print 'Current: {0},{1}'.format(self._alg.getCurrentCell().column, self._alg.getCurrentCell().row)
        self._worldWidget.repaint()
        
    def _resetTimer(self):
        timeOut = 1
        if self._spdSetting == 0:
            timeOut = 1000
        elif self._spdSetting == 1:
            timeOut = 500
        elif self._spdSetting == 2:
            timeOut = 250            
        elif self._spdSetting == 3:
            timeOut = 1
        self._timer.start(timeOut)

class WorldWidget(QWidget):
        
    def __init__(self, model, alg):
        super(WorldWidget, self).__init__()
        self._NUM_COLS = model.getNumColumns()
        self._NUM_ROWS = model.getNumRows()
        self._GRID_SIZE = 1
        #Assuming 33x33 grid, 1 pixel per cell and 1 pixel for grid lines
        #requires a minimum of a 65x65 pixel area
        self.setMinimumSize(65,65)
        self._model = model
        self._alg = alg
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        width = self.width()
        height = self.height()
        
        #Blank out the world
        painter.fillRect(0, 0, width, height, QColor('white'))

        #Compute width/height of the columns and rows
        
        #Reserve pixels for the grid lines
        colWidth = (width - (self._NUM_COLS - 1) * self._GRID_SIZE) / self._NUM_COLS
        rowHeight = (height - (self._NUM_ROWS - 1) * self._GRID_SIZE) / self._NUM_ROWS
        
        colWidth = max(1, colWidth)
        rowHeight = max(1, rowHeight)

        self._drawGrid(width, height, colWidth, rowHeight, painter)
        self._drawObstacles(colWidth, rowHeight, painter)
        self._drawVisitedCells(colWidth, rowHeight, painter)
        self._drawActiveCells(colWidth, rowHeight, painter)
        self._drawStartAndEndCells(colWidth, rowHeight, painter)
        self._drawCurrentCell(colWidth, rowHeight, painter)
        
        painter.end()

    def _drawObstacles(self, colWidth, rowHeight, painter):
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if self._model.getCell(row, col).isObstacle():
                    painter.fillRect(col * (colWidth + self._GRID_SIZE),
                                     row * (rowHeight + self._GRID_SIZE),
                                     colWidth, rowHeight, QColor('black'))
        
    def _drawGrid(self, width, height, colWidth, rowHeight, painter):
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
        start = self._model.getStartCell()
        end = self._model.getEndCell()
        
        if start != None:
            painter.fillRect(start.column * (colWidth + self._GRID_SIZE),
                             start.row * (rowHeight + self._GRID_SIZE),
                             colWidth, rowHeight, QColor('Green'))

        if end != None:
            painter.fillRect(end.column * (colWidth + self._GRID_SIZE),
                             end.row * (rowHeight + self._GRID_SIZE),
                             colWidth, rowHeight, QColor('Red'))
            
    def _drawVisitedCells(self, colWidth, rowHeight, painter):
        visited = self._alg.getVisitedCells()
        
        if visited != None:
            for cell in visited:
                painter.fillRect(cell.column * (colWidth + self._GRID_SIZE),
                                 cell.row * (rowHeight + self._GRID_SIZE),
                                 colWidth, rowHeight, QColor('cyan'))
                #Draw the estimated cost value of the current cell                
                textLoc = QPoint((cell.column + .1) * (colWidth + self._GRID_SIZE), 
                                 #Row + 3/4 of a row so that text is in the cell
                                 (cell.row + .75) * (rowHeight + self._GRID_SIZE))
                painter.drawText(textLoc, "{0:.2g}".format(cell.estimatedPathCostToCell))                

    def _drawActiveCells(self, colWidth, rowHeight, painter):
            visited = self._alg.getActiveCells()
            
            if visited != None:
                for cell in visited:
                    painter.fillRect(cell.column * (colWidth + self._GRID_SIZE),
                                     cell.row * (rowHeight + self._GRID_SIZE),
                                     colWidth, rowHeight, QColor('green'))
                    #Draw the estimated cost value of the current cell
                    textLoc = QPoint((cell.column + .1) * (colWidth + self._GRID_SIZE), 
                                     #Row + 3/4 of a row so that text is in the cell
                                     (cell.row + .75) * (rowHeight + self._GRID_SIZE))
                    painter.drawText(textLoc, "{0:.2g}".format(cell.estimatedPathCostToCell))
                
    def _drawCurrentCell(self, colWidth, rowHeight, painter):
        curCell = self._alg.getCurrentCell()
        
        if curCell != None:
            painter.fillRect(curCell.column * (colWidth + self._GRID_SIZE),
                             curCell.row * (rowHeight + self._GRID_SIZE),
                             colWidth, rowHeight, QColor('Yellow'))
            #Draw the estimated cost value of the current cell
            textLoc = QPoint((curCell.column + .1) * (colWidth + self._GRID_SIZE), 
                             #Row + 3/4 of a row so that text is in the cell
                             (curCell.row + .75) * (rowHeight + self._GRID_SIZE))
            painter.drawText(textLoc, "{0:.2g}".format(curCell.estimatedPathCostToCell))