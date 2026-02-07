import os
import sys
import json
import time
import logging

# Import team modules
from preprocess import clean_text
from extract_points import get_key_points
from extract_actions import get_actions
from output_formatter import format_output
from llm_extractor import extract_minutes


# ---------------------------
# Logging Configuration
# ---------------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------
# Read Text File
# ---------------------------
def read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading text file: {e}")
        raise


# ---------------------------
# Process Input File
# ---------------------------
def process_input(file_path, silent=False):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if os.path.isdir(file_path):
        raise ValueError(f"'{file_path}' is a directory, not a file. Please provide a path to a specific file (e.g., .txt or .mp3).")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        logging.info("Reading transcript file...")
        if not silent: print("📄 Reading transcript file...")
        return read_text_file(file_path)

    elif ext == ".json":
        logging.info("Reading JSON transcript file...")
        if not silent: print("📄 Reading JSON transcript file...")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            if "transcript" not in data:
                 raise ValueError("JSON must contain 'transcript' key.")
                 
            # Convert structured transcript to text format
            full_text = []
            for entry in data["transcript"]:
                speaker = entry.get("speaker", "Unknown")
                utterance = entry.get("utterance", "")
                full_text.append(f"{speaker}: {utterance}")
                
            return "\n".join(full_text)
            
        except Exception as e:
             logging.error(f"Error reading JSON file: {e}")
             raise

    elif ext in [".mp3", ".wav", ".m4a", ".mp4", ".mpeg"]:
        logging.info("Detected audio file. Starting transcription...")
        if not silent: print("🎙️  Audio file detected. Starting transcription (this may take a while)...")
        from audio_to_text import audio_to_text
        return audio_to_text(file_path)

    else:
        file_name = os.path.basename(file_path)
        actual_ext = ext if ext else "no extension"
        raise ValueError(f"Unsupported file format: '{actual_ext}' for file '{file_name}'. Supported: .txt, .json, .mp3, .wav, .m4a")


# ---------------------------
# Main Pipeline
# ---------------------------
def run_pipeline(file_path, meeting_id=None, silent=False):

    try:
        start_time = time.time()

        if not silent: print("\n🚀 Starting AI Meeting Minutes Generator...\n")
        logging.info("Pipeline started")

        # Step 1: Get transcript
        raw_text = process_input(file_path, silent=silent)

        # Step 2: Clean transcript
        if not silent: print("🧹 Cleaning text...")
        cleaned_text = clean_text(raw_text)

        # Step 3 & 4: Extract discussion points and action items
        if not silent: print("🤖 Using AI to extract meeting minutes...")
        llm_results = extract_minutes(cleaned_text)

        if llm_results:
            key_points = llm_results.get("key_points", [])
            actions = llm_results.get("action_items", [])
        else:
            if not silent: print("⚠️ falling back to heuristic extraction...")
            # Step 3: Extract discussion points (Fallback)
            if not silent: print("🧠 Extracting key discussion points...")
            key_points = get_key_points(cleaned_text)

            # Step 4: Extract action items (Fallback)
            if not silent: print("📌 Extracting action items...")
            actions = get_actions(cleaned_text)

        # Step 5: Prepare structured output
        structured_output = {
            "meeting_id": meeting_id if meeting_id else "N/A",
            "key_points": key_points,
            "action_items": actions,
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        logging.info(f"Execution time: {execution_time} seconds")

        # Step 6: Print formatted professional output
        if not silent:
            print("\n📊 FORMATTED MEETING MINUTES\n")
            from output_formatter import format_output
            formatted_result = format_output(structured_output)
            print(formatted_result)

            print("✅ Meeting Minutes Generated Successfully!")
            print(f"⏱ Execution Time: {execution_time} seconds\n")

        return structured_output

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        if not silent: print(f"\n❌ Error occurred: {e}\n")
        return None


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":

    print("\n🚀 AI Meeting Minutes Generator")
    print("Type 'exit' or 'quit' to close the application.\n")

    # Check CLI arguments first
    if len(sys.argv) > 1:
        initial_file = sys.argv[1]
        run_pipeline(initial_file)
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n📂 Enter path to transcript/audio file (or 'exit'): ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            if not os.path.exists(user_input):
                print(f"❌ Error: File not found at '{user_input}'")
                continue
                
            run_pipeline(user_input)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break