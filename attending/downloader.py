import urllib.request as request
from pathlib import Path
from zipfile import ZipFile

from .Doc import DocLocation


def extract_zip(doc_location: DocLocation, file: Path):
    ZipFile(file).extractall(path=doc_location.full_path())
    file.unlink()


def write_to_file(url, doc_location: DocLocation):
    with request.urlopen(url) as connection:
        if connection.status == 200:
            file_extension = _EXTENSION_MAPPING.get(connection.getheader('Content-Type'), 'txt')
            target = doc_location.full_path() / Path(f"{doc_location.name}.{file_extension}")
            with open(target, "wb") as f:
                for bytes in range(0, int(connection.getheader("Content-Length")), 1024):
                    f.write(connection.read(bytes))
            if file_extension in _EXTENSION_POST_DIRECTIVES:
                _EXTENSION_POST_DIRECTIVES[file_extension](doc_location, target)
        elif 300 <= connection.status and connection.status < 400:
            write_to_file(connection.getheader("Location"), doc_location)
        else:
            raise LookupError(f"Failed to fetch docs at {url}, http status: {connection.status}")


_EXTENSION_MAPPING = {
    "application/pdf": "pdf",
    "application/zip": "zip",
    "text/html": "html",
    "text/plain": "txt"
}

_EXTENSION_POST_DIRECTIVES = {
    "zip": extract_zip
}
