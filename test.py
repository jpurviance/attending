import foobar
import fizbuz
import versionless
import latest

from attending import Library

library = Library()

for patient in [foobar, fizbuz, versionless, latest]:
    print(f"{patient.__name__} managed by attending? {patient in library}")
    print(f"{patient.__name__} foobar's docs")
    library.fetch(patient)
    print(f"{patient.__name__} managed by attending? {patient in library}")
