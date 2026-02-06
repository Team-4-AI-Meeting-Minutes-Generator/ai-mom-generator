import whisper
import os


def audio_to_text(audio_path, output_path=None):
    """
    Converts audio file to text using Whisper.
    
    Parameters:
        audio_path (str): Path to audio file
        output_path (str): Optional path to save transcript file
    
    Returns:
        str: Full transcript text
    """

    # Load model (base is good balance of speed & accuracy)
    model = whisper.load_model("base")

    # Transcribe audio
    result = model.transcribe(audio_path)

    # Format transcript using segments
    formatted_transcript = ""
    for segment in result["segments"]:
        line = segment["text"].strip()
        formatted_transcript += line + "\n"

    # Save transcript if output path provided
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted_transcript)

    return formatted_transcript


if __name__ == "__main__":
    # Get project root directory
    base_dir = os.path.dirname(os.path.dirname(__file__))

    audio_file = os.path.join(base_dir, "data", "sample_audio.mp3")
    output_file = os.path.join(base_dir, "data", "sample_transcript.txt")

    transcript = audio_to_text(audio_file, output_file)

    print("\n Transcription Completed!\n")
    print("----- Transcript Preview -----\n")
    print(transcript)
