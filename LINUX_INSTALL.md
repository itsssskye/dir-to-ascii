# 🐧 Linux Installation Guide  

Follow these steps to install and run the ASCII Tree Generator on Linux.  

## ✅ Prerequisites  

Ensure you have **Python 3.10+** installed. Most Linux distributions come with Python pre-installed. Check your version with:
```python3 --version```

If Python is not installed, use your package manager:
	•	Debian/Ubuntu:
            ```sudo apt update && sudo apt install python3 python3-pip -y```
	•	Arch Linux:
            ```sudo pacman -S python python-pip```
	•	Fedora:
            ```sudo dnf install python3 python3-pip -y```

## 🔧 Installation Steps

1️⃣ Install required dependencies:
```pip install pyqt6 pyperclip```

⚠️ If you get an externally-managed-environment error, use:
```pip install --break-system-packages pyqt6 pyperclip```

Alternatively, set up a virtual environment:
```python3 -m venv venv
source venv/bin/activate
pip install pyqt6 pyperclip```

2️⃣ Download the script:
Clone the repository or download script.py manually.
```git clone https://github.com/itsssskye/dir-to-ascii.git
cd dir-to-ascii```

3️⃣ Run the script:
```python3 script.py```

## 🔄 Reusing Steps

1️⃣ Navigate to the script’s directory:
```cd dir-to-ascii```

2️⃣ Run the script:
```python3 script.py```

⸻

🛠 Troubleshooting
	•	“Command not found” errors? Ensure Python and dependencies are installed correctly.
	•	Issues with PyQt6? Try reinstalling it:
            ```pip uninstall pyqt6 -y && pip install pyqt6```
	•	Need help? Check the [README](README.md) or open an issue on GitHub.

🎉 You’re all set! Check the [README](README.md) on how to use it!