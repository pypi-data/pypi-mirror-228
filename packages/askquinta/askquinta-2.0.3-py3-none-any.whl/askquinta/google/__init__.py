# askquinta/google/__init__.py

# Package-level variables
VERSION = '0.2'

# Package-level function
def greet():
    print("Welcome to askquinta!")

# Import submodules to make them accessible when users import the package
from .Gsheet import About_Gsheet
from .BQ import About_BQ
