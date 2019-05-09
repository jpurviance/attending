from pathlib import Path

from .downloader import write_to_file
from .Doc import DocLocation, Doc


def _module_identifier(module):
    return module.__name__, module.__version__


class Library:
    def __init__(self, home=Path().home()):
        self.location = self._construct(home / Path(".attending"))
        self.docs = self._load_docs()
        print(self.docs)

    def fetch(self, module):
        if not hasattr(module, "__doc_url__"):
            raise AttributeError(f"{module.__name__} missing '__doc_url__'")
        if not hasattr(module, "__version__"):
            raise AttributeError(f"{module.__name__} missing '__version__'")
        if module not in self:
            doc_location = DocLocation(self.location, module.__name__, module.__version__)
            self._add_project(doc_location, module.__doc_url__)

    def _construct(self, home: Path):
        if not home.exists():
            home.mkdir(parents=True)
        return home

    def _add_project(self, doc_location: DocLocation, url):
        if doc_location.full_path().exists():
            raise FileExistsError(f"{doc_location.full_path()}")
        doc_location.full_path().mkdir(parents=True)
        write_to_file(url, doc_location)
        self.docs[doc_location.as_module_identifier()] = Doc(doc_location.name, doc_location)

    def _load_docs(self):
        docs = {}
        for project in self.location.iterdir():
            if project.is_dir():
                for version in project.iterdir():
                    if version.is_dir():
                        docs[(project.stem, version.name)] = \
                            Doc(project.stem, DocLocation(self.location, project.stem, version.name))
        return docs

    def __contains__(self, module):
        return _module_identifier(module) in self.docs

    def __getitem__(self, module):
        return self.docs[_module_identifier(module)]
