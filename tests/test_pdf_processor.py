import pytest
import os
import tempfile
from pdf_comment_viewer.pdf_processor import extract_comments

class TestPDFProcessor:
    def test_extract_comments_nonexistent_file(self):
        # Test with a file that doesn't exist
        with pytest.raises(FileNotFoundError):
            extract_comments('nonexistent_file.pdf')
    
    def test_extract_comments_empty_file(self):
        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # The function should handle an empty file without crashing
            with pytest.raises(Exception):
                extract_comments(tmp_path)
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)