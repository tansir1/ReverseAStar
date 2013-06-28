import sys

from PySide.QtGui import QApplication

import gui
import model
import algorithm

#Main launching point of the application.

if __name__ == '__main__':
    #Create Qt library wrapper
    app = QApplication(sys.argv)
    #Define our world
    world = model.WorldModel()
    #Default to 30% obstacle coverage
    world.reset(0.3)
    #Create the algorithm and attach the world to it.
    alg = algorithm.ReverseAStarAlgorithm(world)
    #Initialize the algorithm class settings
    alg.reset()
    #Launch the GUI
    gui = gui.MainWindow(world, alg)
    #Run until the application is terminated.
    sys.exit(app.exec_())