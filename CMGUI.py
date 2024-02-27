from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog, QWidget, QListWidget, QPlainTextEdit, QLabel
from PyQt5.QtCore import Qt
import os
from PyQt5.QtWidgets import QMessageBox
import model
import json
import utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Checking before the creation of the window
        self.initialChecklist()

        utils.list_files()

        self.fileList = QListWidget()
        self.current_dir = "./campaign"
        self.updateFileList(self.current_dir)
        self.current_file_path = None

        self.setWindowTitle("Campaign maker GUI")

        mainLayout = QHBoxLayout()
        textLayout = QVBoxLayout()
        fileLayout = QVBoxLayout()

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
        


        fileLayout.addWidget(title_files)
        fileLayout.addWidget(self.fileList, alignment=Qt.AlignRight)
        fileLayout.addWidget(self.button_save, alignment=Qt.AlignLeft)


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

    # Function to update the list of files in the working directory.
    def updateFileList(self, directory):
        self.fileList.clear()
        files = os.listdir(directory)
        if self.current_dir != "./campaign":
            self.fileList.addItem("...")  # Add '...' to the fileList
        for file in files:
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
        else:
            QMessageBox.information(self, 'Information', 'Nothing to save.')

    # Function to send the text from the history to the current file.
    def sendToCurrent(self):
        center_text = self.textEdit_center.toPlainText()
        self.textEdit_top.setPlainText(center_text)
        self.current_file_path = None

    def clearCurrent(self):
        self.textEdit_top.clear()
        self.current_file_path = None

    # Function to initialize the directories and openai api key
    def initialChecklist(self):

        # Create the directory and subdirectories
        os.makedirs("./campaign", exist_ok=True)
        os.makedirs("./campaign/places", exist_ok=True)
        os.makedirs("./campaign/characters", exist_ok=True)
        os.makedirs("./campaign/items", exist_ok=True)
        os.makedirs("./campaign/quests", exist_ok=True)
        os.makedirs("./campaign/others", exist_ok=True)
        
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

def main():
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    """

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # Pause before the script ends
    os.system('pause')

if __name__ == "__main__":
    main()
