import sys
import os
from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PyQt6.QtCore import Qt
import pyperclip  # Install with: pip install pyperclip

class FolderTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag & Drop Folder to Generate ASCII Tree")
        self.setGeometry(100, 100, 600, 400)

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
        self.textbox.setFont(QFont("Arial", 12))
        self.textbox.setPlainText("🗂️ Drag and Drop a folder to get an ASCII representation")
        layout.addWidget(self.textbox)

        # Filter button
        self.filter_list = []
        self.filter_button = QPushButton("Set Filtered Files/Folders")
        self.filter_button.clicked.connect(self.set_filter)
        layout.addWidget(self.filter_button)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

    def set_filter(self):
        """Opens an input dialog for the user to enter files/folders to ignore."""
        text, ok = QInputDialog.getText(self, "Set Filters", "Enter file/folder names to ignore (comma-separated):")
        if ok:
            self.filter_list = [item.strip() for item in text.split(",")]

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
                pyperclip.copy(ascii_tree)  # Copy to clipboard

    def generate_tree(self, folder, prefix=""):
        """Recursively generates an ASCII tree for the given folder, ignoring hidden and filtered files."""
        tree = f"{folder}\n"
        items = sorted(
            [item for item in os.listdir(folder) if not item.startswith(".") and item not in self.filter_list]
        )

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
    window = FolderTreeApp()
    window.show()
    sys.exit(app.exec())