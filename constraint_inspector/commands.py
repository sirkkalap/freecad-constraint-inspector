# SPDX-License-Identifier: LGPL-2.1-or-later

"""FreeCAD command registration; import does not open the panel."""
import FreeCADGui as Gui
from pathlib import Path
from .i18n import tr

ICON_PATH = str(Path(__file__).resolve().parents[1] /
                'resources' / 'icons' / 'constraint-inspector.svg')


class ShowInspector:
    def GetResources(self):
        return {'Pixmap': ICON_PATH,
                'MenuText': tr('Constraint bindings'),
                'ToolTip': tr('Show all explicit sketch constraint references')}

    def IsActive(self):
        return True

    def Activated(self):
        from constraint_inspector.panel import show_panel
        show_panel()


def register():
    Gui.addCommand('ConstraintInspector_Show', ShowInspector())
