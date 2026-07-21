import glob
import json
from PIL import Image, ImageQt

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QStatusBar, QMessageBox, QFileDialog, QSplitter, QFrame, QScrollArea, QSizePolicy, QSpinBox, QButtonGroup
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QKeySequence, QImage, QIcon
from PySide6.QtCore import Qt, QSize

# Main Window Class
class main_window(QMainWindow):
    def __init__(self):

        #####################
        ### Initial Setup ###
        #####################

        super().__init__()                             # Initialize super class
        self.setWindowTitle("Palette Creation Helper") # Set Window title
        self.setMinimumSize(900, 600)                  # Set Window Size

        # Intialize instance variables
        self.palettes = dict()
        self.image = None
        self.image_preview = None
        self.filepath = None

        # Set Status Bar
        self.setStatusBar(QStatusBar(self))

        # Allow opening images by dragging and dropping them onto the image frame
        self.setAcceptDrops(True)

        #######################
        ### Set Window Icon ###
        #######################

        icon = QIcon()
        icon.addFile("assets/images/palette_creator_icon.ico")
        self.setWindowIcon(icon)


        ################
        ### Menu Bar ###
        ################

        # Create Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        # Create open button
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.setStatusTip("Open a file")
        file_menu.addAction(open_action)

        # Create Export button
        export_action = QAction("E&xport", self)
        export_action.triggered.connect(self.export)
        export_action.setShortcut(QKeySequence("Ctrl+Shift+E"))
        export_action.setStatusTip("Export the palette for inlay helper")
        file_menu.addAction(export_action)

        # Add Exit action
        file_menu.addSeparator()
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.exit)
        exit_action.setShortcut(QKeySequence("Ctrl+W"))
        exit_action.setStatusTip("Exit the application")
        file_menu.addAction(exit_action)


    # Function to safely quit the application
    def exit(self):
        QApplication.instance().quit()
    

    # Export a palette to main
    def export(self):
        pass


    # Open a folder and set up application
    def open(self):
        pass

# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
