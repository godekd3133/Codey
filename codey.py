import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QCheckBox
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QIcon, QPixmap
import openai
import pyperclip
from PyQt5.QtCore import Qt

class LanguageConverter(QMainWindow):
    def drawImage(self, path, posX, posY):
        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap(path)
        self.image.setPixmap(self.pixmap)
        self.image.resize(self.pixmap.width(), self.pixmap.height())
        self.image.setScaledContents(False)
        
        posY = posY - self.pixmap.height()
        self.image.move(0,0)
        self.image.move(posX, posY)
        return self.image
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Language Converter")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setGeometry(100, 100, 1280, 720)
        self.setFixedSize(1280, 720)
        main_layout = QVBoxLayout()
        
        top_layout = QHBoxLayout()
       # main_layout.addLayout(top_layout)

        source_layout = QVBoxLayout()
    #    top_layout.addLayout(source_layout)
        
        self.setStyleSheet("background-color: #191D23;")

        self.drawImage('images/logo.png', 40, 50)
        self.drawImage('images/icon/dark/inputcode.png', 40, 135)
        self.drawImage('images/Input Code.png', 72, 131)
        self.drawImage('images/icon/dark/outputcode.png', 660, 135)
        self.drawImage('images/Output Code.png', 692, 131)
    
        self.drawImage('images/Rectangle 5.png', 40, 141+539)
        self.drawImage('images/Rectangle 5.png', 660, 141+539)
        self.drawImage('images/Rectangle 14.png', 540-52/2, 636+32)
        self.drawImage('images/Convert.png', 530, 654)
        main_layout = QVBoxLayout()
        
        main_layout.addLayout(top_layout)
        self.input_field = QTextEdit(self)
        self.input_field.setPlaceholderText("Your input code here")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-image: url(images/Rectangle 5.png);
                background-attachment: fixed;
                color: white;
                border: 1px solid #2C313E;
                border-radius: 5px;
            }
        """)
        self.input_field.setGeometry(40, 141, 600, 539)  
        self.output_field = QTextEdit(self)
        self.output_field.setPlaceholderText("Your output code here")
        self.output_field.setStyleSheet("""
            QTextEdit {
                     background-image: url(images/Rectangle 5.png);
                color: white;
                border: 1px solid #2C313E;
                border-radius: 5px;
            }
        """)
        self.output_field.setGeometry(660, 141, 600, 539)  # Set position and size directly
        
        # Create a Convert button with background image
        self.convert_button = QPushButton(self)
        self.convert_button.setGeometry(530, 634, 100, 40)  # Set position and size
        self.convert_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                background-image: url(images/Convert.png);
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton:hover {
                background-color: transparent;
                background-image: url(images/Convert_hover.png);  # Optional hover effect image
            }
        """)
        self.convert_button.clicked.connect(self.convert)

        # QComboBox 생성 및 설정
        self.source_combo = QComboBox(self)
        self.source_combo.setGeometry(184, 105, 200, 30)  # 위치와 크기 설정
        self.source_combo.addItems(["Python", "Java", "C++"])  # 드롭다운 항목 추가
        self.source_combo.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                color: white;
                border: 1px solid #2C313E;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2C313E;
                color: white;
                border: 1px solid #2C313E;
                selection-background-color: #3A3F51;
            }
        """)

        # 또 다른 QComboBox 생성 및 설정
        self.target_combo = QComboBox(self)
        self.target_combo.setGeometry(820, 105, 200, 30)  # 위치와 크기 설정
        self.target_combo.addItems(["Python", "Java", "C++"])  # 드롭다운 항목 추가
        self.target_combo.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                color: white;
                border: 1px solid #2C313E;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2C313E;
                color: white;
                border: 1px solid #2C313E;
                selection-background-color: #3A3F51;
            }
        """)
        self.annotation_checkbox = QCheckBox("Annotation", self)
        self.annotation_checkbox.setGeometry(1104, 108, 200, 20)
        self.annotation_checkbox.setStyleSheet("color: white;")
        
        
        self.convert_button = QPushButton(self)
        self.convert_button.setGeometry(1195, 100, 40, 40)  # Set position and size
        self.convert_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                background-image: url(images/Group 9.png);
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton:hover {
                background-color: transparent;
                background-image: url(images/Group 9.png);  # Optional hover effect image
            }
        """)
        self.convert_button.clicked.connect(self.copy_to_clipboard)
        
        self.convert_button = QPushButton(self)
        self.convert_button.setGeometry(1225, 100, 40, 40)  # Set position and size
        self.convert_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                background-image: url(images/Group 8.png);
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton:hover {
                background-color: transparent;
                background-image: url(images/Group 8.png);  # Optional hover effect image
            }
        """)
        self.convert_button.clicked.connect(self.save_to_file)
    def convert(self):
        source_language = self.source_combo.currentText()
        target_language = self.target_combo.currentText()
        input_text = self.input_field.toPlainText()
        promptstr = "12421412"
        if self.annotation_checkbox.isChecked():
            promptstr = f"Convert the following {source_language} code to {target_language} code and include comments about the key differences and important as Korean, given considerations:\n{input_text} all comments should be in Korean."
        else:
            promptstr = f"Convert the following {source_language} code to {target_language} code:\n{input_text} "

        # Perform the conversion here
        output_text = self.get_completion(promptstr)

        self.output_field.setPlainText(output_text)


    def highlight_output(self, text):
        self.output_field.clear()
        cursor = self.output_field.textCursor()
        format = QTextCharFormat()
                
        lines = text.split('\n')
        for line in lines:
            if '#' in line:
                before_comment, comment = line.split('#', 1)
                cursor.insertText(before_comment)
                format.setForeground(QColor('orange'))
                cursor.setCharFormat(format)
                cursor.insertText('#' + comment)
                format.setForeground(QColor('white'))
                cursor.setCharFormat(format)
            elif '//' in line:
                before_comment, comment = line.split('#', 1)
                cursor.insertText(before_comment)
                format.setForeground(QColor('orange'))
                cursor.setCharFormat(format)
                cursor.insertText('#' + comment)
                format.setForeground(QColor('white'))
                cursor.setCharFormat(format)
            else:
                cursor.insertText(line)
            cursor.insertBlock()

    def copy_to_clipboard(self):
        text = self.output_field.toPlainText()
        pyperclip.copy(text)

    def save_to_file(self):
        text = self.output_field.toPlainText()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(text)

    def get_completion(self,promptString, model="gpt-3.5-turbo"):
       messages = [{"role": "user", "content": promptString}]
       response = openai.ChatCompletion.create(
           model=model,
           messages=messages,
           temperature=0,
       )
       return response.choices[0].message["content"]

if __name__ == "__main__":
    openai.api_key = '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'
    app = QApplication(sys.argv)
    converter = LanguageConverter()
    converter.show()
    sys.exit(app.exec())
