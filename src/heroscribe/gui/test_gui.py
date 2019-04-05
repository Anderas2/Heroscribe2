import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import *
from src.heroscribe.Constants import Constants
#from PyQt5.QtCore import pyqtSlot
from src.heroscribe.Preferences import Preferences


class hs2_window(QMainWindow):
    def __init__(self):
        super().__init__()
        pref = Preferences()
        const = Constants()
        
        # Window stats
        self.title = self.update_title()
        self.width = 1024
        self.height = 768

        
        self.g_text = pref.gui_texts

        try:
        	options = open("options", "r")
        	self.lang = options.readline()[9:]
        	options.close()
        except FileNotFoundError:
        	options = open("options", "x")
        	options.write("language=en\n")
        	self.lang = "en"
        	options.close()
        self.initUI()


	# Initialize the GUI to the main window
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(1024, 768)
        self.center_window()
        self.statusBar().showMessage('Map Editor')

		#--------------------Buttons--------------------#
		# NOTE: I'm thinking these might be better at the top of the screen, then
		# we will have the section specific buttons/boxes on the left side
        # Add Objects button
        add_button = QPushButton("Add Objects", self)
        add_button.setToolTip('Add elements to the map')
        add_button.move(20, 20)
        add_button.clicked.connect(self.add_click)

        # Edit Object button
        edit_button = QPushButton('Edit Objects', self)
        edit_button.setToolTip('Edit placed objects')
        edit_button.move(20, 50)
        edit_button.clicked.connect(self.edit_click)

        # Darken/Color button
        dark_button = QPushButton('Darken/Color', self)
        dark_button.setToolTip('Darken/color squares on the map')
        dark_button.move(20, 80)
        dark_button.clicked.connect(self.dark_click)

        # Import button
        import_button = QPushButton('Import', self)
        import_button.setToolTip('Import icons, maps or quests')
        import_button.move(20, 110)
        import_button.clicked.connect(self.import_click)

        # Export button
        export_button = QPushButton('Export', self)
        export_button.setToolTip('Export icons, maps, or quests')
        export_button.move(20, 140)
        export_button.clicked.connect(self.export_click)

        # Display the window
        self.show()

    # Function to center main window
    def center_window(self):
    	win_bounds = self.frameGeometry()
    	screen_cp = QDesktopWidget().availableGeometry().center()
    	win_bounds.moveCenter(screen_cp)
    	self.move(win_bounds.topLeft())
    	
    def update_title(self):
    	title = const.applicationName + ' ' + const.version
    	return title

    	

	#--------------------Button Event Handlers--------------------#
	# Add Object button
    def add_click(self):
        self.statusBar().showMessage('Add button pressed')

	# Edit Object button
    def edit_click(self):
        self.statusBar().showMessage('Edit button pressed')

	# Darken/Color button
    def dark_click(self):
        self.statusBar().showMessage('Darken button pressed')

    # Import button
    def import_click(self):
    	self.statusBar().showMessage('Import functionality hopefully coming soon!')

    # Export button
    def export_click(self):
    	self.statusBar().showMessage('Export functionality hopefully coming soon!')