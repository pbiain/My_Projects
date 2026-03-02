"""
Data Processor Module
Handles input from various sources (files, URLs, text, etc.)
"""

import os
from pathlib import Path
from typing import Union, List
import json


class DataProcessor:
    """Process input data from various sources"""
    
    def __init__(self):
        self.supported_formats = ['.txt', '.pdf', '.md', '.json']
        self.max_file_size = 100 * 1024 * 1024  # 100MB
    
    def process_file(self, file_path: str) -> str:
        """
        Process input file and extract text content
        
        Args:
            file_path: Path to the input file
            
        Returns:
            Extracted text content
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.stat().st_size > self.max_file_size:
            raise ValueError(f"File exceeds maximum size of {self.max_file_size} bytes")
        
        # Handle different file types
        if path.suffix == '.txt':
            return self._read_text_file(file_path)
        elif path.suffix == '.json':
            return self._read_json_file(file_path)
        elif path.suffix == '.md':
            return self._read_markdown_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    def process_text(self, text: str) -> str:
        """
        Process raw text input
        
        Args:
            text: Raw text content
            
        Returns:
            Processed text
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        # Clean up text
        text = text.strip()
        return text
    
    def _read_text_file(self, file_path: str) -> str:
        """Read plain text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _read_json_file(self, file_path: str) -> str:
        """Read JSON file and extract text content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'content' in data:
                return str(data['content'])
            return json.dumps(data, indent=2)
    
    def _read_markdown_file(self, file_path: str) -> str:
        """Read markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def validate_content_length(self, content: str, min_length: int = 10, max_length: int = 1000000) -> bool:
        """
        Validate content length
        
        Args:
            content: Content to validate
            min_length: Minimum character count
            max_length: Maximum character count
            
        Returns:
            True if content is valid
        """
        if len(content) < min_length:
            raise ValueError(f"Content too short (minimum {min_length} characters)")
        if len(content) > max_length:
            raise ValueError(f"Content too long (maximum {max_length} characters)")
        return True


if __name__ == "__main__":
    processor = DataProcessor()
    print("Data Processor initialized")
