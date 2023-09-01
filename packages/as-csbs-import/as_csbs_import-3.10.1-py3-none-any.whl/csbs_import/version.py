import importlib.metadata

def version() -> str:
    return importlib.metadata.version("as-csbs-import")
