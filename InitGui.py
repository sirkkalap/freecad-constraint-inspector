# SPDX-License-Identifier: LGPL-2.1-or-later

"""FreeCAD discovers this entry point in its user Mod directory."""
import FreeCADGui as Gui
from constraint_inspector.commands import ICON_PATH, register
from constraint_inspector.toolbar import install

register()
install()


class ConstraintInspectorWorkbench(Gui.Workbench):
    Icon = ICON_PATH
    MenuText = 'Constraint Inspector'
    ToolTip = 'Inspect Sketcher constraint bindings, including origin and axes'

    def Initialize(self):
        self.appendMenu('Constraint Inspector', ['ConstraintInspector_Show'])
        self.appendToolbar('Constraint Inspector', ['ConstraintInspector_Show'])

    def GetClassName(self):
        return 'Gui::PythonWorkbench'


Gui.addWorkbench(ConstraintInspectorWorkbench())
