"""
Document Loading and Processing Module
Supports multiple document formats: PDF, DOCX, TXT, MD
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Document parsing libraries
from pypdf import PdfReader
from docx import Document
import chardet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentLoader:
    """Load and parse various document formats"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.md', '.docx'}
    
    def __init__(self, document_path: str):
        """
        Initialize document loader
        
        Args:
            document_path: Path to documents directory
        """
        self.document_path = Path(document_path)
        
        if not self.document_path.exists():
            raise FileNotFoundError(f"Document path not found: {document_path}")
    
    def load_all_documents(self) -> List[Dict[str, str]]:
        """
        Load all supported documents from the directory
        
        Returns:
            List of document dictionaries with content and metadata
        """
        documents = []
        
        for file_path in self.document_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    doc_data = self.load_single_document(file_path)
                    if doc_data:
                        documents.append(doc_data)
                        logger.info(f"Loaded: {file_path.name}")
                except Exception as e:
                    logger.error(f"Error loading {file_path.name}: {str(e)}")
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    def load_single_document(self, file_path: Path) -> Optional[Dict[str, str]]:
        """
        Load a single document based on its extension
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dictionary with content and metadata
        """
        extension = file_path.suffix.lower()
        
        loaders = {
            '.pdf': self._load_pdf,
            '.txt': self._load_text,
            '.md': self._load_text,
            '.docx': self._load_docx
        }
        
        loader_func = loaders.get(extension)
        if not loader_func:
            return None
        
        content = loader_func(file_path)
        
        if content:
            return {
                'content': content,
                'source': str(file_path.name),
                'file_path': str(file_path),
                'file_type': extension[1:],  # Remove the dot
                'file_size': file_path.stat().st_size
            }
        
        return None
    
    def _load_pdf(self, file_path: Path) -> str:
        """Load PDF document"""
        try:
            reader = PdfReader(str(file_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading PDF {file_path.name}: {str(e)}")
            return ""
    
    def _load_text(self, file_path: Path) -> str:
        """Load text or markdown file"""
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] or 'utf-8'
            
            # Read with detected encoding
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error reading text file {file_path.name}: {str(e)}")
            return ""
    
    def _load_docx(self, file_path: Path) -> str:
        """Load Word document"""
        try:
            doc = Document(str(file_path))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading DOCX {file_path.name}: {str(e)}")
            return ""
    
    def get_document_stats(self, documents: List[Dict[str, str]]) -> Dict:
        """
        Get statistics about loaded documents
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Statistics dictionary
        """
        total_chars = sum(len(doc['content']) for doc in documents)
        file_types = {}
        
        for doc in documents:
            file_type = doc['file_type']
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        return {
            'total_documents': len(documents),
            'total_characters': total_chars,
            'file_types': file_types,
            'average_chars_per_doc': total_chars // len(documents) if documents else 0
        }
