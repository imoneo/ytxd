import os

__cwd = os.getcwd()

__EXTENSIONS = (".mp4", ".mkv", ".mp3", ".flac", ".wav", ".m4a")


def remove_media_files_and_empty_directories():
    remove_files_with_specified_extansions()
    remove_empty_directories()


def remove_files_with_specified_extansions(extensions=__EXTENSIONS, cwd=__cwd):
    for filename in os.listdir(cwd):
        file_path = os.path.join(cwd, filename)

        if os.path.isfile(file_path) and file_path.endswith(extensions):
            os.remove(file_path)
            print(f"Removed file: {file_path}")
        elif os.path.isdir(file_path):
            remove_files_with_specified_extansions(cwd=file_path)


def remove_empty_directories(cwd=__cwd):
    for dir_name in os.listdir(cwd):
        dir_path = os.path.join(cwd, dir_name)

        if os.path.isdir(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)
            print(f"Removed empty direectory: {dir_path}")
        elif os.path.isdir(dir_path) and os.listdir(dir_path):
            remove_empty_directories(cwd=dir_path)
