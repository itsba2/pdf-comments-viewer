import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
from tkinter import filedialog
from pdf_processor import extract_comments
from version import __version__
import sys

class PDFCommentViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"PDF Comment Viewer v{__version__}")
        self.root.geometry("800x600")
        
        self.current_file_path = None
        self.setup_ui()
    
    def setup_ui(self):
                # Setup menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PDF...", command=self.browse_file)
        file_menu.add_command(label="Reset", command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection row
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        file_label = ttk.Label(file_frame, text="PDF File:")
        file_label.pack(side=tk.LEFT, padx=5)
        
        self.file_var = tk.StringVar()
        self.file_var.set("No file selected")
        file_entry = ttk.Entry(file_frame, textvariable=self.file_var, width=50, state="readonly")
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Buttons row
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        browse_button = ttk.Button(button_frame, text="Browse PDF", command=self.browse_file)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        process_button = ttk.Button(button_frame, text="Extract Comments", command=self.process_current_file)
        process_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset)
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Comments", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(
            results_frame, 
            wrap=tk.WORD, 
            width=70, 
            height=20,
            font=("Courier New", 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path and file_path.lower().endswith('.pdf'):
            self.current_file_path = file_path
            self.file_var.set(file_path)
            self.process_pdf(file_path)
    
    def process_current_file(self):
        if self.current_file_path:
            self.process_pdf(self.current_file_path)
        else:
            self.status_var.set("No file selected. Please browse for a PDF file.")
    
    def reset(self):
        self.current_file_path = None
        self.file_var.set("No file selected")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.status_var.set("Ready")
    
    def process_pdf(self, file_path):
        self.status_var.set(f"Processing: {os.path.basename(file_path)}...")
        self.root.update()
        
        try:
            # Try the standard parser first
            comments = extract_comments(file_path, debug_mode=False)
            
            # If no comments found with the standard parser, try the alternate parser
            if not comments:
                self.status_var.set(f"No comments found with standard parser. Trying alternate methods...")
                self.root.update()
                comments = extract_comments(file_path, debug_mode=False, use_alternate=True)
            
            self.display_comments(comments)
            self.status_var.set(
                f"Completed: {os.path.basename(file_path)} - {len(comments)} comments found"
            )
            
            # If no comments found, show diagnostic info
            if not comments:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No comments were found in this PDF file.\n\n")
                self.result_text.insert(tk.END, "Possible reasons:\n")
                self.result_text.insert(tk.END, "1. The PDF doesn't contain any annotations/comments\n")
                self.result_text.insert(tk.END, "2. The annotations use a format not supported by the current parser\n")
                self.result_text.insert(tk.END, "3. The PDF was created with software that uses non-standard annotation formats\n")
                self.result_text.insert(tk.END, "4. The PDF might be encrypted or secured\n")
                self.result_text.config(state=tk.DISABLED)
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"An error occurred: {str(e)}\n\n")
            self.result_text.config(state=tk.DISABLED)
    
    def display_comments(self, comments):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if not comments:
            self.result_text.insert(tk.END, "No comments found in this PDF.")
            self.result_text.config(state=tk.DISABLED)
            return
        
        current_page = None
        
        for comment in comments:
            if current_page != comment.get('page'):
                current_page = comment.get('page')
                if current_page:
                    self.result_text.insert(tk.END, f"\n--- Page {current_page} ---\n\n")
            
            # Use index if available, otherwise just number them sequentially
            index = comment.get('index', 0)
            self.result_text.insert(tk.END, f"Comment #{index+1}:\n")
            
            if 'type' in comment:
                annotation_type = comment['type'].replace('/', '')
                self.result_text.insert(tk.END, f"  Type: {annotation_type}\n")
            
            self.result_text.insert(tk.END, f"  Author: {comment.get('author', 'Unknown')}\n")
            
            if comment.get('date'):
                self.result_text.insert(tk.END, f"  Date: {comment['date']}\n")
                
            self.result_text.insert(tk.END, f"  Content: {comment.get('content', '')}\n\n")
        
        self.result_text.config(state=tk.DISABLED)

    def display_comments(self, comments):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if not comments:
            self.result_text.insert(tk.END, "No comments found in this PDF.")
            self.result_text.config(state=tk.DISABLED)
            return
        
        current_page = None
        
        for comment in comments:
            if current_page != comment.get('page'):
                current_page = comment.get('page')
                if current_page:
                    self.result_text.insert(tk.END, f"\n--- Page {current_page} ---\n\n")
            
            # Use index if available, otherwise just number them sequentially
            index = comment.get('index', 0)
            self.result_text.insert(tk.END, f"Comment #{index+1}:\n")
            
            if 'type' in comment:
                annotation_type = comment['type'].replace('/', '')
                self.result_text.insert(tk.END, f"  Type: {annotation_type}\n")
            
            self.result_text.insert(tk.END, f"  Author: {comment.get('author', 'Unknown')}\n")
            
            if comment.get('date'):
                self.result_text.insert(tk.END, f"  Date: {comment['date']}\n")
                
            self.result_text.insert(tk.END, f"  Content: {comment.get('content', '')}\n\n")
        
        self.result_text.config(state=tk.DISABLED)
    
    def show_about(self):
        """Show the About dialog with application information"""
        about_message = f"PDF Comment Viewer v{__version__}\n\n"
        about_message += "A simple tool for extracting and viewing comments from PDF files.\n\n"
        about_message += "© 2025 S. Batuhan Bilmez\n"
        about_message += "Licensed under MIT License\n\n"
        about_message += f"Python {sys.version.split()[0]}"
        
        messagebox.showinfo("About PDF Comment Viewer", about_message)    