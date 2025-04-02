import pypdf
import logging

from alternate_parser import extract_comments_alternate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_contents_from_popup(annot_obj):
    """Extract contents from a popup annotation if present"""
    if '/Popup' in annot_obj:
        popup = annot_obj['/Popup']
        if popup:
            popup_obj = popup.get_object()
            return popup_obj.get('/Contents', '')
    return ''

def extract_comments(pdf_file_path, debug_mode=False, use_alternate=False):
    """
    Extract comments from a PDF file
    
    Args:
        pdf_file_path (str): Path to the PDF file
        debug_mode (bool): Whether to log detailed debug information
    
    Returns:
        list: List of dictionaries containing comment information
    """
    comments = []
    annotation_types_found = set()
    
    # Try alternate parser first if requested
    if use_alternate:
        logger.info("Attempting to use alternate PDF parser")
        alternate_comments = extract_comments_alternate(pdf_file_path)
        if alternate_comments:
            logger.info(f"Alternate parser found {len(alternate_comments)} comments")
            return alternate_comments
        logger.info("Alternate parser didn't find comments, falling back to pypdf")
    
    try:
        reader = pypdf.PdfReader(pdf_file_path)
        if reader.is_encrypted:
            try:
                reader.decrypt('')  # Try empty password
                logger.info("Successfully decrypted PDF with empty password")
            except:
                logger.warning("PDF is encrypted and could not be decrypted with empty password")
                # Try alternate parser as fallback for encrypted PDFs
                logger.info("Trying alternate parser for encrypted PDF")
                alternate_comments = extract_comments_alternate(pdf_file_path)
                if alternate_comments:
                    return alternate_comments
                return []
        
        # Supported annotation subtypes
        comment_subtypes = [
            '/Text', '/FreeText', '/Highlight', '/Underline',
            '/Squiggly', '/StrikeOut', '/Stamp', '/Caret',
            '/Ink', '/Square', '/Circle', '/Polygon', '/PolyLine', '/Line',
            '/FileAttachment', '/Sound', '/Note'
        ]
        
        for page_num, page in enumerate(reader.pages, 1):
            annotations = []
            
            # Get annotations
            if '/Annots' in page:
                # Handle direct annotations
                annots = page['/Annots']
                if annots:
                    try:
                        # Handle both direct and indirect annotation arrays
                        if isinstance(annots, list):
                            annotations.extend(annots)
                        else:
                            # Get the actual object if it's a reference
                            annots_obj = annots.get_object()
                            if isinstance(annots_obj, list):
                                annotations.extend(annots_obj)
                    except Exception as e:
                        logger.warning(f"Error processing annotations on page {page_num}: {str(e)}")
            
            for i, annot in enumerate(annotations):
                try:
                    # Get annotation object (handle indirect references)
                    annot_obj = annot.get_object() if hasattr(annot, 'get_object') else annot
                    
                    if not annot_obj:
                        continue
                    
                    # Get annotation subtype
                    subtype = annot_obj.get('/Subtype', '')
                    
                    # Track all annotation types for debugging
                    if debug_mode:
                        annotation_types_found.add(subtype)
                    
                    # Only process comment-like annotations
                    if subtype in comment_subtypes:
                        # Get content directly or from popup
                        content = annot_obj.get('/Contents', '')
                        if not content:
                            content = get_contents_from_popup(annot_obj)
                        
                        # Skip empty comments
                        if not content and subtype not in ['/Highlight', '/Underline', '/StrikeOut', '/Squiggly']:
                            continue
                            
                        # Try to get the author (different PDFs might use different keys)
                        author = annot_obj.get('/T', '')
                        if not author:
                            author = annot_obj.get('/TI', '')
                            if not author:
                                author = annot_obj.get('/TU', 'Unknown')
                        
                        # Try to get the date
                        date = annot_obj.get('/M', '')
                        if not date:
                            date = annot_obj.get('/CreationDate', '')
                        
                        # For annotations like highlights that might not have content
                        if not content and subtype in ['/Highlight', '/Underline', '/StrikeOut', '/Squiggly']:
                            content = f"[{subtype.replace('/', '')} annotation]"
                        
                        comments.append({
                            'page': page_num,
                            'index': i,
                            'content': content,
                            'author': author,
                            'date': date,
                            'type': subtype
                        })
                    
                except Exception as e:
                    logger.warning(f"Error processing annotation {i} on page {page_num}: {str(e)}")
        
        if debug_mode:
            logger.info(f"Found annotation types: {annotation_types_found}")
            logger.info(f"Total comments extracted: {len(comments)}")
        
        return sorted(comments, key=lambda x: (x['page'], x['index']))
    
    except Exception as e:
        logger.error(f"Error extracting comments: {str(e)}")
        raise