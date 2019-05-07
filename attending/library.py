from pathlib import Path
import urllib.request
from dataclasses import dataclass


class Library:
    def __init__(self, home=Path().home()):
        self.location = self._construct(home / Path(".attending"))
        self.docs = self._load_docs()
        print(self.docs)

    def fetch(self, module):
        if hasattr(module, "__doc_url__"):
            if module not in self:
                self._add_project(module.__name__, module.__doc_url__)
        else:
            print("this project does not yet have support for attending")

    def _construct(self, home: Path):
        if not home.exists():
            home.mkdir(parents=True)
        return home

    def _add_project(self, name, url):
        location = self.location / Path(name)
        if location.exists():
            raise FileExistsError(f"{name} already exists")
        location.mkdir(parents=True)
        with open(location / Path(name + ".pdf"), "wb") as f:
            with urllib.request.urlopen(url) as doc:
                f.write(doc.read())
        self.docs[name] = Doc(name, location)

    def _load_docs(self):
        docs = {}
        for project in self.location.iterdir():
            if project.is_dir():
                docs[project.stem] = Doc(project.stem, project)
        return docs

    def __contains__(self, item):
        return item.__name__ in self.docs

    def __getitem__(self, item):
        return self.docs[item.__name__]


@dataclass
class Doc:
    name: str
    location: Path
