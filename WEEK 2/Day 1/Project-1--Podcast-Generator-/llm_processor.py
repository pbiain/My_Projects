"""
LLM Processor Module
Handles integration with Language Model APIs (OpenAI, etc.)
"""

import os
from typing import Optional, List
import json
from dotenv import load_dotenv


class LLMProcessor:
    """Process content through LLM APIs"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize LLM Processor
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4o-mini)
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate_podcast_script(self, content: str, style: str = "conversational") -> str:
        """
        Generate a podcast script from content
        
        Args:
            content: Source content to convert to podcast script
            style: Podcast style (conversational, educational, interview, etc.)
            
        Returns:
            Generated podcast script
        """
        prompt = f"""
You are a professional podcast scriptwriter. Convert the following content into an engaging 
podcast script with a {style} style. Include:
- Introduction hook
- Main content points (clearly structured)
- Transitions between segments
- Conclusion/call-to-action

Content to convert:
{content}

Generate the podcast script now:
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def generate_episode_outline(self, content: str, num_segments: int = 5) -> List[dict]:
        """
        Generate episode outline with segments
        
        Args:
            content: Source content
            num_segments: Number of segments to create
            
        Returns:
            List of episode segments with timing
        """
        prompt = f"""
Create a {num_segments}-segment podcast episode outline from this content.
For each segment, provide:
- Title
- Duration (in minutes)
- Key points
- Talking points

Content:
{content}

Format as JSON array.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return [{"segment": response.choices[0].message.content}]
    
    def refine_script(self, script: str, feedback: str) -> str:
        """
        Refine an existing script based on feedback
        
        Args:
            script: Original script
            feedback: Feedback for improvement
            
        Returns:
            Refined script
        """
        prompt = f"""
Please refine this podcast script based on the feedback provided.

Original Script:
{script}

Feedback:
{feedback}

Generate the refined script:
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def extract_key_points(self, content: str) -> List[str]:
        """
        Extract key points from content
        
        Args:
            content: Source content
            
        Returns:
            List of key points
        """
        prompt = f"""
Extract the 5-7 most important key points from this content in a concise format.
Return as a JSON array of strings.

Content:
{content}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return response.choices[0].message.content.split('\n')


if __name__ == "__main__":
    llm = LLMProcessor()
    print("LLM Processor initialized")
