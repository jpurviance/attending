import urllib.request
from pathlib import Path
from zipfile import ZipFile


def extract_zip(directory: Path, file: Path):
    ZipFile(file).extractall(path=directory)
    file.unlink()


def write_to_file(url, directory, name):
    with urllib.request.urlopen(url) as connection:
        if 400 > connection.status >= 300:
            write_to_file(connection.getheader("Location"), directory, name)
        elif connection.status == 200:
            file_extension = _EXTENSION_MAPPING.get(connection.getheader('Content-Type'), 'txt')
            target = directory / Path(f"{name}.{file_extension}")
            with open(target, "wb") as f:
                for bytes in range(0, int(connection.getheader("Content-Length")), 1024):
                    f.write(connection.read(bytes))
            if file_extension in _EXTENSION_POST_DIRECTIVES:
                _EXTENSION_POST_DIRECTIVES[file_extension](directory, target)
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
