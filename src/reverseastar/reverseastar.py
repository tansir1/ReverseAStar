import sys

from PySide.QtCore import *
from PySide.QtGui import *

import gui
import model

if __name__ == '__main__':  
    app = QApplication(sys.argv)
    world = model.WorldModel()
    gui = gui.MainWindow(world)
    sys.exit(app.exec_())