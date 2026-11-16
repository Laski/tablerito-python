from pathlib import Path

from flask import send_from_directory
from werkzeug.datastructures import FileStorage


def save(card_id: int, file: FileStorage) -> str:
    name = f"{card_id}-{Path(file.filename).name}"
    target = Path("attachments") / name
    target.parent.mkdir(exist_ok=True)
    file.save(target)
    return name


def download(name: str):
    # send_from_directory doesn't let you leave the folder: a name like ../config.py gives 404.
    # The folder goes absolute because otherwise Flask looks for it inside the package.
    return send_from_directory(Path("attachments").absolute(), name, as_attachment=True)
