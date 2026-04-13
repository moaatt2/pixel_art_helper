import glob
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QMenu, QGridLayout, QStackedLayout, QTabWidget, QStatusBar, QToolBar, QDialog, QDialogButtonBox, QMessageBox, QFileDialog, QSplitter, QFrame, QSizePolicy
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize


# Helper class to display a solid color window
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        pallette = self.palette()
        pallette.setColor(QPalette.Window, QColor(color))
        self.setPalette(pallette)


# Custom Label class overwriting min size hint so the splitter can make the image smaller
class ImageLabel(QLabel):
    def minimumSizeHint(self):
        return QSize(0,0)


# Helper accordian widget
class Accordian(QWidget):
    def __init__(self, title):
        super().__init__()

        # Create color section
        self.content_section = QWidget()
        self.content_section.setVisible(False)

        # Set a fixed layout to add widgets to the content section
        self.content_layout = QVBoxLayout(self.content_section)

        # Add button
        button = QPushButton(title)
        button.clicked.connect(self.toggle_section)

        # Create layout and add content
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.content_section)
        layout.setContentsMargins(0,0,0,0)

        # Apply layout to self
        self.setLayout(layout)


    def toggle_section(self):
        self.content_section.setVisible(not self.content_section.isVisible())


    def set_content(self, content:QWidget):
        while self.content_layout.count() > 0:
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            
        self.content_layout.addWidget(content)



# Main Window Class
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()                      # Initialize super class
        self.setWindowTitle("Pixel Art Helper") # Set Window title
        self.setMinimumSize(600, 600)           # Set Window Size

        # Intialize instance variables
        self.palettes = dict()


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

        # Create save button
        save_action = QAction("&Save", self)
        save_action.triggered.connect(self.save)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.setStatusTip("Save the current file")
        file_menu.addAction(save_action)

        # Create save as button
        save_as_action = QAction("Save &As", self)
        save_as_action.triggered.connect(self.save_as)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.setStatusTip("Save the current file with a new name")
        file_menu.addAction(save_as_action)

        # Add a separator between file actions and palette actions
        file_menu.addSeparator()

        # Create reload button
        reload_action = QAction("&Reload Palettes", self)
        reload_action.triggered.connect(self.load_palettes)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.setStatusTip("Reload the color palettes")
        file_menu.addAction(reload_action)

        # Add Exit action
        file_menu.addSeparator()
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.exit)
        exit_action.setShortcut(QKeySequence("Ctrl+W"))
        exit_action.setStatusTip("Exit the application")
        file_menu.addAction(exit_action)

        #################
        ### Side Menu ###
        #################

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignTop)
        menu_layout.setContentsMargins(0,0,0,0)
        menu_layout.setSpacing(0)

        self.palette_accordion = Accordian("Palettes")
        menu_layout.addWidget(self.palette_accordion)
        self.palette_accordion.set_content(QLabel("Palette content goes here"))

        self.image_accordion = Accordian("Image Options")
        menu_layout.addWidget(self.image_accordion)
        self.image_accordion.set_content(QLabel("Image options go here"))

        self.pattern_accordion = Accordian("Pattern Options")
        menu_layout.addWidget(self.pattern_accordion)
        self.pattern_accordion.set_content(QLabel("Pattern options go here"))


        # Create Side Menu
        self.side_menu = QFrame()
        self.side_menu.setLayout(menu_layout)
        self.side_menu.setLineWidth(2)
        self.side_menu.setFrameShape(QFrame.Box)


        #############################
        ### Setup Image Container ###
        #############################

        # Create Frame for image
        self.image_frame = QFrame()
        self.image_frame.setLineWidth(2)
        self.image_frame.setFrameShape(QFrame.Box)

        # Create Layout for image
        image_layout = QVBoxLayout(self.image_frame)
        image_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        self.image_container = ImageLabel("Press Ctrl+O to open an image", self.image_frame)
        self.image_container.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_container)


        ##########################
        ### Create Main Layout ###
        ##########################

        # Create Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.side_menu)
        splitter.addWidget(self.image_frame)

        # Set an inital 1:3 ratio
        splitter.setSizes([200,600])

        # Set splitter stretch factors to maintain 1:3 ratio
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,3)

        # When the splitter moves update the image size
        splitter.splitterMoved.connect(self.update_image)

        # Set splitter as central widget
        self.setCentralWidget(splitter)

        # Set Status Bar
        self.setStatusBar(QStatusBar(self))


    # On open button, create file dialog, load selected image, display image in container
    def open(self):
        print("Open File")

        # Create File Dialog
        file_dialog = QFileDialog(self)

        # File Dialog Settings
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
 
        # Execute File Dialog and get selected file
        if file_dialog.exec():
            file_name = file_dialog.selectedFiles()[0]
            print(f"Selected file: {file_name}")

            # Load the selected image into the image container
            self.image = QPixmap(file_name)
            self.image_path = file_name
            self.update_image()


    # Placeholder for save file functionality
    def save(self):
        print("Save File")


    # Placeholder for save as functionality
    def save_as(self):
        print("Save As File")


    # Placeholder for reload palettes functionality
    def load_palettes(self):
        print("Reload Palettes")
    
        # Itterate over palette files
        for path in glob.glob("palettes/*.json"):
            palette_name = path.split("/")[-1].split("\\")[-1].split(".")[0]

            # Load palette files
            with open(path, "r") as f:
                raw = json.load(f)
            
            # Create dict in palettes dict for current palette
            self.palettes[palette_name] = {
                "enabled": False,
                "colors": dict(),
            }

            # Convert hex color codes to RGB tuples and store in palette dict
            for k, v in raw.items():
                r = int(v[0:2], 16)
                g = int(v[2:4], 16)
                b = int(v[4:6], 16)
                self.palettes[palette_name]["colors"][k] = {
                    "rgb": (r, g, b),
                    "hexstring": v,
                    "enabled": False,
                }


    # Custom Resize Event to rescale image when window is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()


    # Function to safely quit the application
    def exit(self):
        # TODO: Check for unsaved work and ask if user is sure
        QApplication.instance().quit()

    # Resize image preview based on available space
    def update_image(self):
        if hasattr(self, "image"):
            size = self.image_container.size()

            if size.width() > 0 and size.height() > 0:
                self.image_container.setPixmap(
                    self.image.scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )


# Start Application
if __name__ == "__main__":
    app = QApplication([]) # Create application instance
    window = main_window() # Create an instance of the main window
    window.show()          # Show the main window instance
    app.exec()             # Start the application's event loop
