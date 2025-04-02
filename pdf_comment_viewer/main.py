import tkinter as tk
from ui import PDFCommentViewerApp
from version import __version__

def main():
    root = tk.Tk()
    app = PDFCommentViewerApp(root)
    root.mainloop()

def run_app():
    main()

if __name__ == "__main__":
    main()