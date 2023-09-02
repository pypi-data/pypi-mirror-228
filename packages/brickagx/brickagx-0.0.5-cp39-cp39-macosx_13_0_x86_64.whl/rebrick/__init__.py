import os
if "DEBUG_AGXBRICK" in os.environ:
    print(f"#### Using Debug build ####")
    try:
        from .debug.api import *
        from .debug import Core
        from .debug import Math
        from .debug import Physics
        from .debug import Simulation
    except:
        print(f"Failed finding rebrick modules or libraries, did you set PYTHONPATH correctly? Should point to where rebrick directory with binaries are located")
        print(f"Also, make sure you are using the same Python version the libraries were built for.")
        exit(255)
else:
    try:
        from .api import *
        from . import Core
        from . import Math
        from . import Simulation
    except:
        print(f"Failed finding rebrick modules or libraries, did you set PYTHONPATH correctly? Should point to where rebrick directory with binaries are located")
        print(f"Also, make sure you are using the same Python version the libraries were built for.")
        exit(255)
