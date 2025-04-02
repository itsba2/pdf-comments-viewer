# PDF Comment Viewer

A simple application to extract and display comments from PDF files.

## Features

- Browse and select PDF files
- Extract comments from PDF files
- Display comments in a structured manner, organized by page
- Show author, date, and content for each comment
- Reset functionality for quick switching between files

## Installation

### Pre-built Executables

Download the latest executable for your platform from the [Releases](https://github.com/yourusername/pdf-comment-viewer/releases) page:

- Windows: `PDFCommentViewer-Windows.exe`
- macOS: `PDFCommentViewer-MacOS.dmg`
- Linux: `PDFCommentViewer-Linux.tar.gz`

### From Source

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python pdf_comment_viewer/main.py
```

## Building Executables

See [BUILDING.md](BUILDING.md) for detailed instructions on how to build executables for Windows, macOS, and Linux.

## How It Works

1. The application allows you to select a PDF file by browsing
2. Once a PDF is selected, the application extracts all comments/annotations from the file
3. Comments are displayed in a structured format, organized by page number
4. For each comment, the application shows:
   - Comment number
   - Type of annotation (if available)
   - Author name
   - Date (if available)
   - Comment content
5. If no comments are found with the standard parser, an alternative parser is automatically used
6. If still no comments are found, diagnostic information is displayed

## Troubleshooting


## Attribution

App icon is downloaded from

[Comments icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/comments)