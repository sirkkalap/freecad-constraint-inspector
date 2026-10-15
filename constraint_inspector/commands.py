# SPDX-License-Identifier: LGPL-2.1-or-later

"""FreeCAD command registration; import does not open the panel."""
import FreeCADGui as Gui


class ShowInspector:
    def GetResources(self):
        return {'MenuText': 'Rajoitteiden sidonnat',
                'ToolTip': 'Näytä luonnoksen rajoitteiden kaikki suorat viittaukset'}

    def IsActive(self):
        return True

    def Activated(self):
        from constraint_inspector.panel import show_panel
        show_panel()


def register():
    Gui.addCommand('ConstraintInspector_Show', ShowInspector())
