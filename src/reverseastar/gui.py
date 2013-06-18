from PySide.QtCore import *
from PySide.QtGui import *


class MainWindow(object):
    '''
    Contains the implementation for building and displaying the 
    application's main window.
    '''


    def __init__(self):
        self._window = QMainWindow()
        self._window.setWindowTitle("Reverse A*")
        self._worldWidget = WorldWidget()
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
        setupBtn = QPushButton("Setup", self._window)
        runBtn = QPushButton("Run", self._window)
        stepBtn = QPushButton("Step", self._window)
        
        setupBtn.clicked.connect(self._onSetup)
        runBtn.clicked.connect(self._onRun)
        stepBtn.clicked.connect(self._onStep)
        
        layout = QVBoxLayout()
        layout.addWidget(setupBtn)
        layout.addWidget(runBtn)
        layout.addWidget(stepBtn)
        
        grpBx = QGroupBox("Controls")
        grpBx.setLayout(layout)
        return grpBx
                
    @Slot()    
    def _onSetup(self):
        print 'setup called'
    
    @Slot()
    def _onRun(self):
        print 'run called'
    
    @Slot()
    def _onStep(self):
        print 'step called'

class WorldWidget(QWidget):
        
    def __init__(self):
        super(WorldWidget, self).__init__()
        self._NUM_COLS = 10
        self._NUM_ROWS = 10
        self._GRID_SIZE = 1
        self.setMinimumSize(65,65)
    
    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        
        width = self.width()
        height = self.height()
        
        #Blank out the world
        painter.fillRect(0, 0, width, height, QColor('white'))
        
        #TODO Border cells are not bounded properly
        
        #Compute width of the columns and rows
        colWidth = width / self._NUM_COLS
        rowHeight = height / self._NUM_ROWS
        #Allow room for grid lines
        colWidth = colWidth - (self._NUM_COLS - 1) * self._GRID_SIZE
        rowHeight = rowHeight - (self._NUM_ROWS - 1) * self._GRID_SIZE
        
        #Paint the grid lines
        brush = QBrush(QColor('black'))
        painter.setBrush(brush)
        for row in range(1, self._NUM_ROWS):
            painter.drawLine(0, row * rowHeight + self._GRID_SIZE,
                             width, row * rowHeight + self._GRID_SIZE)
            for col in range(1, self._NUM_COLS):
                painter.drawLine(col * colWidth + self._GRID_SIZE, 0,
                             col * colWidth + self._GRID_SIZE, height)
        
        painter.end()