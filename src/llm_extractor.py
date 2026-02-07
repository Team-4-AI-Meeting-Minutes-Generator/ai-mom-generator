import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and API_KEY != "your_api_key_here":
    genai.configure(api_key=API_KEY)
    # Using gemini-2.0-flash as identified in the available models list.
    MODEL = genai.GenerativeModel('gemini-2.0-flash')
else:
    MODEL = None

def extract_minutes(transcript_text: str):
    """
    Extracts key points and action items from a transcript using Gemini API.
    """
    if not MODEL:
        logger.warning("Gemini model not initialized. Skipping LLM extraction.")
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
        logger.info("Sending request to Gemini API...")
        response = MODEL.generate_content(prompt)
        # Extract JSON from response (Gemini might wrap it in markdown blocks)
        content = response.text.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        
        logger.info("Gemini API response received successfully.")
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error during Gemini extraction: {e}")
        return None
