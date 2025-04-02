import re
import logging

logger = logging.getLogger(__name__)

def parse_pdf_manually(pdf_file_path):
    """
    Attempt to parse PDF comments using a lower-level approach
    This is a fallback method for PDFs that don't work with pypdf
    
    Args:
        pdf_file_path (str): Path to the PDF file
        
    Returns:
        list: List of potential comments found
    """
    try:
        comments = []
        
        with open(pdf_file_path, 'rb') as file:
            pdf_content = file.read()
            
        # Look for potential annotations using pattern matching
        # This is a simplified approach and might not work for all PDFs
        
        # Look for /Annot objects
        annot_pattern = rb'/Annot\s'
        annot_positions = [m.start() for m in re.finditer(annot_pattern, pdf_content)]
        
        # Look for /Text (comment) annotations
        text_pattern = rb'/Text\s'
        text_positions = [m.start() for m in re.finditer(text_pattern, pdf_content)]
        
        # Look for /Contents entries (comment content)
        contents_pattern = rb'/Contents\s*\(([^\)]*)\)'
        contents_matches = re.finditer(contents_pattern, pdf_content)
        
        for i, match in enumerate(contents_matches):
            try:
                content = match.group(1).decode('latin-1', errors='replace')
                # Try to clean up content
                content = content.replace('\\r', '\r').replace('\\n', '\n')
                content = content.replace('\\(', '(').replace('\\)', ')')
                
                # Look for author pattern near this content
                author = "Unknown"
                search_range = pdf_content[max(0, match.start()-200):match.start()]
                author_match = re.search(rb'/T\s*\(([^\)]*)\)', search_range)
                if author_match:
                    author = author_match.group(1).decode('latin-1', errors='replace')
                
                comments.append({
                    'content': content,
                    'author': author,
                    'date': '',
                    'source': 'alternate_parser'
                })
            except Exception as e:
                logger.debug(f"Error extracting comment content: {str(e)}")
        
        logger.info(f"Alternative parser found {len(comments)} potential comments")
        return comments
        
    except Exception as e:
        logger.error(f"Alternative parser failed: {str(e)}")
        return []


def extract_comments_alternate(pdf_file_path):
    """
    Extract comments using PyMuPDF if available, otherwise fallback to manual parsing
    
    Args:
        pdf_file_path (str): Path to the PDF file
        
    Returns:
        list: List of dictionaries containing comment information
    """
    comments = []
    
    # Try using PyMuPDF (fitz) if available
    try:
        import fitz
        logger.info("Using PyMuPDF for comment extraction")
        
        doc = fitz.open(pdf_file_path)
        
        for page_num, page in enumerate(doc, 1):
            annots = page.annots()
            for i, annot in enumerate(annots):
                annot_info = annot.info
                annot_type = annot.type[1]  # Get annotation type
                
                content = annot_info.get("content", "")
                author = annot_info.get("title", "Unknown")
                date = annot_info.get("modDate", "")
                
                # Skip empty annotations unless they're highlights
                if not content and annot_type not in [8, 9, 10, 11]:  # highlight, underline, strikeout, squiggly
                    continue
                    
                comments.append({
                    'page': page_num,
                    'index': i,
                    'content': content,
                    'author': author,
                    'date': date,
                    'type': f'/{annot_type}',
                    'source': 'pymupdf'
                })
                
        logger.info(f"PyMuPDF found {len(comments)} comments")
        return comments
        
    except ImportError:
        logger.info("PyMuPDF not available, falling back to manual parsing")
        # Fallback to manual parsing
        return parse_pdf_manually(pdf_file_path)