import foobar
import fizbuz

from attending import Library

library = Library()
print(foobar in library)
library.fetch(foobar)
print(foobar in library)
print(library[foobar])

print(fizbuz in library)
library.fetch(fizbuz)
print(fizbuz in library)
print(library[fizbuz])
library[fizbuz].diagnose()
