from pathlib import Path
import urllib.request


class Library:
    def __init__(self):
        self._construct(home=Path().home() / Path(".attending"))

    def _construct(self, home: Path):
        if not home.exists():
            home.mkdir(parents=True)
        self.location = home

    def add_project(self, name, version, url):
        location = self.location / Path(name) / Path(version)
        if location.exists():
            raise FileExistsError(f"{name}/{version} already exists")
        location.mkdir(parents=True)
        with open(location / Path(name + ".pdf"), "wb") as f:
            with urllib.request.urlopen(url) as doc:
                f.write(doc.read())