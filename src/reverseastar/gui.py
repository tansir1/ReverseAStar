from PySide.QtCore import *
from PySide.QtGui import *


class MainWindow(object):
    '''
    Contains the implementation for building and displaying the 
    application's main window.
    '''


    def __init__(self, model):
        self._window = QMainWindow()
        self._window.setWindowTitle("Reverse A*")
        self._worldWidget = WorldWidget(model)
        self._model = model
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
        
        #self._worldWidget.setMinimumSize(65,65)
        
    def _buildControlPanel(self):
        setupBtn = QPushButton("Setup", self._window)
        runBtn = QPushButton("Run", self._window)
        stepBtn = QPushButton("Step", self._window)
        
        setupBtn.clicked.connect(self._onSetup)
        runBtn.clicked.connect(self._onRun)
        stepBtn.clicked.connect(self._onStep)
        
        #slider = QSlider(Qt.Horizontal, self._window)
        #slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        #slider.setTickInterval(25)
        
        layout = QVBoxLayout()
        layout.addWidget(setupBtn)
        layout.addWidget(runBtn)
        layout.addWidget(stepBtn)
        #layout.addWidget(QLabel("Update speed"))
        #layout.addWidget(slider)
        
        grpBx = QGroupBox("Controls")
        grpBx.setLayout(layout)
        return grpBx
                
    @Slot()    
    def _onSetup(self):
        print 'setup called'
        self._model.reset(0.3)
        self._worldWidget.repaint()
    
    @Slot()
    def _onRun(self):
        print 'run called'
    
    @Slot()
    def _onStep(self):
        print 'step called'

class WorldWidget(QWidget):
        
    def __init__(self, model):
        super(WorldWidget, self).__init__()
        self._NUM_COLS = model.getNumColumns()
        self._NUM_ROWS = model.getNumRows()
        self._GRID_SIZE = 1
        self.setMinimumSize(65,65)
        self._model = model
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        width = self.width()
        height = self.height()
        
        #Blank out the world
        painter.fillRect(0, 0, width, height, QColor('white'))

        #Compute width/height of the columns and rows
        
        #Reserve pixels for the gridlines
        width = width - (self._NUM_COLS - 1) * self._GRID_SIZE
        height = height - (self._NUM_ROWS - 1) * self._GRID_SIZE
        
        colWidth = width / self._NUM_COLS
        rowHeight = height / self._NUM_ROWS
        
        colWidth = max(1, colWidth)
        rowHeight = max(1, rowHeight)
        
        self._drawGrid(width, height, colWidth, rowHeight, painter)
        self._drawObstacles(colWidth, rowHeight, painter)
        
        painter.end()

    def _drawObstacles(self, colWidth, rowHeight, painter):
        for row in range(0, self._NUM_ROWS):
            for col in range(0, self._NUM_COLS):
                if self._model.isObstacle(row, col):
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
                