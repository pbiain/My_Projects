"""
Text-to-Speech Generator Module
Converts podcast scripts to audio using TTS APIs
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


class TTSGenerator:
    """Generate audio from text using TTS APIs"""
    
    def __init__(self, api_key: Optional[str] = None, voice: str = "nova", speed: float = 1.0):
        """
        Initialize TTS Generator
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            voice: Voice to use (nova, shimmer, echo, etc.)
            speed: Speech speed (0.25 to 4.0)
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.voice = voice
        self.speed = speed
        self.client = None
        self._initialize_client()
        self.output_dir = Path("audio_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate_audio(self, text: str, output_file: Optional[str] = None) -> str:
        """
        Generate audio from text
        
        Args:
            text: Text to convert to speech
            output_file: Optional custom output filename
            
        Returns:
            Path to generated audio file
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("Text content cannot be empty")
        
        if len(text) > 4096:
            raise ValueError("Text exceeds maximum length (4096 characters). Use generate_audio_chunks() for longer content.")
        
        # Generate audio
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text,
            speed=self.speed
        )
        
        # Save audio file
        if output_file is None:
            output_file = f"podcast_{len(text)[:8]}.mp3"
        
        file_path = self.output_dir / output_file
        response.stream_to_file(str(file_path))
        
        return str(file_path)
    
    def generate_audio_chunks(self, text: str, chunk_size: int = 4000, output_prefix: str = "podcast") -> list:
        """
        Generate audio from long text by splitting into chunks
        
        Args:
            text: Long text to convert
            chunk_size: Maximum characters per chunk
            output_prefix: Prefix for output files
            
        Returns:
            List of generated audio file paths
        """
        chunks = self._split_text(text, chunk_size)
        audio_files = []
        
        for i, chunk in enumerate(chunks):
            output_file = f"{output_prefix}_part_{i+1:03d}.mp3"
            file_path = self.generate_audio(chunk, output_file)
            audio_files.append(file_path)
        
        return audio_files
    
    def _split_text(self, text: str, chunk_size: int) -> list:
        """
        Split text into chunks at sentence boundaries
        
        Args:
            text: Text to split
            chunk_size: Maximum chunk size
            
        Returns:
            List of text chunks
        """
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            test_chunk = current_chunk + sentence + ". "
            if len(test_chunk) <= chunk_size:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def change_voice(self, voice: str):
        """
        Change the voice for subsequent generations
        
        Args:
            voice: Voice name (nova, shimmer, echo, etc.)
        """
        valid_voices = ["nova", "shimmer", "echo", "alloy", "onyx", "fable"]
        if voice not in valid_voices:
            raise ValueError(f"Invalid voice. Must be one of: {valid_voices}")
        self.voice = voice
    
    def change_speed(self, speed: float):
        """
        Change the speech speed
        
        Args:
            speed: Speed multiplier (0.25 to 4.0)
        """
        if not (0.25 <= speed <= 4.0):
            raise ValueError("Speed must be between 0.25 and 4.0")
        self.speed = speed
    
    def merge_audio_files(self, audio_files: list, output_file: str = "final_podcast.mp3") -> str:
        """
        Merge multiple audio files into one (requires ffmpeg)
        
        Args:
            audio_files: List of audio file paths
            output_file: Name of merged output file
            
        Returns:
            Path to merged audio file
        """
        try:
            import subprocess
        except ImportError:
            raise ImportError("subprocess module required for audio merging")
        
        # Create concat file for ffmpeg
        concat_file = self.output_dir / "concat.txt"
        with open(concat_file, 'w') as f:
            for audio_file in audio_files:
                f.write(f"file '{audio_file}'\n")
        
        # Merge using ffmpeg
        output_path = self.output_dir / output_file
        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', str(concat_file),
               '-c', 'copy', str(output_path)]
        
        subprocess.run(cmd, check=True)
        
        # Clean up concat file
        concat_file.unlink()
        
        return str(output_path)


if __name__ == "__main__":
    tts = TTSGenerator()
    print("TTS Generator initialized")
