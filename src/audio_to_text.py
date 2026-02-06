import whisper
import os
import shutil
import imageio_ffmpeg

# Setup ffmpeg: Ensure it's available in the environment
ffmpeg_exe_path = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe_path)

# 1. Inject into PATH
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]

# 2. Fallback: Copy to CWD if not reachable (common Windows issue with PATH updates in runtime)
local_ffmpeg = os.path.join(os.getcwd(), "ffmpeg.exe")
if not shutil.which("ffmpeg") and not os.path.exists(local_ffmpeg):
    print(f"   ℹ️  ffmpeg not found in PATH, copying from {ffmpeg_exe_path} to {local_ffmpeg}...")
    try:
        shutil.copy(ffmpeg_exe_path, local_ffmpeg)
        os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]
    except Exception as e:
        print(f"   ⚠️ Could not copy ffmpeg: {e}")

print(f"   ℹ️  ffmpeg path configured: {shutil.which('ffmpeg') or 'Not Found'}")


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
    try:
        print("   Loading Whisper model...")
        model = whisper.load_model("base")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        return ""

    # Transcribe audio
    print(f"   Transcribing {os.path.basename(audio_path)}...")
    try:
        result = model.transcribe(audio_path)
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

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
