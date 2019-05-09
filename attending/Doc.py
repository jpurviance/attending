from pathlib import Path
from dataclasses import dataclass
import webbrowser
import shutil


@dataclass
class DocLocation:
    attending_path: Path
    name: str
    version: str

    def full_path(self):
        return self.attending_path / Path(self.name) / Path(self.version)

    def base_path(self):
        return self.attending_path / Path(self.name)

    def __str__(self):
        return self.full_path().as_uri()

    def __repr__(self):
        return str(self)

    def as_module_identifier(self):
        return self.name, self.version

    def clean_up(self):
        shutil.rmtree(self.full_path())


@dataclass
class Doc:
    name: str
    doc_location: DocLocation

    def diagnose(self):
        webbrowser.open(str(self.doc_location))

    def retire(self):
        self.doc_location.clean_up()
