from attending import Library
import pytest
from pathlib import Path
import os
import shutil


@pytest.fixture
def ipython():
    yield "ipython", "1.0.0", "https://readthedocs.org/projects/ipython/downloads/pdf/stable/"


@pytest.fixture
def lib_fixture():
    base_path = Path(os.path.dirname(os.path.abspath(__file__))) / "test_dir"
    yield base_path
    if base_path.exists():
        shutil.rmtree(base_path)


def test_library_fetch(ipython, lib_fixture):
    name, version, __doc__url__ = ipython

    # check that library does not have doc
    lib = Library(home=lib_fixture)
    assert not lib.in_collection(name, version)
    with pytest.raises(KeyError):
        lib.get_edition(name, version)

    # get the doc and check that we have it
    lib.fetch(name, version, __doc__url__)
    assert (lib_fixture / ".attending" / name / version).exists()
    assert lib.get_edition(name, version)

    # verifying that getting the doc again is idempotent
    lib.fetch(name, version, __doc__url__)
    assert (lib_fixture / ".attending" / name / version).exists()
    assert lib.get_edition(name, version)


def test_library_retire(ipython, lib_fixture):
    name, version, __doc_url__ = ipython
    lib = Library(home=lib_fixture)

    assert not lib.in_collection(name, version)
    with pytest.raises(KeyError):
        lib.retire(name, version)
    assert not (lib_fixture / ".attending" / name / version).exists()

    lib.fetch(name, version, __doc_url__)

    assert lib.in_collection(name, version)
    assert (lib_fixture / ".attending" / name / version).exists()

    lib.retire(name, version)
    assert not lib.in_collection(name, version)
    assert not (lib_fixture / ".attending" / name / version).exists()



