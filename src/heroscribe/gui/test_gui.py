import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
#from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

language_dict = {"en":{"add_objects" : "Add Objects",
                       "edit_objects": "Edit Objects",
                       "darken": "Darken/Color",
                       "import":"Import",
                       "export":"Export",
                       "questimate":"Questimate",
                      },
                 "de":{"add_objects" : "Neues Teil",
                       "edit_objects": "Teil bearbeiten",
                       "darken": "abdunkeln / färben",
                       "import":"Import",
                       "export":"Export",
                       "questimate":"Questimate",
                      },
                 "fr":{"add_objects" : "Nouveau Piece",
                       "edit_objects": "Editer Piece",
                       "darken": "sombrer / coulourer",
                       "import":"importer",
                       "export":"exporter",
                       "questimate":"Questimate",
                      },
                 }

class hs2_window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window stats
        self.title = 'Heroscribe 2.0'
        self.left = 10
        self.top = 10
        self.width = 1024
        self.height = 768
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
        self.setGeometry(self.left,self.top, self.width, self.height)
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

        # Questimator button
        quest_button = QPushButton('Questimator', self)
        quest_button.setToolTip('Questimator functionality')
        quest_button.move(20, 170)
        quest_button.clicked.connect(self.quest_click)

        # Display the window
        self.show()

	#--------------------Button Event Handlers--------------------#
	# Add Object button
    @pyqtSlot()
    def add_click(self):
        self.statusBar().showMessage('Add button pressed')

	# Edit Object button
    @pyqtSlot()
    def edit_click(self):
        self.statusBar().showMessage('Edit button pressed')

	# Darken/Color button
    @pyqtSlot()
    def dark_click(self):
        self.statusBar().showMessage('Darken button pressed')

    # Import button
    @pyqtSlot()
    def import_click(self):
    	self.statusBar().showMessage('Import functionality hopefully coming soon!')

    # Export button
    @pyqtSlot()
    def export_click(self):
    	self.statusBar().showMessage('Export functionality hopefully coming soon!')

    # Questimator button
    @pyqtSlot()
    def quest_click(self):
    	self.statusBar().showMessage('Questimator functionality hopefully coming soon!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = hs2_window()
    sys.exit(app.exec_())