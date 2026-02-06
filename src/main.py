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
def process_input(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist.")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        logging.info("Reading transcript file...")
        print("📄 Reading transcript file...")
        return read_text_file(file_path)

    elif ext in [".mp3", ".wav", ".m4a", ".mp4", ".mpeg"]:
        logging.info("Detected audio file. Starting transcription...")
        print("🎙️  Audio file detected. Starting transcription (this may take a while)...")
        from audio_to_text import audio_to_text
        return audio_to_text(file_path)

    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported: .txt, .mp3, .wav, .m4a")


# ---------------------------
# Main Pipeline
# ---------------------------
def run_pipeline(file_path, meeting_id=None):

    try:
        start_time = time.time()

        print("\n🚀 Starting AI Meeting Minutes Generator...\n")
        logging.info("Pipeline started")

        # Step 1: Get transcript
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

        # Step 5: Prepare structured output
        structured_output = {
            "meeting_id": meeting_id if meeting_id else "N/A",
            "key_points": key_points,
            "action_items": actions,
            "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Step 6: Save JSON output
        if not os.path.exists("output"):
            os.makedirs("output")

        output_file = f"output/meeting_minutes_{int(time.time())}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structured_output, f, indent=4)

        logging.info(f"Output saved to {output_file}")

        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        logging.info(f"Execution time: {execution_time} seconds")

        # Step 7: Print formatted professional output
        print("\n📊 FORMATTED MEETING MINUTES\n")
        formatted_result = format_output(structured_output)
        print(formatted_result)

        print("✅ Meeting Minutes Generated Successfully!")
        print(f"⏱ Execution Time: {execution_time} seconds")
        print(f"📁 JSON saved at: {output_file}\n")

        return structured_output

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"\n❌ Error occurred: {e}\n")
        return None


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":

    input_file = "data/sample_transcript.txt"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    run_pipeline(input_file)