from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog, QWidget, QListWidget, QPlainTextEdit, QLabel
from PyQt5.QtCore import Qt, QBuffer, QIODevice
import os
from PyQt5.QtWidgets import QMessageBox
import model
import json
import utils
import settings
import functions
from PyQt5.QtGui import QPixmap
import urllib.request

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Checking before the creation of the window
        self.initialChecklist()

        utils.list_files()

        self.fileList = QListWidget()
        self.current_dir = ".\\campaign"
        self.updateFileList(self.current_dir)
        self.current_file_path = None

        self.setWindowTitle("Campaign maker GUI")

        mainLayout = QHBoxLayout()
        pictureLayout = QVBoxLayout()
        textLayout = QVBoxLayout()
        fileLayout = QVBoxLayout()

        # Picture of the current piece of lore
        self.picture = QLabel()

        # Button to save the current picture
        self.button_save_picture = QPushButton("Save picture")
        self.button_save_picture.clicked.connect(self.savePicture)

        # Button to generate a new picture
        self.button_generate_picture = QPushButton("Generate picture")
        self.button_generate_picture.clicked.connect(self.generatePicture)

        # Text editor for the current viewed file.
        self.textEdit_top = QPlainTextEdit()
        title_top = QLabel()
        title_top.setText("Current file:")

        # Button to clear the current file.
        self.button_clear_current = QPushButton("Clear")
        self.button_clear_current.clicked.connect(self.clearCurrent)

        # Text editor for the model response.
        self.textEdit_center = QPlainTextEdit()
        self.textEdit_center.setReadOnly(True)
        title_center = QLabel()
        title_center.setText("Model generation:")

        # Button to copy text from response to current file.
        self.button_send_to_current = QPushButton("Send to current")
        self.button_send_to_current.clicked.connect(self.sendToCurrent)

        # Text editor for the user input.
        self.textEdit_bottom = QTextEdit()
        title_bottom = QLabel()
        title_bottom.setText("User input:")

        # Button to validate the user input.
        self.button_validate = QPushButton("Send to model")
        self.button_validate.clicked.connect(self.validateText)

        

        # List of files in the current directory.
        title_files = QLabel()
        title_files.setText("Working directory:")
        self.fileList.itemClicked.connect(self.loadFile)
        self.fileList.itemDoubleClicked.connect(self.openDirectory)
        

        # Button to save the current file.
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.saveText)


        # Creation of the picture layout
        pictureLayout.addWidget(self.picture)

        pictureLayout.addWidget(self.button_save_picture)

        pictureLayout.addWidget(self.button_generate_picture)


        # Creation of the window layout
        textLayout.addWidget(title_top)
        textLayout.addWidget(self.textEdit_top,8)

        textLayout.addWidget(self.button_clear_current)

        textLayout.addWidget(title_center)
        textLayout.addWidget(self.textEdit_center,8)

        textLayout.addWidget(self.button_send_to_current)

        textLayout.addWidget(title_bottom)
        textLayout.addWidget(self.textEdit_bottom,1)

        textLayout.addWidget(self.button_validate)


        # Creation of the file layout
        fileLayout.addWidget(title_files)
        fileLayout.addWidget(self.fileList, alignment=Qt.AlignRight)
        fileLayout.addWidget(self.button_save, alignment=Qt.AlignLeft)


        # Adding the layouts to the main layout
        mainLayout.addLayout(pictureLayout,3)
        mainLayout.addLayout(textLayout,3)
        mainLayout.addLayout(fileLayout,1)


        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)


        # Initiate the language model
        self.client, self.messages = model.initiate_conversation()

    # Function to validate the user input and communicate with the model.
    def validateText(self):
        user_text = self.textEdit_bottom.toPlainText()
        current_file_text = self.textEdit_top.toPlainText()
        self.messages, response = model.handle_input(user_text, self.client, self.messages)

        self.textEdit_center.setPlainText(response)

    # Function to load a file from the working directory.
    def loadFile(self, item):
        file_path = os.path.join(self.current_dir, item.text())
        self.current_file_path = file_path
        if os.path.isdir(file_path):
            return  # Do nothing if the clicked item is a directory

        with open(file_path, 'r') as file:
            self.textEdit_top.setPlainText(file.read())
        
        # Update the picture
        picture_path = file_path.replace('.txt', '.png')
        self.picture.setPixmap(QPixmap(picture_path))

    # Function to update the list of files in the working directory.
    def updateFileList(self, directory):
        self.fileList.clear()
        files = os.listdir(directory)
        if self.current_dir != ".\\campaign":
            self.fileList.addItem("...")  # Add '...' to the fileList
        for file in files:
            if not file.endswith('.png'):
                self.fileList.addItem(file)

    # Function to open a directory from the working directory.
    def openDirectory(self, item):
        file_path = os.path.join(self.current_dir, item.text())
        if item.text() == '...':
            self.current_dir = os.path.dirname(self.current_dir)
        elif os.path.isdir(file_path):
            self.current_dir = file_path
        else:
            return  # Do nothing if the clicked item is a file

        self.updateFileList(self.current_dir)

    # Function to save the current file.
    def saveText(self):
        if self.textEdit_top.toPlainText():
            plainText = self.textEdit_top.toPlainText()
            try:
                json_data = json.loads(plainText)
            except json.JSONDecodeError:
                QMessageBox.warning(self, 'Error', 'Invalid JSON format.')
            
            name = json_data['name']
            name = name.replace(' ', '_')
            name = name.lower()

            type = json_data['type']
            type = type.replace(' ', '_')
            type = type.lower()

            file_path = f"./campaign/{type}/{name}.txt"
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write(plainText)
                    QMessageBox.information(self, 'Information', 'File created.')
                    self.updateFileList(self.current_dir)
            else:
                with open(file_path, 'w') as file:
                    file.write(plainText)
                    QMessageBox.information(self, 'Information', 'File saved.')
            self.current_file_path = file_path
        else:
            QMessageBox.information(self, 'Information', 'Nothing to save.')

    # Function to send the text from the model to the current file.
    def sendToCurrent(self):
        center_text = self.textEdit_center.toPlainText()
        self.textEdit_top.setPlainText(center_text)
        self.current_file_path = None

    # Function to clear the current file.
    def clearCurrent(self):
        self.textEdit_top.clear()
        self.current_file_path = None

    # Function to initialize the directories and openai api key
    def initialChecklist(self):

        # Create the settings.ini file
        settings.createSettingsIni()

        # Create the campaign directory and functions subdirectory
        os.makedirs(".\\campaign", exist_ok=True)
        os.makedirs(".\\campaign\\others", exist_ok=True)
        os.makedirs(".\\campaign\\functions", exist_ok=True)
        functions.createFunctionsIni()

        # Create the directories for the campaign from the functions files
        utils.createDirectoriesFromFunctions()

        # Check that the .env file exists
        if not os.path.exists(".env"):
            # Asking the user for the openai api key
            openaiApiKey, ok = QInputDialog.getText(self, "Question", "Enter your openai api key:")
            if ok:
                with open(".env", "w") as file:
                    file.write(f'OPENAI_API_KEY = {openaiApiKey}')
                print("The .env file has been created.")
            else:
                QMessageBox.information(self, 'Information', 'The program will not work without the openai api key.')

    # Function to generate a picture from the current file
    def generatePicture(self):
        if self.current_file_path:
            picture_url = model.generatePicture(self.client, self.current_file_path)
            data = urllib.request.urlopen(picture_url).read()

            buffer = QBuffer()
            buffer.open(QIODevice.ReadWrite)
            buffer.write(data)
            buffer.seek(0)

            pixmap = QPixmap()
            pixmap.loadFromData(buffer.readAll())
            self.picture.setPixmap(QPixmap(pixmap))
        else:
            QMessageBox.information(self, 'Information', 'Save before generating a picture.')

    # Function to save the current picture
    def savePicture(self):
        if self.current_file_path:
            picture_path = self.current_file_path.replace('.txt', '.png')
            pixmap = self.picture.pixmap()
            pixmap.save(picture_path)
            QMessageBox.information(self, 'Information', 'Picture saved.')
        else:
            QMessageBox.information(self, 'Information', 'Save before saving a picture.')

def main():

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # Pause before the script ends
    os.system('pause')

if __name__ == "__main__":
    main()
