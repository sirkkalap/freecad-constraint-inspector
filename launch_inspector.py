# SPDX-License-Identifier: LGPL-2.1-or-later

"""Launch inside FreeCAD using runpy.run_path(), including through a symlink."""
from pathlib import Path
import sys

project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from constraint_inspector.panel import show_panel

inspector = show_panel()
