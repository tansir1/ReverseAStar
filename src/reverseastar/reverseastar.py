import sys

from PySide.QtCore import *
from PySide.QtGui import *

import gui


if __name__ == '__main__':  
    app = QApplication(sys.argv)
    gui = gui.MainWindow()
    sys.exit(app.exec_())