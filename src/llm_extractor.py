import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)

# Configure OpenRouter API
API_KEY = os.getenv("OPENROUTER_API_KEY")
CLIENT = None

if API_KEY:
    try:
        CLIENT = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        # Using gemini-2.0-flash via OpenRouter
        MODEL = "google/gemini-2.0-flash-001"
    except Exception as e:
        logger.error(f"Failed to initialize OpenRouter client: {e}")
        CLIENT = None
else:
    logger.warning("OPENROUTER_API_KEY not found in environment.")

def extract_minutes(transcript_text: str):
    """
    Extracts key points and action items from a transcript using OpenRouter API.
    """
    if not CLIENT:
        logger.warning("OpenRouter client not initialized. Skipping LLM extraction.")
        return None

    prompt = f"""
    You are an expert meeting assistant. Analyze the following meeting transcript and extract:
    1. Key Discussion Points: A list of the most important topics discussed.
    2. Action Items: A list of specific tasks assigned, who they are assigned to (owner), and the deadline (if mentioned).

    Transcript:
    \"\"\"
    {transcript_text}
    \"\"\"

    Respond ONLY in JSON format with the following structure:
    {{
        "key_points": ["point 1", "point 2", ...],
        "action_items": [
            {{
                "action": "task description",
                "owner": "person name or 'Unknown'",
                "deadline": "date or 'N/A'"
            }},
            ...
        ]
    }}
    """

    try:
        logger.info(f"Sending request to OpenRouter API (Model: {MODEL})...")
        response = CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        logger.info("OpenRouter API response received successfully.")
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error during OpenRouter extraction: {e}")
        return None
