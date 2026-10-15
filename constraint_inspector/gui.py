# SPDX-License-Identifier: LGPL-2.1-or-later

"""FreeCAD discovers this entry point in its user Mod directory."""
import FreeCADGui as Gui
from .commands import ICON_PATH, register
from .toolbar import install


class ConstraintInspectorWorkbench(Gui.Workbench):
    Icon = ICON_PATH
    MenuText = 'Constraint Inspector'
    ToolTip = 'Inspect Sketcher constraint bindings, including origin and axes'

    def Initialize(self):
        self.appendMenu('Constraint Inspector', ['ConstraintInspector_Show'])
        self.appendToolbar('Constraint Inspector', ['ConstraintInspector_Show'])

    def GetClassName(self):
        return 'Gui::PythonWorkbench'


def initialize():
    register()
    Gui.addWorkbench(ConstraintInspectorWorkbench())
    install()
