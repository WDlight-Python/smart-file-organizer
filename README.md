# Smart File Organizer 🚀

## Project Overview

This Python automation project is a command-line utility designed to help users automatically sort and organize files within a specified directory into categorized subfolders (e.g., Images, Documents, Videos, Audio, Archives, Other). It aims to declutter folders like 'Downloads' with ease and safety.

## Features

*   **Intelligent Scanning:** Recursively scans a given directory to identify all files.
*   **Category-Based Sorting:** Automatically classifies files based on their extensions into predefined categories.
*   **Interactive User Interface:** Guides the user through the organization process with clear prompts and options.
*   **File Selection:** Allows users to choose specific files to organize or select all.
*   **Dry Run (Preview):** Shows a preview of proposed file moves before any actual changes are made to ensure user confidence.
*   **Conflict Resolution:** Automatically renames files (e.g., `photo (1).jpg`) to prevent overwriting existing files with the same name.
*   **Comprehensive Logging:** Maintains a detailed log file (`.organizer_log.txt`) of all moved files, including timestamps and destination paths, for traceability and potential undo operations.
*   **Modularity:** Separates core logic (`organizer.py`) from the user interface (`main.py`) for better maintainability and reusability.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPO_URL_HERE]
    cd smart-file-organizer
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install black ruff pylint
    ```

## Usage

To run the organizer, navigate to the project directory in your terminal and execute:

```bash
python main.py
```

The program will then prompt for the folder path to organize and guide through the process.

## Project Structure

```
smart-file-organizer/
├── core/                  # Contains the core logic (functions without user interaction)
│   ├── __init__.py        # Makes 'core' a Python package
│   └── organizer.py       # Core file scanning, categorization, and moving logic
├── venv/                  # Python virtual environment (ignored by Git)
├── .gitignore             # Specifies files/folders to be ignored by Git
├── main.py                # Main entry point and user interface logic
└── README.md              # Project documentation (this file)
```

## Contribution

Feel free to fork the repository, make improvements, and submit pull requests. All contributions are welcome!

## License

This project is open-source and available under the [MIT License](LICENSE-optional-but-recommended.md).

## Contact

For any inquiries, please contact [Your GitHub Username/Email here].
