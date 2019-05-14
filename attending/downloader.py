import urllib.request as request
from pathlib import Path

from .mimetypes import get_mapping, get_extractor


def unpack_docs(working_directory: Path, file: Path):
    extractor = get_extractor(''.join(file.suffixes))
    if extractor:
        extractor(working_directory, file)


def write_to_file(base_path, name, version, url):
    with request.urlopen(url) as connection:
        if connection.status == 200:
            file_extension = get_mapping(connection.getheader('Content-Type'))
            target = base_path / name / version / Path(f"{name}.{file_extension}")
            with open(target, "wb") as f:
                f.write(connection.read())
            unpack_docs(base_path / name / version, target)
        elif 300 <= connection.status and connection.status < 400:
            write_to_file(base_path, name, version, connection.getheader("Location"))
        else:
            raise LookupError(f"Failed to fetch docs at {url}, http status: {connection.status}")
