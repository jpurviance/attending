from pathlib import Path
from dataclasses import dataclass
import webbrowser


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
        return str(self.full_path())

    def __repr__(self):
        return str(self)

    def as_module_identifier(self):
        return self.name, self.version


@dataclass
class Doc:
    name: str
    doc_location: DocLocation

    def diagnose(self):
        webbrowser.open(f"file://{self.doc_location}")
