from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QMenu, QGridLayout, QStackedLayout, QTabWidget, QStatusBar, QToolBar, QDialog, QDialogButtonBox, QMessageBox
from PySide6.QtGui import QPixmap, QColor, QPalette, QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize
from random import randint

# Setup class for main window
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        # Set window size
        self.setMinimumSize(600, 600)

        # Add button to window
        self.button = QPushButton("Click for new random value: 0")
        self.button.clicked.connect(self.button_pressed)

        self.setCentralWidget(self.button)

    def button_pressed(self):
        self.button.setText(f"Click for new random value: {randint(0, 100)}")


# Testing of directly wiring one widget to another
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


# Testing of overiding mouse event functions
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.label = QLabel()
        self.setCentralWidget(self.label)

    def mouseMovedEvent(self, event):
        self.label.setText("Mouse Moved")

    def mousePressEvent(self, event):
        self.label.setText("Mouse Pressed")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.label.setText("Left Button Released")
        elif event.button() == Qt.RightButton:
            self.label.setText("Right Button Released")
        elif event.button() == Qt.MiddleButton:
            self.label.setText("Middle Button Released")
        else:
            self.label.setText("Other Button Released")

    def mouseDoubleClickEvent(self, event):
        self.label.setText("Double Clicked")


# Test Displaying an image
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.label = QLabel()
        self.label.setPixmap(QPixmap("test_images/source_images/exdeath.bmp"))
        self.setCentralWidget(self.label)


# Test Checkboxes
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        self.checkbox1 = QCheckBox("Option 1")
        self.checkbox2 = QCheckBox("Option 2")
        self.checkbox3 = QCheckBox("Option 3")

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)

        self.checkbox1.setCheckState(Qt.CheckState.PartiallyChecked)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


# Helper class to display a solid color window
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        pallette = self.palette()
        pallette.setColor(QPalette.Window, QColor(color))
        self.setPalette(pallette)


# Layout testing class
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        widget = Color("red")
        self.setCentralWidget(widget)
    

# QVbox layout test
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        layout = QVBoxLayout()
        layout.addWidget(Color("red"))
        layout.addWidget(Color("green"))
        layout.addWidget(Color("blue"))

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


# QHbox layout test
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        layout = QHBoxLayout()
        layout.addWidget(Color("red"))
        layout.addWidget(Color("green"))
        layout.addWidget(Color("blue"))

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


# Test Context Menus
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")
    
    def contextMenuEvent(self, event):
        context = QMenu(self)
        context.addAction(QAction("Option 1", self))
        context.addAction(QAction("Option 2", self))
        context.addAction(QAction("Option 3", self))
        context.exec(event.globalPos())


# Test Nested Layouts
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        c1 = QVBoxLayout()
        c1.addWidget(Color("red"))
        c1.addWidget(Color("green"))
        c1.addWidget(Color("blue"))

        c2 = QVBoxLayout()
        c2.addWidget(Color("blue"))
        c2.addWidget(Color("red"))
        c2.addWidget(Color("green"))

        c3 = QVBoxLayout()
        c3.addWidget(Color("green"))
        c3.addWidget(Color("blue"))
        c3.addWidget(Color("red"))

        
        main_layout = QHBoxLayout()
        main_layout.addLayout(c1)
        main_layout.addLayout(c2)
        main_layout.addLayout(c3)
        main_layout.addWidget(Color("yellow"))

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)


# Test Layout Spacing and Margins
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        c1 = QVBoxLayout()
        c1.addWidget(Color("red"))
        c1.addWidget(Color("green"))
        c1.addWidget(Color("blue"))
        c1.setContentsMargins(5,5,5,5)

        c2 = QVBoxLayout()
        c2.addWidget(Color("blue"))
        c2.addWidget(Color("red"))
        c2.addWidget(Color("green"))

        c3 = QVBoxLayout()
        c3.addWidget(Color("green"))
        c3.addWidget(Color("blue"))
        c3.addWidget(Color("red"))
        c3.setSpacing(5)

        
        main_layout = QHBoxLayout()
        main_layout.addLayout(c1)
        main_layout.addLayout(c2)
        main_layout.addLayout(c3)
        main_layout.addWidget(Color("yellow"))

        main_layout.setSpacing(0)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)


