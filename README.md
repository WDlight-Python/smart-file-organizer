# Smart File Organizer 🚀

## Project Overview
This program helps you clean up your messy folders! It automatically sorts your files (like pictures, documents, and videos) into neat folders.

## Features
*   **Intelligent Scanning:** Finds all files in a folder.
*   **Automatic Sorting:** Moves files based on their type (e.g., `.jpg` to Images folder).
*   **Interactive:** Asks you what to move and shows a preview.
*   **Safe:** Prevents overwriting files and logs everything.

## How to Install (Simple Steps)

### Step 1: Get the program
Open your computer's terminal (or command prompt) and run:
```bash
git clone https://github.com/WDlight-Python/smart-file-organizer
cd smart-file-organizer
```

### Step 2: Set up the "Safety Box" (Virtual Environment)
*Choose your computer type:*

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install helper tools
In the same terminal, run:
```bash
pip install black ruff pylint
```

## How to Use It

1. Make sure you have activated the "Safety Box" (you should see `(venv)` in your terminal prompt).
2. Run the program by typing:
   ```bash
   python main.py
   ```
3. Type the folder path you want to clean up, and follow the simple steps on the screen.

---

## Project Structure
*   `main.py`: The friendly interface you talk to.
*   `core/organizer.py`: The smart engine that does the work.
*   `.gitignore`: Tells Git to ignore unnecessary files.
*   `organizer_log.txt`: A history book of everything moved.

---
*Created with Python, Git, and curiosity!*
