import os
from dotenv import load_dotenv

def config_llm():
    """
    Ensures environment variables are loaded and valid.
    This replaces the 'test' logic with 'setup' logic.
    """
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not openai_key and not anthropic_key:
        print("⚠️ Warning: No API keys found in .env file!")
    else:
        print("✅ Environment variables loaded.")

# If you want to keep your test functionality, keep it simple:
if __name__ == "__main__":
    config_llm()
    print("OpenAI Key Status:", "Set" if os.getenv("OPENAI_API_KEY") else "Missing")
    print("Anthropic Key Status:", "Set" if os.getenv("ANTHROPIC_API_KEY") else "Missing")