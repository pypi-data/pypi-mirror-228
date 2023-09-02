import os
import sys
__all__ = ["camera", "light_source", "LibreDR", "Geometry"]
# All camera models (python)
from . import camera
# All light source models (python)
from . import light_source
# LibreDR client (rust)
from .libredr import __author__, __version__, LibreDR, Geometry
# PyTorch bindings (python)
try:
  import torch
except ModuleNotFoundError:
  if "LIBREDR_LOG_LEVEL" in os.environ and os.environ["LIBREDR_LOG_LEVEL"] in ("info", "debug"):
    print("PyTorch not found, disabled PyTorch bindings.")
if "torch" in sys.modules:
  from . import torch
  __all__.append("torch")
