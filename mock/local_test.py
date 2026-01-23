from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("argenta")
except PackageNotFoundError:
    __version__ = "unknown"

print("__version__ = {}".format(__version__))