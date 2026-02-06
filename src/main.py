import os
import sys
import json
import time
import logging

# Import team modules
from preprocess import clean_text
from extract_points import get_key_points
from extract_actions import get_actions
from extract_entities import get_entities
from audio_to_text import convert_audio
from output_formatter import format_output


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
    """
    Reads transcript text file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading text file: {e}")
        raise


# ---------------------------
# Process Input File
# ---------------------------
def process_input(file_path):
    """
    Detects file type and returns transcript text
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist.")

    # Audio file handling
    if file_path.lower().endswith((".mp3", ".wav", ".m4a")):
        logging.info("Converting audio to text...")
        print("🎧 Converting audio to text...")
        return convert_audio(file_path)

    # Text file handling
    elif file_path.lower().endswith(".txt"):
        logging.info("Reading transcript file...")
        print("📄 Reading transcript file...")
        return read_text_file(file_path)

    else:
        raise ValueError("Unsupported file format. Use .txt, .mp3, .wav, .m4a")


# ---------------------------
# Main Pipeline
# ---------------------------
def run_pipeline(file_path, meeting_id=None):
    """
    Executes complete AI Meeting Minutes pipeline
    """

    try:
        start_time = time.time()

        print("\n🚀 Starting AI Meeting Minutes Generator...\n")
        logging.info("Pipeline started")

        # Step 1: Get raw transcript
        raw_text = process_input(file_path)

        # Step 2: Clean transcript
        print("🧹 Cleaning text...")
        cleaned_text = clean_text(raw_text)

        # Step 3: Extract discussion points
        print("🧠 Extracting key discussion points...")
        key_points = get_key_points(cleaned_text)

        # Step 4: Extract action items
        print("📌 Extracting action items...")
        actions = get_actions(cleaned_text)

        # Step 5: Extract responsible persons & deadlines
        print("👤 Extracting responsible persons & deadlines...")
        entities = get_entities(cleaned_text)

        # Step 6: Structure final output
        print("📊 Formatting output...")
        structured_output = {
            "meeting_id": meeting_id if meeting_id else "N/A",
            "discussion_points": key_points,
            "action_items": actions,
            "entities": entities,
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save JSON Output
        if not os.path.exists("output"):
            os.makedirs("output")

        output_file = f"output/meeting_minutes_{int(time.time())}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structured_output, f, indent=4)

        logging.info(f"Output saved to {output_file}")

        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        logging.info(f"Execution time: {execution_time} seconds")

        print("\n✅ Meeting Minutes Generated Successfully!")
        print(f"⏱ Execution Time: {execution_time} seconds")
        print(f"📁 Output saved at: {output_file}\n")

        return structured_output

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"\n❌ Error occurred: {e}\n")
        return None


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":

    # Default file path
    input_file = "data/sample_transcript.txt"

    # Allow file input from terminal
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    result = run_pipeline(input_file)

    if result:
        print("📌 Final Structured Output:")
        print(json.dumps(result, indent=4))