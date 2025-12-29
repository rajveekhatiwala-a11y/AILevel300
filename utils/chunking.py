"""
Text Chunking Utilities
Implements various chunking strategies for RAG
"""
from typing import List, Dict
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextChunker:
    """Chunk documents for vector indexing"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Chunk all documents
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of chunk dictionaries with metadata
        """
        all_chunks = []
        
        for doc_idx, doc in enumerate(documents):
            chunks = self.chunk_text(doc['content'])
            
            for chunk_idx, chunk in enumerate(chunks):
                chunk_data = {
                    'content': chunk,
                    'source': doc['source'],
                    'file_path': doc['file_path'],
                    'file_type': doc['file_type'],
                    'chunk_id': f"{doc['source']}_chunk_{chunk_idx}",
                    'chunk_index': chunk_idx,
                    'total_chunks': len(chunks),
                    'document_index': doc_idx
                }
                all_chunks.append(chunk_data)
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Chunk text using sliding window approach
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        # If text is smaller than chunk size, return as is
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Get the chunk
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings near the chunk boundary
                chunk_text = text[start:end]
                last_period = max(
                    chunk_text.rfind('. '),
                    chunk_text.rfind('.\n'),
                    chunk_text.rfind('! '),
                    chunk_text.rfind('? ')
                )
                
                if last_period > self.chunk_size * 0.5:  # Don't break too early
                    end = start + last_period + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap if end < len(text) else end
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing excessive whitespace
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Replace multiple newlines with double newline
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def chunk_by_section(self, text: str, section_headers: List[str] = None) -> List[Dict[str, str]]:
        """
        Chunk text by sections (headers)
        
        Args:
            text: Text to chunk
            section_headers: List of header patterns (e.g., ['#', '##'])
            
        Returns:
            List of section chunks with metadata
        """
        if section_headers is None:
            section_headers = ['#', '##', '###']
        
        sections = []
        current_section = ""
        current_header = "Introduction"
        
        for line in text.split('\n'):
            # Check if line is a header
            is_header = False
            for header_pattern in section_headers:
                if line.strip().startswith(header_pattern):
                    # Save previous section
                    if current_section.strip():
                        sections.append({
                            'content': current_section.strip(),
                            'header': current_header
                        })
                    
                    # Start new section
                    current_header = line.strip()
                    current_section = ""
                    is_header = True
                    break
            
            if not is_header:
                current_section += line + "\n"
        
        # Add last section
        if current_section.strip():
            sections.append({
                'content': current_section.strip(),
                'header': current_header
            })
        
        return sections
