from attending.library import Library


def get_the_docs(module):
    library = Library()
    if hasattr(module, "__doc_url__"):
        library.add_project(module.__name__, "latest", module.__doc_url__)
    else:
        print("this project does not yet have support for attending")
