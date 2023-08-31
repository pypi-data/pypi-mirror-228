# askquinta/connector/__init__.py

# Package-level variables
VERSION = '0.1'

# Package-level function
def greet():
    print("Welcome to askquinta!")

# Import submodules to make them accessible when users import the package
from .ArangoDB import About_ArangoDB
from .MySQL import About_MySQL
from .API import About_API