# Test Grid Layout
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        # Intialize grid layout
        layout = QGridLayout()

        # # Grid layout removes unused rows/columns
        # layout.addWidget(Color("red"), 3, 3)
        # layout.addWidget(Color("green"), 0, 0)
        # layout.addWidget(Color("blue"), 3, 0)
        # layout.addWidget(Color("yellow"), 0, 3)

        # Basic layout using all columns/rows
        layout.addWidget(Color("red"), 3, 3)
        layout.addWidget(Color("green"), 2, 1)
        layout.addWidget(Color("blue"), 1, 2)
        layout.addWidget(Color("yellow"), 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


# Test QStacked Layout
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        layout = QStackedLayout()

        layout.addWidget(Color("red"))
        layout.addWidget(Color("green"))
        layout.addWidget(Color("blue"))
        layout.addWidget(Color("yellow"))

        layout.setCurrentIndex(3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


# Use Qstacked Widget to create a tabbed interface
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        # Create Stacked layout for color layers
        color_layout = QStackedLayout()
        color_layout.addWidget(Color("red"))
        color_layout.addWidget(Color("green"))
        color_layout.addWidget(Color("blue"))
        color_layout.addWidget(Color("yellow"))


        # Create Hbox layout for buttons to switch between color layers
        button_layout = QHBoxLayout()
        red_button = QPushButton("Red")
        red_button.pressed.connect(lambda: color_layout.setCurrentIndex(0))
        button_layout.addWidget(red_button)

        green_button = QPushButton("Green")
        green_button.pressed.connect(lambda: color_layout.setCurrentIndex(1))
        button_layout.addWidget(green_button)

        blue_button = QPushButton("Blue")
        blue_button.pressed.connect(lambda: color_layout.setCurrentIndex(2))
        button_layout.addWidget(blue_button)

        yellow_button = QPushButton("Yellow")
        yellow_button.pressed.connect(lambda: color_layout.setCurrentIndex(3))
        button_layout.addWidget(yellow_button)


        # Create toplevel Vbox to store buttons on top of colors
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addLayout(color_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


# Use QTabWidget to create a tabbed interface
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.East)
        tabs.setMovable(True)
        for c in ["red", "green", "blue", "yellow"]:
            tabs.addTab(Color(c), c.capitalize())

        self.setCentralWidget(tabs)


# Add a toolbar
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()  

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        toolbar = QToolBar("Example Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        button_action = QAction("Test Button", self)
        button_action.setStatusTip("This is a test button")
        button_action.triggered.connect(lambda: self.toolbar_button_clicked("Test Button"))
        button_action.setCheckable(True)
        button_action.setShortcut(QKeySequence("Ctrl+T"))
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        bug_report = QAction(QIcon("test_images/source_images/exdeath.bmp"), "Report a Bug", self)
        bug_report.setStatusTip("Report a bug to the developer")
        bug_report.triggered.connect(self.bug_report_clicked)
        toolbar.addAction(bug_report)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("Toolbar Label"))
        toolbar.addWidget(QCheckBox())

        toolbar.addSeparator()

        toolbar.addWidget(QLineEdit("Toolbar Input"))

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)

        submenu = file_menu.addMenu("Submenu")
        submenu.addAction(button_action)


    def toolbar_button_clicked(self, s):
        print("Toolbar button clicked", s)
    
    def bug_report_clicked(self):
        print("Bug Reported")


# Custom dialog class
class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Dialog")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Something Important Happened"))
        layout.addWidget(self.button_box)
        self.setLayout(layout)


# Dialog for accepting or rejecting something with title/message set when called
class AcceptRejectDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(message))
        layout.addWidget(self.button_box)
        self.setLayout(layout)


# Test Dialog Boxes
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()  

        # Set Window title
        self.setWindowTitle("Pixel Art Helper")

        button = QPushButton("Click me for a dialog")
        button.clicked.connect(self.button_clicked)
        button.setShortcut(QKeySequence("Ctrl+Shift+T"))
        self.setCentralWidget(button)


    # def button_clicked(self):
    #     print("Button Clicked")

    #     # dialog = CustomDialog()
    #     dialog = AcceptRejectDialog("Important Question", "Do you want to proceed?", self)
    #     if dialog.exec():
    #         print("Dialog Accepted")
    #     else:
    #         print("Dialog Rejected")

    def button_clicked(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Message Box")
        dialog.setText("This is a message box")
        dialog.setIcon(QMessageBox.Question)
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        button = dialog.exec()
        if button == QMessageBox.Ok:
            print("Alright")
        else:
            print("Oh")


# Create application instance
app = QApplication([])

# Create an instance of the main window
window = main_window()

# Show the main window instance
window.show()

# Start the application's event loop
app.exec()