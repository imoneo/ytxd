import subprocess


def check() -> bool:
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        print("FFmpeg is installed, but there was an error running it.")
        return False
    except FileNotFoundError:
        print("FFmpeg is not installed.")
        print("Please install FFmpeg")
        print("Download and install from official website: https://www.ffmpeg.org/")
        return False
    except Exception as e:
        print(f"An error occured: {e}")
        return False
