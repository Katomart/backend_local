import shutil

def check_for_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None

def check_geckodriver() -> bool:
    return shutil.which("geckodriver") is not None
