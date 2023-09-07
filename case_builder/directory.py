from .case import *
from .uco import *

submodules = [v for k, v in globals().items() if k[:2] != "__"]

directory = dict()
for submodule in submodules:
    directory |= submodule.directory
