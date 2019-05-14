from pathlib import Path
from zipfile import ZipFile


def extract_zip(doc_location: Path, file: Path):
    ZipFile(file).extractall(path=doc_location)
    file.unlink()


def get_mapping(mime_type):
    return {
        "application/pdf": "pdf",
        "application/zip": "zip",
        "text/html": "html",
        "text/plain": "txt"
    }.get(mime_type, "txt")


def get_extractor(file_extension):
    post_directives = {
        ".zip": extract_zip
    }
    if file_extension in post_directives:
        return post_directives[file_extension]
