# Smart File Organizer

A Python-based file organization tool that automatically categorizes files into folders based on their extensions. It includes duplicate file detection using SHA-256 hashing, collision-safe file movement, logging, and a dry-run mode for previewing operations before making changes.

## Features

- **Automatic File Categorization:** Organizes files into categories such as Documents, Images, Audio, Videos, and Archives.
- **Directory Scanning:** Scans a specified directory and identifies files.
- **Duplicate Detection:** Uses SHA-256 hashing to identify files with identical content.
- **Safe File Movement:** Automatically handles filename collisions by generating unique filenames.
- **Dry-Run Mode:** Previews file movements without modifying the filesystem.
- **Logging:** Records application activities, warnings, and errors.
- **Exception Handling:** Handles common filesystem errors.

## Tech Stack

- Python 3
- pathlib
- shutil
- hashlib
- logging

## Project Structure

```text
smart-file-organizer/
│
├── organizer/
│   ├── __init__.py
│   ├── main.py
│   ├── scanner.py
│   ├── categorizer.py
│   ├── file_manager.py
│   ├── duplicate_detector.py
│   └── logger_config.py
│
├── logs/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd smart-file-organizer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

## Usage

1. Configure the target directory in `organizer/main.py`.
2. Set `DRY_RUN = True` to preview the planned file movements.
3. Run the application:

```bash
python -m organizer.main
```

4. Review the generated logs.
5. Set `DRY_RUN = False` to perform the actual file organization.

**Important:** Test with a sample directory before using the application on important files.

## Example

Before:

```text
organizer_test/
├── resume.pdf
├── photo.jpg
├── song.mp3
├── backup.zip
└── video.mp4
```

After:

```text
organizer_test/
├── Documents/
│   └── resume.pdf
├── Images/
│   └── photo.jpg
├── Audio/
│   └── song.mp3
├── Archives/
│   └── backup.zip
└── Videos/
    └── video.mp4
```

## Learning Outcomes

- Python file and directory handling
- Modular programming
- File hashing and duplicate detection
- Exception handling
- Logging
- Safe filesystem operations
- Project structuring

## Future Improvements

- Graphical user interface using Streamlit or Tkinter.
- Configurable file categories.
- Recursive directory scanning.
- Duplicate file management options.
- Configuration through a JSON file.

## Author

Alan Shaju

GitHub: https://github.com/ALANSHAJU1