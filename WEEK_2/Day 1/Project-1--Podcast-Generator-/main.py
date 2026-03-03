"""
Podcast Studio Main Application
FastAPI/Gradio interface for podcast generation
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_processor import DataProcessor
from llm_processor import LLMProcessor
from tts_generator import TTSGenerator


class PodcastStudio:
    """Main Podcast Studio application"""
    
    def __init__(self):
        """Initialize Podcast Studio with all modules"""
        self.data_processor = DataProcessor()
        self.llm_processor = LLMProcessor()
        self.tts_generator = TTSGenerator()
    
    def create_podcast_from_file(self, file_path: str, style: str = "conversational", voice: str = "nova") -> dict:
        """
        Create a complete podcast from a source file
        
        Args:
            file_path: Path to source file
            style: Podcast style
            voice: TTS voice to use
            
        Returns:
            Dictionary with podcast metadata and output files
        """
        result = {
            "status": "processing",
            "steps": []
        }
        
        try:
            # Step 1: Process input file
            result["steps"].append("Processing input file...")
            content = self.data_processor.process_file(file_path)
            result["content_length"] = len(content)
            
            # Step 2: Validate content
            result["steps"].append("Validating content...")
            self.data_processor.validate_content_length(content)
            
            # Step 3: Generate podcast script
            result["steps"].append("Generating podcast script...")
            script = self.llm_processor.generate_podcast_script(content, style)
            result["script"] = script
            
            # Step 4: Extract key points
            result["steps"].append("Extracting key points...")
            key_points = self.llm_processor.extract_key_points(content)
            result["key_points"] = key_points
            
            # Step 5: Generate audio
            result["steps"].append("Generating audio...")
            self.tts_generator.change_voice(voice)
            audio_files = self.tts_generator.generate_audio_chunks(script)
            result["audio_files"] = audio_files
            
            # Step 6: Merge audio (optional)
            if len(audio_files) > 1:
                result["steps"].append("Merging audio files...")
                merged_audio = self.tts_generator.merge_audio_files(
                    audio_files,
                    f"podcast_{Path(file_path).stem}.mp3"
                )
                result["merged_audio"] = merged_audio
            
            result["status"] = "completed"
            result["steps"].append("Podcast generation complete!")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def create_podcast_from_text(self, text: str, style: str = "conversational", voice: str = "nova") -> dict:
        """
        Create a complete podcast from raw text
        
        Args:
            text: Raw text content
            style: Podcast style
            voice: TTS voice to use
            
        Returns:
            Dictionary with podcast metadata and output files
        """
        result = {
            "status": "processing",
            "steps": []
        }
        
        try:
            # Step 1: Process text
            result["steps"].append("Processing text...")
            content = self.data_processor.process_text(text)
            result["content_length"] = len(content)
            
            # Step 2: Validate content
            result["steps"].append("Validating content...")
            self.data_processor.validate_content_length(content)
            
            # Step 3: Generate podcast script
            result["steps"].append("Generating podcast script...")
            script = self.llm_processor.generate_podcast_script(content, style)
            result["script"] = script
            
            # Step 4: Extract key points
            result["steps"].append("Extracting key points...")
            key_points = self.llm_processor.extract_key_points(content)
            result["key_points"] = key_points
            
            # Step 5: Generate audio
            result["steps"].append("Generating audio...")
            self.tts_generator.change_voice(voice)
            audio_files = self.tts_generator.generate_audio_chunks(script)
            result["audio_files"] = audio_files
            
            # Step 6: Merge audio
            if len(audio_files) > 1:
                result["steps"].append("Merging audio files...")
                merged_audio = self.tts_generator.merge_audio_files(
                    audio_files,
                    "podcast_from_text.mp3"
                )
                result["merged_audio"] = merged_audio
            
            result["status"] = "completed"
            result["steps"].append("Podcast generation complete!")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result


def create_gradio_interface():
    """Create Gradio interface for the application"""
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Install with: pip install gradio")
        return None
    
    studio = PodcastStudio()
    
    with gr.Blocks(title="Podcast Studio") as demo:
        gr.Markdown("# Podcast Studio")
        gr.Markdown("Convert your content into professional podcasts with AI")
        
        with gr.Tabs():
            # Tab 1: From File
            with gr.TabItem("From File"):
                file_input = gr.File(label="Upload File (.txt, .md, .json)", type="filepath")
                style_dropdown = gr.Dropdown(
                    choices=["conversational", "educational", "interview", "storytelling"],
                    value="conversational",
                    label="Podcast Style"
                )
                voice_dropdown = gr.Dropdown(
                    choices=["nova", "shimmer", "echo", "alloy", "onyx", "fable"],
                    value="nova",
                    label="Voice"
                )
                submit_btn = gr.Button("Generate Podcast")
                output_text = gr.Textbox(label="Generation Status", lines=10)
                
                def process_file(file_obj, style, voice):
                    if file_obj is None:
                        return "Please upload a file"
                    result = studio.create_podcast_from_file(file_obj.name, style, voice)
                    return str(result)
                
                submit_btn.click(
                    fn=process_file,
                    inputs=[file_input, style_dropdown, voice_dropdown],
                    outputs=output_text
                )
            
            # Tab 2: From Text
            with gr.TabItem("From Text"):
                text_input = gr.Textbox(
                    label="Paste your content here",
                    lines=15,
                    placeholder="Enter the content you want to convert to a podcast..."
                )
                style_dropdown2 = gr.Dropdown(
                    choices=["conversational", "educational", "interview", "storytelling"],
                    value="conversational",
                    label="Podcast Style"
                )
                voice_dropdown2 = gr.Dropdown(
                    choices=["nova", "shimmer", "echo", "alloy", "onyx", "fable"],
                    value="nova",
                    label="Voice"
                )
                submit_btn2 = gr.Button("Generate Podcast")
                output_text2 = gr.Textbox(label="Generation Status", lines=10)
                
                def process_text(text, style, voice):
                    if not text:
                        return "Please enter some text"
                    result = studio.create_podcast_from_text(text, style, voice)
                    return str(result)
                
                submit_btn2.click(
                    fn=process_text,
                    inputs=[text_input, style_dropdown2, voice_dropdown2],
                    outputs=output_text2
                )
    
    return demo


if __name__ == "__main__":
    # Start Gradio interface
    demo = create_gradio_interface()
    if demo:
        demo.launch(share=True)
    else:
        print("Could not start Gradio interface. Install gradio or use the Python API directly.")
