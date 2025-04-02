#!/usr/bin/env python3
"""
Build script for PDF Comment Viewer
"""

import PyInstaller.__main__
import os
import sys
import platform
import shutil
import importlib.util
import re

def get_version():
    spec = importlib.util.spec_from_file_location(
        "version", 
        os.path.join("pdf_comment_viewer", "version.py")
    )
    version_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_module)
    return version_module.__version__

__version__ = get_version()
# Determine platform-specific settings
if platform.system() == "Windows":
    icon_file = "assets/icon32.ico"
    output_name = f"PDFCommentViewer-{__version__}"
elif platform.system() == "Darwin":  # macOS
    icon_file = "assets/icon32.icns"
    output_name = f"PDFCommentViewer-{__version__}"
else:  # Linux
    icon_file = "assets/icon32.png"
    output_name = f"pdf_comment_viewer-{__version__}"

# Create the assets directory if it doesn't exist
os.makedirs("assets", exist_ok=True)

# Default icon file if none exists - will be a blank icon
if not os.path.exists(icon_file):
    # Create a minimal icon file
    with open(icon_file, "w") as f:
        f.write("")

# Entry point is now in the package directory
entry_point = os.path.join("pdf_comment_viewer", "main.py")

# Check if entry point exists
if not os.path.exists(entry_point):
    print(f"Error: Entry point {entry_point} not found!")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    if os.path.exists("pdf_comment_viewer"):
        print(f"Files in package directory: {os.listdir('pdf_comment_viewer')}")
    sys.exit(1)

# Define PyInstaller arguments
pyinstaller_args = [
    entry_point,  # Main script to bundle from the package
    "--name=%s" % output_name,
    "--onefile",
    "--windowed",
    # Include package modules
    "--paths=pdf_comment_viewer",
    # Add assets
    "--add-data=%s%s%s" % (
        icon_file, 
        os.pathsep, 
        "assets"
    ),
    # Icon
    "--icon=%s" % icon_file,
]

print(f"Building executable for {platform.system()}...")
print(f"Using entry point: {entry_point}")
print(f"PyInstaller arguments: {' '.join(pyinstaller_args)}")

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print(f"\nBuild complete for {platform.system()}!")
print(f"Executable saved to dist/{output_name}{'.exe' if platform.system() == 'Windows' else ''}")

# Verify the output
output_file = os.path.join("dist", output_name)
if platform.system() == "Windows":
    output_file += ".exe"

if os.path.exists(output_file):
    print(f"Successfully created: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
else:
    print(f"WARNING: Expected output file {output_file} was not found!")
    print("Check the PyInstaller output for errors.")
    sys.exit(1)