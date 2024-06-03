import shutil

def check_for_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None