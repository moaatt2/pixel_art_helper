import glob
import json
import pathlib
from PIL import Image, ImageQt

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QStatusBar, QMessageBox, QFileDialog, QSplitter, QFrame, QScrollArea, QSizePolicy, QSpinBox, QButtonGroup
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QKeySequence, QImage, QIcon
from PySide6.QtCore import Qt, QSize

#########################
### Custom UI Widgets ###
#########################

# Custom Label class overwriting min size hint so the splitter can make the image smaller
class ImageLabel(QLabel):
    def minimumSizeHint(self):
        return QSize(0,0)


###################
### Main Window ###
###################

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
        self.config = None
        self.config_path = None

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
        open_action.triggered.connect(self.select_folder)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.setStatusTip("Open a folder")
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


        ########################
        ### Create Image Box ###
        ########################

        # Create Frame for image
        image_box = QFrame()
        image_box.setLineWidth(2)
        image_box.setFrameShape(QFrame.Box)

        # Create Layout for image
        image_layout = QVBoxLayout(image_box)
        image_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        image_container = ImageLabel("Press Ctrl+O to open a folder or drag a folder here", image_box)
        image_container.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_container)


        #######################
        ### Create Mask Box ###
        #######################

        # Create Frame for image
        mask_box = QFrame()
        mask_box.setLineWidth(2)
        mask_box.setFrameShape(QFrame.Box)

        # Create Layout for image
        mask_layout = QVBoxLayout(mask_box)
        mask_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        mask_container = ImageLabel("Mask Box", mask_box)
        mask_container.setAlignment(Qt.AlignCenter)
        mask_layout.addWidget(mask_container)


        #########################
        ### Create Folder Box ###
        #########################

        # Create Frame for image
        folder_box = QFrame()
        folder_box.setLineWidth(2)
        folder_box.setFrameShape(QFrame.Box)

        # Create Layout for image
        folder_layout = QVBoxLayout(folder_box)
        folder_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        folder_container = ImageLabel("Folder Box", folder_box)
        folder_container.setAlignment(Qt.AlignCenter)
        folder_layout.addWidget(folder_container)


        ###################################
        ### Create Mask/Folder Splitter ###
        ###################################

        # Create vertical splitter
        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.addWidget(mask_box)
        vsplitter.addWidget(folder_box)

        # Set an inital 1:1 ratio
        vsplitter.setSizes([1,1])

        # Set splitter stretch factors to maintain 1:1 ratio
        vsplitter.setStretchFactor(0,1)
        vsplitter.setStretchFactor(1,1)


        ##########################
        ### Create Main Layout ###
        ##########################

        # Create Splitter
        splitter = QSplitter(Qt.Horizontal)
        # splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(vsplitter)
        splitter.addWidget(image_box)

        # Set an inital 1:3 ratio
        splitter.setSizes([200,600])

        # Set splitter stretch factors to maintain 1:3 ratio
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,3)

        # Set splitter as central widget
        self.setCentralWidget(splitter)


    # Function to safely quit the application
    def exit(self):
        QApplication.instance().quit()
    

    # Export a palette to main
    def export(self):
        pass


    # Open a folder and set up application
    def open_folder(self, folder_path):
        print(folder_path)

        # Get images by extension
        bmps  = glob.glob("*.bmp",  root_dir=folder_path)
        pngs  = glob.glob("*.png",  root_dir=folder_path)
        jpgs  = glob.glob("*.jpg",  root_dir=folder_path)
        jpegs = glob.glob("*.jpeg", root_dir=folder_path)

        # Combine images
        images = list()
        images.extend(bmps + pngs + jpgs + jpegs)
        images.sort()

        # Load config from file if it exists
        self.config_path = pathlib.Path(folder_path, "_config.json")
        if self.config_path.exists(follow_symlinks=False):
            with open(str(self.config_path)) as config_file:
                self.config = json.load(config_file)

        # Otherwise create config
        else:
            self.config = dict()
            for image in images:

                # Get image name without extension
                image_name = ''.join(image.split('.')[:-1])

                # Add image to config
                self.config[image] = {
                    "image_path": str(pathlib.Path(folder_path, image)),
                    "image_name": ''.join(image.split('.')[:-1]).replace("_", " ").title(),
                    "hex_code": "",
                    "masks": dict()
                }

            # Write config to file
            with open(self.config_path, 'w') as config_file:
                json.dump(self.config, config_file, indent=4)




    # Select the folder to open and pass it to the folder opening function
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.open_folder(folder_path)


# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
