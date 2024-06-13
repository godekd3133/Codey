import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor
import openai
import pyperclip

class LanguageConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Language Converter")
        self.setGeometry(100, 100, 1280, 720)

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        source_layout = QVBoxLayout()
        top_layout.addLayout(source_layout)

        self.source_label = QLabel("Source Language:")
        source_layout.addWidget(self.source_label)

        self.source_combo = QComboBox()
        self.source_combo.addItem("Python")
        self.source_combo.addItem("JavaScript")
        source_layout.addWidget(self.source_combo)

        target_layout = QVBoxLayout()
        top_layout.addLayout(target_layout)

        self.target_label = QLabel("Target Language:")
        target_layout.addWidget(self.target_label)

        self.target_combo = QComboBox()
        self.target_combo.addItem("Java")
        self.target_combo.addItem("C++")
        target_layout.addWidget(self.target_combo)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        main_layout.addWidget(self.convert_button)

        input_output_layout = QHBoxLayout()
        main_layout.addLayout(input_output_layout)

        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Your input code here")
        self.input_field.textChanged.connect(self.highlight_input)
        input_output_layout.addWidget(self.input_field)

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        input_output_layout.addWidget(self.output_field)

        # Add buttons for copying to clipboard and saving to file
        buttons_layout = QHBoxLayout()
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        buttons_layout.addWidget(self.copy_button)

        self.save_button = QPushButton("Save to TXT")
        self.save_button.clicked.connect(self.save_to_file)
        buttons_layout.addWidget(self.save_button)

        main_layout.addLayout(buttons_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def highlight_input(self):
        self.input_field.blockSignals(True)
        cursor = self.input_field.textCursor()
        position = cursor.position()
        
        cursor.select(QTextCursor.Document)
        document_text = cursor.selectedText()
        cursor.removeSelectedText()
        
        lines = document_text.split('\n')
        format = QTextCharFormat()
        
        for line in lines:
            if '#' in line:
                before_comment, comment = line.split('#', 1)
                cursor.insertText(before_comment)
                format.setForeground(QColor('orange'))
                cursor.setCharFormat(format)
                cursor.insertText('#' + comment)
                format.setForeground(QColor('black'))
                cursor.setCharFormat(format)
            else:
                cursor.insertText(line)
            cursor.insertBlock()
        
        cursor.setPosition(position)
        self.input_field.setTextCursor(cursor)
        self.input_field.blockSignals(False)

    def convert(self):
        source_language = self.source_combo.currentText()
        target_language = self.target_combo.currentText()
        input_text = self.input_field.toPlainText()

        # Perform the conversion here
        output_text = get_completion(f"Convert the following {source_language} code to {target_language} code: {input_text}")
        self.highlight_output(output_text)

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
                format.setForeground(QColor('black'))
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

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    openai.api_key = 'sk-proj-5lIWzAK4KaFzu9GOtpbbT3BlbkFJF1MRTHOHr12TOdtVDZfu'

    app = QApplication(sys.argv)
    converter = LanguageConverter()
    converter.show()
    sys.exit(app.exec())