import glob
import json
import pathlib
import functools
from PIL import Image, ImageQt

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QStatusBar, QMessageBox, QFileDialog, QSplitter, QFrame, QScrollArea, QSizePolicy, QSpinBox, QButtonGroup, QSlider
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QKeySequence, QImage, QIcon
from PySide6.QtCore import Qt, QSize


########################
### Helper Functions ###
########################

# Helper function for converting a pil image to a pixmap
def pil_to_pixmap(image: Image.Image) -> QPixmap:
    image = image.convert("RGB")
    data = image.tobytes("raw", "RGB")
    qi = QImage(data, image.size[0], image.size[1], image.size[0]*3, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qi)


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
        self.image_buttons = None

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
        self.image_container = ImageLabel("Press Ctrl+O to open a folder or drag a folder here", image_box)
        self.image_container.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_container)


        #######################
        ### Create Mask Box ###
        #######################

        # Create Frame for image
        self.mask_box = QFrame()
        self.mask_box.setLineWidth(2)
        self.mask_box.setFrameShape(QFrame.Box)

        # Create Layout for image
        mask_layout = QVBoxLayout(self.mask_box)
        mask_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        self.mask_container = ImageLabel("Open a folder to get started", self.mask_box)
        self.mask_container.setAlignment(Qt.AlignCenter)
        mask_layout.addWidget(self.mask_container)


        #########################
        ### Create Folder Box ###
        #########################

        # Create Frame for image
        self.folder_box = QFrame()
        self.folder_box.setLineWidth(2)
        self.folder_box.setFrameShape(QFrame.Box)

        # Create Layout for image
        folder_layout = QVBoxLayout(self.folder_box)
        folder_layout.setContentsMargins(0,0,0,0)

        # Create label for image
        folder_container = ImageLabel("Open a folder to get started", self.folder_box)
        folder_container.setAlignment(Qt.AlignCenter)
        folder_layout.addWidget(folder_container)


        ###################################
        ### Create Mask/Folder Splitter ###
        ###################################

        # Create vertical splitter
        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.addWidget(self.mask_box)
        vsplitter.addWidget(self.folder_box)

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

        # Connect Splitter to image resizing
        splitter.splitterMoved.connect(self.update_image)

        # Set splitter as central widget
        self.setCentralWidget(splitter)


    # Function to safely quit the application
    def exit(self):
        QApplication.instance().quit()
    

    # Export a palette to main
    def export(self):
        pass


    # Resize image based on available space
    def update_image(self):
        if self.image_preview is not None:
            size = self.image_container.size()
            if size.width() > 0 and size.height() > 0:
                self.image_container.setPixmap(
                    self.image_preview.scaled(
                        size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )


    # Custom Resize Event to rescale image when window is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()


    # Handle user clicking an image button
    def image_click(self, button=None):
        print(f"Clicked {button} image button")

        ##################
        ### Load image ###
        ##################

        # Open image
        image_path = self.config[button]['image_path']
        self.image = Image.open(image_path)

        # Create preview
        self.image_preview = pil_to_pixmap(self.image)

        # Draw image to image box
        self.update_image()

        ##################
        ### Load Masks ###
        ##################


        # Find layout for mask box
        mask_layout = self.mask_box.layout()

        # Clear existing items from mask box layout
        for _ in range(mask_layout.count()):
            w = mask_layout.itemAt(0).widget()
            w.setParent(None)
            w.deleteLater()

        # Itterate over masks for image
        self.masks = list()
        for mask_name in self.config[button]['masks']:

            # Get mask data
            mask = self.config[button]['masks'][mask_name]

            # Create container & layout for sliders
            sliders = QWidget()
            slider_layout = QVBoxLayout(sliders)

            slider_config = [
                ["Red Min",   "rmin"],
                ["Red Max",   "rmax"],
                ["Green Min", "gmin"],
                ["Green Max", "gmax"],
                ["Blue Min",  "bmin"],
                ["Blue Max",  "bmax"],
            ]

            for label, key in slider_config:
                widget = QWidget()
                layout = QHBoxLayout(widget)
                label = QLabel(label)
                slider = QSlider()
                slider.setRange(0, 255)
                slider.setSingleStep(1)
                slider.setSliderPosition(mask[key])
                slider.setOrientation(Qt.Horizontal)
                layout.addWidget(label)
                layout.addWidget(slider)
                slider_layout.addWidget(widget)

            mask_layout.addWidget(sliders)

        #################
        ### Run Masks ###
        #################

        # TODO

        #############################
        ### Fill Image background ###
        #############################

        # TODO


    # Read config and fill out folder box
    def update_folder_box(self):

        # Find layout for folder box
        folder_layout = self.folder_box.layout()

        # Clear existing items from folderbox layout
        for _ in range(folder_layout.count()):
            w = folder_layout.itemAt(0).widget()
            w.setParent(None)
            w.deleteLater()


        # Create widget to hold file buttons
        file_section = QWidget()
        file_section_layout = QVBoxLayout(file_section)
        file_section_layout.setSpacing(3)
        file_section_layout.setAlignment(Qt.AlignTop)

        # Create Exclusive Button group to add buttons to
        self.image_buttons = QButtonGroup()
        self.image_buttons.setExclusive(True)

        # Create buttons for each folder
        for key in self.config:
            name = self.config[key]["image_name"]

            text = f"✔️ {name}" if self.config[key]['hex_code'] else f"❌ {name}"

            button = QPushButton(text)
            button.setCheckable(True)
            button.clicked.connect(functools.partial(self.image_click, button=key))
            button.setStyleSheet("text-align: left; padding-left: 5px; padding-right: 5px; padding-top: 3px; padding-bottom: 3px;")
            self.image_buttons.addButton(button)
            file_section_layout.addWidget(button)


        # Create a scroll area to hold a large list of files
        scroll_area = QScrollArea()
        scroll_area.setWidget(file_section)

        # Scroll Area Setting
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add the scroll area to the layout
        folder_layout.addWidget(scroll_area)


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

        # Create config file path and verify it exists
        self.config_path = pathlib.Path(folder_path, "_config.json")
        config_exists = self.config_path.exists(follow_symlinks=False)

        # If config exists load it
        if config_exists:
            with open(str(self.config_path)) as config_file:
                self.config = json.load(config_file)

        # If config doesnt exist initalize
        else:
            self.config = dict()

        # Ensure all images are in config
        images_added = list()
        for image in images:
            if image not in self.config:
                images_added.append(image)
                self.config[image] = {
                    "image_path": str(pathlib.Path(folder_path, image)),
                    "image_name": ''.join(image.split('.')[:-1]).replace("_", " ").title(),
                    "hex_code": "",
                    "masks": {
                        "default": {
                            "type": "rgb_subtractive",
                            "active": False,
                            "rmax": 255,
                            "rmin": 180,
                            "gmax": 255,
                            "gmin": 180,
                            "bmax": 255,
                            "bmin": 180,                            
                        },
                    },
                }


        # Notify user if images were added to existing config
        if config_exists and len(images_added) > 0:
            images_added = ''.join([f"\n\t{i}" for i in images_added])
            QMessageBox.warning(self,"Images Added to Config",f"The following images were added to the existing config:{images_added}")


        # Mark config items if they are on disk
        for item in self.config:
            path = self.config[item]['image_path']
            if pathlib.Path(path).exists(follow_symlinks=False):
                self.config[item]['path_valid'] = True
            else:
                self.config[item]['path_valid'] = False 


        # Update config on file in case changes occured
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config, config_file, indent=4)


        # update the folder box with config data
        self.update_folder_box()


        # Update Image box text
        self.image_container.setText("Select an image to continue")

        # Update Mask box text
        self.mask_container.setText("Select an image to continue")

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
