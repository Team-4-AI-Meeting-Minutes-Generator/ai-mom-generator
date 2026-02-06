import os
import sys

# Import team modules
from preprocess import clean_text
from extract_points import get_key_points
from extract_actions import get_actions
from extract_entities import get_entities
from audio_to_text import convert_audio
from output_formatter import format_output


def read_text_file(file_path):
    """
    Reads transcript text file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        sys.exit(1)


def process_input(file_path):
    """
    Detects file type and returns transcript text
    """
    if not os.path.exists(file_path):
        print("File does not exist.")
        sys.exit(1)

    # If audio file
    if file_path.endswith((".mp3", ".wav", ".m4a")):
        print("🎧 Converting audio to text...")
        return convert_audio(file_path)

    # If text file
    elif file_path.endswith(".txt"):
        print("📄 Reading transcript file...")
        return read_text_file(file_path)

    else:
        print("Unsupported file format.")
        sys.exit(1)


def run_pipeline(file_path):
    """
    Main pipeline execution
    """

    print("\n🚀 Starting AI Meeting Minutes Generator...\n")

    # Step 1: Get raw text
    raw_text = process_input(file_path)

    # Step 2: Clean text
    print("🧹 Cleaning text...")
    cleaned_text = clean_text(raw_text)

    # Step 3: Extract key discussion points
    print("🧠 Extracting key discussion points...")
    key_points = get_key_points(cleaned_text)

    # Step 4: Extract action items
    print("📌 Extracting action items...")
    actions = get_actions(cleaned_text)

    # Step 5: Extract entities (person + deadlines)
    print("👤 Extracting responsible persons & deadlines...")
    entities = get_entities(cleaned_text)

    # Step 6: Format final output
    print("📊 Formatting output...")
    format_output(
        key_points=key_points,
        actions=actions,
        entities=entities
    )

    print("\n✅ Meeting Minutes Generated Successfully!\n")


if __name__ == "__main__":
    # You can change file path here for testing
    input_file = "data/sample_transcript.txt"

    # OR allow user to pass file from terminal:
    # python main.py data/meeting.mp3
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    run_pipeline(input_file)
    