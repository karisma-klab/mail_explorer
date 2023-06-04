#!/usr/bin/env python3

import datetime
import os
import re
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QTextEdit, QSplitter, QDialog, QLabel, QPlainTextDocumentLayout, QFileDialog
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextDocument, QColor

SUMMARIZED_DIR = None
SUMMARIZED_NUM_FILES = None
SEARCHES_DIR = None

def spanish_friendly(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    text = text.lower()
    spanish_friendly_str = ""
    for letter in text:
        if letter in vowels:
            spanish_friendly_str += f"[[={letter}=]]"
        else:
            spanish_friendly_str += letter
    return spanish_friendly_str


class SearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Application")
        self.setGeometry(200, 200, 400, 600)

        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.run_search_command)

        self.search_history_label = QLabel("Search History:")
        self.search_history_table = QTableWidget()
        self.search_history_table.setColumnCount(3)
        self.search_history_table.setHorizontalHeaderLabels(["Search Term", "Results", "Date"])
        self.search_history_table.cellClicked.connect(self.show_search_result)

        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.search_history_label)
        layout.addWidget(self.search_history_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Get data dir
        self.data_dir = str(QFileDialog.getExistingDirectory(self, "Select Data Directory"))
        init_dialog = InitDialog(self.data_dir)
        init_dialog.exec_()

        self.populate_search_history()

    def run_search_command(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            return

        # disable search_button and change text
        self.search_button.setEnabled (False)
        self.search_button.setText ('Running... 0%')

        # Replace spaces in the search term with underscores for the output file name
        output_file = search_term.replace(" ", "_") + ".txt"
        output_file_fullpath = os.path.join(SEARCHES_DIR, output_file)

        # Make search_term spanish accent spanish_friendly
        spanish_friendly_str = spanish_friendly(search_term)

        # Construct the search command
        # command = f'time find summarized/ -type f -print0 | pv -0 -s 3330608 | xargs -0 -P 5 grep -R -i -m 1 "{search_term}" > searches/{output_file}'
        command = f'find {SUMMARIZED_DIR} -type f -print0 | pv -0 -n -s {SUMMARIZED_NUM_FILES} | xargs -0 -P 5 grep -R -i -m 1 "{spanish_friendly_str}" > {output_file_fullpath}'

        process = QProcess()
        process.readyReadStandardError.connect(lambda: self.update_search_status(process))
        process.finished.connect(self.search_finished)
        process.start("bash", ["-c", command])

        self.populate_search_history()

    def update_search_status(self, process):
        # Read the output from the processSEARCHES_DIR
        output = process.readAllStandardError().data().decode()
        output = output.strip()
        try:
            int(output)
            self.search_button.setText(f'Running... {output}%')
        except:
            pass

    def search_finished(self):
        self.search_button.setEnabled (True)
        self.search_button.setText ('Search')
        self.populate_search_history()

    def populate_search_history(self):
        # Clear the search history table
        self.search_history_table.clearContents()
        self.search_history_table.setRowCount(0)

        # Get the list of search history files
        search_files = [f for f in os.listdir(SEARCHES_DIR) if f.endswith(".txt")]

        # Populate the search history table
        for i, file_name in enumerate(search_files):
            search_term = os.path.splitext(file_name)[0].replace("_", " ")
            result_file = os.path.join(SEARCHES_DIR, file_name)
            results = sum(1 for _ in open(f"{result_file}", encoding="latin-1"))
            create_date = datetime.datetime.fromtimestamp(os.path.getctime(f"{result_file}")).strftime('%c')
            self.search_history_table.insertRow(i)
            self.search_history_table.setItem(i, 0, QTableWidgetItem(search_term))
            self.search_history_table.setItem(i, 1, QTableWidgetItem(str(results)))
            self.search_history_table.setItem(i, 2, QTableWidgetItem(create_date))

    def show_search_result(self, row, _):
        file_name = self.search_history_table.item(row, 0).text().replace(" ", "_") + ".txt"
        file_path = os.path.join(SEARCHES_DIR, file_name)
        result_dialog = ResultDialog(file_path)
        result_dialog.exec_()


class ResultDialog(QDialog):
    def __init__(self, file_path):
        super().__init__()

        self.setWindowTitle("Search Result")
        self.setMinimumSize(800, 600)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search term")
        self.search_input.textChanged.connect(self.highlight_search_results)

        self.search_result_text = QTextEdit()
        self.search_result_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_result_text)

        self.setLayout(layout)

        # Load and display the search result file
        with open(file_path, "r", errors='ignore') as file:
            for line in file.readlines():
                if line.find(':') == -1:
                    self.search_result_text.append(line)
                else:
                   filename, text = line.split(':', 1)
                   self.search_result_text.append(filename)
                   self.search_result_text.append(text)
            #self.search_result_text.setPlainText(file.read())

    def highlight_search_results(self):
        search_term = self.search_input.text().strip()

        format = QTextCharFormat()
        format.setBackground(QColor("#FFFF00"))  # Yellow highlight color

        cursor = self.search_result_text.textCursor()
        cursor.setPosition(0)

        highlighter = QTextDocument(self)
        highlighter.setPlainText(self.search_result_text.toPlainText())

        highlight_cursor = QTextCursor(highlighter)
        highlight_cursor.beginEditBlock()

        while not highlight_cursor.isNull() and not highlight_cursor.atEnd():
            highlight_cursor = highlighter.find(search_term, highlight_cursor)
            if not highlight_cursor.isNull():
                selection_start = highlight_cursor.selectionStart()
                selection_end = highlight_cursor.selectionEnd()
                highlight_cursor.setPosition(selection_start, QTextCursor.MoveAnchor)
                highlight_cursor.setPosition(selection_end, QTextCursor.KeepAnchor)
                highlight_cursor.mergeCharFormat(format)
                highlight_cursor.clearSelection()

        highlight_cursor.endEditBlock()

        self.search_result_text.setDocument(highlighter)
        self.search_result_text.setTextCursor(cursor)
        self.search_result_text.ensureCursorVisible()


class InitDialog(QDialog):
    def __init__(self, data_dir):
        super().__init__()

        global SUMMARIZED_DIR
        global SUMMARIZED_NUM_FILES
        global SEARCHES_DIR

        self.setWindowTitle("Configuring...")

        self.message_label = QLabel("Configuring the system... Don't close this window")

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        # check if summarized and searches are on the data_dir
        dirs_in_data_dir =  os.listdir(data_dir)
        if 'summarized' in dirs_in_data_dir:
            SUMMARIZED_DIR = os.path.join(data_dir, 'summarized')
            SUMMARIZED_NUM_FILES = sum([len(files) for r, d, files in os.walk("summarized")])
        else:
            self.message_label.setText("ERROR: 'summarized' folder not found")
            return None

        # setup SEARCHES_DIR
        SEARCHES_DIR = os.path.join(data_dir, 'searches')
        if 'searches' not in dirs_in_data_dir:
            os.mkdir(SEARCHES_DIR)

        self.message_label.setText("READY: all good, close this window now.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())
