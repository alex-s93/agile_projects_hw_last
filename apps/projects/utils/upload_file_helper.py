import os.path
from pathlib import Path

EXTENSIONS = (".pdf", ".csv", ".doc", ".xlsx")
FILE_PATH = "documents"
MAX_SIZE = 2


def validate_file_extension(file_name: str) -> bool:
    file_extension = Path(file_name).suffix
    if file_extension in EXTENSIONS:
        return True
    return False


def validate_file_size(file) -> bool:
    file_size = file.size / (1024**2)
    if file_size > MAX_SIZE:
        return False
    return True


def create_file_path(file_name: str, project_name: str) -> str:
    new_file, file_extension = file_name.split(".")
    file_path = "{}/{}/{}.{}".format(
        FILE_PATH, project_name.replace(' ', '_'),
        new_file.replace(' ', '_'),
        file_extension
    )
    # file_path = os.path.join(FILE_PATH, file_path)
    return file_path


def save_file(file, file_path):
    path = os.path.dirname(Path(file_path))
    os.makedirs(path, exist_ok=True)
    with open(file_path, "wb") as new_file:
        for chunk in file.chunks():
            new_file.write(chunk)
    return file_path

