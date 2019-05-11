import urllib.request as request
from pathlib import Path
from zipfile import ZipFile


def extract_zip(doc_location: Path, file: Path):
    ZipFile(file).extractall(path=doc_location)
    file.unlink()


def write_to_file(base_path, name, version, url):
    with request.urlopen(url) as connection:
        if connection.status == 200:
            file_extension = _EXTENSION_MAPPING.get(connection.getheader('Content-Type'), 'txt')
            target = base_path / name / version / Path(f"{name}.{file_extension}")
            with open(target, "wb") as f:
                f.write(connection.read())
            if file_extension in _EXTENSION_POST_DIRECTIVES:
                _EXTENSION_POST_DIRECTIVES[file_extension](base_path / name / version, target)
        elif 300 <= connection.status and connection.status < 400:
            write_to_file(base_path, name, version, connection.getheader("Location"))
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
