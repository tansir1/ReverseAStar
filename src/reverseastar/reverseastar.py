import sys

from PySide.QtCore import *
from PySide.QtGui import *

import gui
import model
import algorithm

if __name__ == '__main__':  
    app = QApplication(sys.argv)
    world = model.WorldModel()
    #Default to 30% coverage
    world.reset(0.3)
    alg = algorithm.ReverseAStarAlgorithm(world)
    alg.reset()
    gui = gui.MainWindow(world, alg)
    sys.exit(app.exec_())