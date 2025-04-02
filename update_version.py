#!/usr/bin/env python3
"""
Script to update the version number of the PDF Comment Viewer application.
Usage: python update_version.py [major|minor|patch]
"""

import os
import sys
import re

VERSION_FILE = os.path.join("pdf_comment_viewer", "version.py")

def read_version():
    """Read the current version from version.py"""
    with open(VERSION_FILE, 'r') as f:
        content = f.read()
    
    # Extract version with regex
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find version string in version.py")
    
    return match.group(1)

def write_version(version):
    """Write the new version to version.py"""
    with open(VERSION_FILE, 'r') as f:
        content = f.read()
    
    # Replace version with regex
    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{version}"',
        content
    )
    
    with open(VERSION_FILE, 'w') as f:
        f.write(new_content)

def update_version(increment_type):
    """Update the version according to semantic versioning"""
    current = read_version()
    
    # Split version into components
    try:
        major, minor, patch = current.split('.')
        major, minor, patch = int(major), int(minor), int(patch)
    except ValueError:
        print(f"Error: Current version '{current}' does not follow semantic versioning (major.minor.patch)")
        sys.exit(1)
    
    # Increment according to type
    if increment_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif increment_type == 'minor':
        minor += 1
        patch = 0
    elif increment_type == 'patch':
        patch += 1
    else:
        print(f"Error: Unknown increment type '{increment_type}'. Use 'major', 'minor', or 'patch'")
        sys.exit(1)
    
    # Create new version string
    new_version = f"{major}.{minor}.{patch}"
    
    # Write the new version
    write_version(new_version)
    
    print(f"Updated version: {current} -> {new_version}")
    return new_version

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_version.py [major|minor|patch]")
        sys.exit(1)
    
    increment_type = sys.argv[1].lower()
    update_version(increment_type)

if __name__ == "__main__":
    main()