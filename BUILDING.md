# Building Executables for PDF Comment Viewer

This document explains how to build standalone executables for the PDF Comment Viewer application for Windows, macOS, and Linux, including version management.

## Prerequisites

Before building executables, you need to install the following dependencies:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Managing Versions

The application version is defined in `pdf_comment_viewer/version.py`. The version follows semantic versioning (major.minor.patch).

### Updating the Version

You can update the version manually by editing `pdf_comment_viewer/version.py`, or use the provided utility script:

```bash
# Increment the patch version (e.g., 1.0.0 -> 1.0.1)
python update_version.py patch

# Increment the minor version (e.g., 1.0.0 -> 1.1.0)
python update_version.py minor

# Increment the major version (e.g., 1.0.0 -> 2.0.0)
python update_version.py major
```

## Building Manually

The application can be built using the provided `bundle.py` script, which handles platform-specific settings and includes the current version number in the executable name.

To build the application:

```bash
python bundle.py
```

### Output Files

The build process creates executables with version numbers included in the filename:

- Windows: `dist/PDFCommentViewer-1.0.0.exe`
- macOS: `dist/PDFCommentViewer-1.0.0` or `dist/PDFCommentViewer-1.0.0.app`
- Linux: `dist/pdf_comment_viewer-1.0.0`

### What happens during the build

The `bundle.py` script:

1. Reads the current version from `pdf_comment_viewer/version.py`
2. Determines the platform-specific settings
3. Creates a standalone executable with the version in the filename
4. Places the executable in the `dist` directory

## Using GitHub Actions for Automated Builds

This repository includes a GitHub Actions workflow that automatically builds executables for all platforms when you push a new tag. The workflow uses the version number defined in `pdf_comment_viewer/version.py`.

To create a new release:

1. Update the version using the update script:
   ```bash
   python update_version.py minor  # or patch/major
   git add pdf_comment_viewer/version.py
   git commit -m "Bump version to X.Y.Z"
   ```

2. Tag your commit with a version number (should match the version in the code):
   ```bash
   git tag v$(python -c "from pdf_comment_viewer import __version__; print(__version__)")
   git push origin --tags
   ```

3. The GitHub Actions workflow will:
   - Build executables for all platforms with the version number in the filenames
   - Create a GitHub Release with a title that includes the version number
   - Attach the versioned executables to the release

## Troubleshooting

If you encounter issues when building the executables:

- Make sure all dependencies are installed correctly
- Check that the package structure is correct and that imports are properly resolved
- Verify that `pdf_comment_viewer/version.py` exists and contains a valid version string
- Run `python bundle.py` with verbose output to see detailed error messages:
  ```bash
  python -m PyInstaller --debug=all main.py
  ```

If you're building on GitHub Actions and encounter issues, check the workflow logs for details.