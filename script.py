import sys
import os
from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PyQt6.QtCore import Qt
import pyperclip  # Install with: pip install pyperclip

class FolderTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag & Drop Folder to Generate ASCII Tree")
        self.setGeometry(100, 100, 600, 400)

        # Text box to display ASCII tree
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textbox.setFont(QFont("Arial", 12))

        # Initial message with a "drag & drop" hint
        self.textbox.setPlainText("🗂️ Drag and Drop a folder to get an ASCII representation")

        self.setCentralWidget(self.textbox)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

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
        """Recursively generates an ASCII tree for the given folder, ignoring hidden files."""
        tree = f"{folder}\n"
        items = sorted(
            [item for item in os.listdir(folder) if not item.startswith(".")]  # Ignore hidden files
        )
        for i, item in enumerate(items):
            path = os.path.join(folder, item)
            connector = "└── " if i == len(items) - 1 else "├── "
            tree += prefix + connector + item + "\n"
            if os.path.isdir(path):
                new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                tree += self.generate_tree(path, new_prefix)
        return tree

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderTreeApp()
    window.show()
    sys.exit(app.exec())