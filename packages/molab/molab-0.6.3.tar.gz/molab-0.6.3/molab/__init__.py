### molab is a python package for setting up and configuring Morpheus training labs ###

# Original Imports
from .deploy import *
from .destroy import *
from .configure import *
from .courses import *

# v6.0 Imports
from .tools.mo import *
from .labs.labs import newLab, existingLab