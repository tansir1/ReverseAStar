import sys

from PySide.QtGui import QApplication

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