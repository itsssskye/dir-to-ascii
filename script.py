import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QTextEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PyQt6.QtCore import Qt
import pyperclip  # Install with: pip install pyperclip

class FolderTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Directory to ASCII")  # Updated window title
        self.setGeometry(100, 100, 600, 400)

        # State
        self.filter_list = []
        self.show_hidden = False

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Text box
        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textbox.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.textbox.setPlainText("🗂️ Drag and Drop a folder to get an ASCII representation")
        layout.addWidget(self.textbox)

        # Buttons
        self.filter_button = QPushButton("Set Filtered Files/Folders")
        self.filter_button.clicked.connect(self.set_filter)
        layout.addWidget(self.filter_button)

        self.hidden_button = QPushButton("Show Hidden Files: OFF")
        self.hidden_button.clicked.connect(self.toggle_hidden)
        layout.addWidget(self.hidden_button)

        self.copy_button = QPushButton("Copy ASCII Tree")
        self.copy_button.setEnabled(False)  # Start disabled
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

    def set_filter(self):
        """Opens an input dialog for the user to enter files/folders to ignore."""
        text, ok = QInputDialog.getText(self, "Set Filters", "Enter file/folder names to ignore (comma-separated):", text=", ".join(self.filter_list))
        if ok:
            self.filter_list = [item.strip() for item in text.split(",")]

    def toggle_hidden(self):
        """Toggles whether hidden files are included in the ASCII tree."""
        self.show_hidden = not self.show_hidden
        self.hidden_button.setText(f"Show Hidden Files: {'ON' if self.show_hidden else 'OFF'}")

    def copy_to_clipboard(self):
        """Copies the ASCII tree text to the clipboard."""
        text = self.textbox.toPlainText()
        if text:
            pyperclip.copy(text)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handles when a folder is dragged into the window."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handles when a folder is dropped onto the window."""
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            if os.path.isdir(folder_path):
                ascii_tree = self.generate_tree(folder_path)
                self.textbox.setPlainText(ascii_tree)
                self.copy_button.setEnabled(True)  # Enable copy button

    def generate_tree(self, folder, prefix=""):
        """Recursively generates an ASCII tree for the given folder."""
        tree = f"{folder}\n"
        items = sorted(os.listdir(folder))

        # Apply filters
        items = [item for item in items if item not in self.filter_list]
        if not self.show_hidden:
            items = [item for item in items if not item.startswith(".")]

        for i, item in enumerate(items):
            path = os.path.join(folder, item)
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            new_prefix = prefix + ("    " if is_last else "│   ")

            tree += prefix + connector + item + "\n"

            if os.path.isdir(path):
                tree += self.generate_tree(path, new_prefix)

        return tree

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("ASCII Tree Generator")  # Updated application name for macOS dock
    window = FolderTreeApp()
    window.show()
    sys.exit(app.exec())