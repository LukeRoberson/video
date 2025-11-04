"""
WebVTT subtitle file parser for extracting transcript text.

This module provides functionality to parse VTT files and extract
timestamped text chunks for indexing in Elasticsearch.
"""

from typing import List, Dict, Optional
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class VTTParser:
    """
    Parser for WebVTT subtitle files.
    
    Attributes:
        TIMESTAMP_PATTERN: Regex pattern for matching VTT timestamps.
    """
    
    TIMESTAMP_PATTERN = re.compile(
        r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})'
    )
    
    @staticmethod
    def parse_vtt_file(file_path: str) -> Optional[Dict[str, any]]:
        """
        Parse a VTT file and extract transcript chunks with timestamps.
        
        Parameters:
            file_path (str): Path to the VTT file.
        
        Returns:
            Optional[Dict[str, any]]: Dictionary containing full transcript
                and timestamped chunks, or None if parsing fails.
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"VTT file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove VTT header
            if content.startswith('WEBVTT'):
                content = content.split('\n', 1)[1] if '\n' in content else ''
            
            # Split into blocks
            blocks = content.split('\n\n')
            chunks: List[Dict[str, str]] = []
            full_transcript: List[str] = []
            
            for block in blocks:
                block = block.strip()
                if not block:
                    continue
                
                lines = block.split('\n')
                
                # Find timestamp line
                timestamp_line = None
                text_lines = []
                
                for line in lines:
                    if VTTParser.TIMESTAMP_PATTERN.match(line):
                        timestamp_line = line
                    elif line and not line.isdigit():
                        # Skip cue identifiers (numeric lines)
                        text_lines.append(line)
                
                if timestamp_line and text_lines:
                    text = ' '.join(text_lines)
                    # Remove VTT formatting tags
                    text = re.sub(r'<[^>]+>', '', text)
                    text = text.strip()
                    
                    if text:
                        chunks.append({
                            'timestamp': timestamp_line.split('-->')[0].strip(),
                            'text': text
                        })
                        full_transcript.append(text)
            
            if not chunks:
                logger.warning(f"No content extracted from VTT file: {file_path}")
                return None
            
            return {
                'transcript': ' '.join(full_transcript),
                'transcript_chunks': chunks
            }
            
        except Exception as e:
            logger.error(f"Error parsing VTT file {file_path}: {e}")
            return None
    
    @staticmethod
    def get_vtt_path_for_video(video_id: int, vtt_directory: str) -> str:
        """
        Construct the VTT file path for a given video ID.
        
        Parameters:
            video_id (int): The video database ID.
            vtt_directory (str): Base directory containing VTT files.
        
        Returns:
            str: Full path to the VTT file.
        """
        return str(Path(vtt_directory) / f"{video_id}.vtt")