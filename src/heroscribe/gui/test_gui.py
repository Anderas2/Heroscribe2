import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import *
from src.heroscribe.Constants import Constants
from PyQt5.QtCore import pyqtSlot
from src.heroscribe.Preferences import Preferences

class QuitMessage(QMessageBox):
	def __init__(self):
		QMessageBox.__init__(self)
		self.setText('Are you sure you wish to close Heroscribe?')
		self.addButton(self.Yes)
		self.addButton(self.No)
		self.setDefaultButton(self.Yes)
		

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
        
        #----------------Menu Bar Actions---------------#
        # New menu actions
        nq = QAction('Quest', self)
        nq1x2 = QAction('Quest 1x2', self)
        nq2x1 = QAction('Quest 2x1', self)
        nq2x2 = QAction('Quest 2x2', self)
        nq2x3 = QAction('Quest 2x3', self)
        nq3x2 = QAction('Quest 3x2', self)
        nq3x3 = QAction('Quest 3x3', self)
        
        # File menu actions
        oq_act = QAction('Open Quest', self)
        sq_act = QAction('Save Quest', self)
        sqa_act = QAction('Save Quest As', self)
        q_act = QAction('Quit', self)
        q_act.triggered.connect(qApp.quit)
        
        # Region menu actions
        eu_act = QAction('Europe layout', self)
        us_act = QAction('USA layout', self)
        
        # Help menu actions
        about = QAction('About', self)
        
        #-------------------Menu Bar--------------------#
        menu_bar = self.menuBar()
        
        # Menu bars don't display the same across all OS platforms. To fix this,
        # the manu bar is told to act as a non-native menu bar
        menu_bar.setNativeMenuBar(False)
        
        # New menu that is contained in File menu
        n_menu = QMenu('New', self)
        n_menu.addAction(nq)
        n_menu.addAction(nq1x2)
        n_menu.addAction(nq2x1)
        n_menu.addAction(nq2x2)
        n_menu.addAction(nq2x3)
        n_menu.addAction(nq3x2)
        n_menu.addAction(nq3x3)
        
        file_menu = menu_bar.addMenu('File')
        file_menu.addMenu(n_menu)
        file_menu.addAction(oq_act)
        file_menu.addAction(sq_act)
        file_menu.addAction(sqa_act)
        file_menu.addAction(q_act)
        
        region_menu = menu_bar.addMenu('Region')
        region_menu.addAction(eu_act)
        region_menu.addAction(us_act)
        
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(about)

		#--------------------Buttons--------------------#
		# NOTE: I'm thinking these might be better at the top of the screen, then
		# we will have the section specific buttons/boxes on the left side
        # Add Objects button
        add_button = QPushButton("Add Objects", self)
        add_button.setToolTip('Add elements to the map')
        add_button.move(20, 40)
        add_button.clicked.connect(self.add_click)

        # Edit Object button
        edit_button = QPushButton('Edit Objects', self)
        edit_button.setToolTip('Edit placed objects')
        edit_button.move(20, 70)
        edit_button.clicked.connect(self.edit_click)

        # Darken/Color button
        dark_button = QPushButton('Darken/Color', self)
        dark_button.setToolTip('Darken/color squares on the map')
        dark_button.move(20, 100)
        #dark_button.setGeometry(20, 80, 120, 30)
        #dark_button.resize(dark_button.sizeHint())
        dark_button.clicked.connect(self.dark_click)

        # Import button
        import_button = QPushButton('Import', self)
        import_button.setToolTip('Import icons, maps or quests')
        import_button.move(20, 130)
        import_button.clicked.connect(self.import_click)

        # Export button
        export_button = QPushButton('Export', self)
        export_button.setToolTip('Export icons, maps, or quests')
        export_button.move(20, 160)
        export_button.clicked.connect(self.export_click)
        

        # Display the window
        self.show()
        

  	#Override PyQt's built in closeEvent method to include verification text box
    def closeEvent(self, event):
        reply = QuitMessage().exec_()
        if reply == QMessageBox.Yes:
            event.accept()
        else: 
            event.ignore()
            

    # Function to center main window
    def center_window(self):
    	win_bounds = self.frameGeometry()
    	screen_cp = QDesktopWidget().availableGeometry().center()
    	win_bounds.moveCenter(screen_cp)
    	self.move(win_bounds.topLeft())
    	
    	
    def update_title(self):
    	const = Constants()
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
    	
