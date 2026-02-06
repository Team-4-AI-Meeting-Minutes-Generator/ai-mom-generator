import os
import sys
import subprocess
import shutil
import imageio_ffmpeg

print(f"Python: {sys.executable}")
print(f"CWD: {os.getcwd()}")

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print(f"imageio_ffmpeg path: {ffmpeg_exe}")

if not os.path.exists(ffmpeg_exe):
    print("❌ Error: imageio_ffmpeg binary does not exist at path.")
else:
    print("✅ imageio_ffmpeg binary exists.")

# Inject into PATH
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] += os.pathsep + ffmpeg_dir
print(f"Injected into PATH: {ffmpeg_dir}")

# Check shutil.which
which_ffmpeg = shutil.which("ffmpeg")
print(f"shutil.which('ffmpeg'): {which_ffmpeg}")

# Check subprocess execution
print("Attempting to run 'ffmpeg -version'...")
try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ ffmpeg execution successful!")
        print(result.stdout.splitlines()[0])
    else:
        print(f"❌ ffmpeg execution failed with code {result.returncode}")
        print(result.stderr)
except Exception as e:
    print(f"❌ Exception running ffmpeg: {e}")
