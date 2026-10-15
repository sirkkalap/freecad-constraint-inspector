# SPDX-License-Identifier: LGPL-2.1-or-later
"""Attach the registered command to Sketcher's existing Constraints toolbar."""
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets

from .commands import ICON_PATH
from .i18n import tr

COMMAND = 'ConstraintInspector_Show'
_installed = False


def attach():
    try:
        workbench = Gui.activeWorkbench()
    except RuntimeError:
        # FreeCAD has not activated its initial workbench yet. The connected
        # workbenchActivated signal will attach the button when Sketcher opens.
        return
    if workbench is None or workbench.name() != 'SketcherWorkbench':
        return
    window = Gui.getMainWindow()
    toolbar = window.findChild(QtWidgets.QToolBar, 'Constraints')
    command = Gui.Command.get(COMMAND)
    if toolbar is None or command is None:
        return
    if any(action.objectName() == COMMAND for action in toolbar.actions()):
        return
    # Command QActions are created lazily by FreeCAD, so the inspector workbench
    # may not have created one yet. Route this button through the command system.
    action_class = getattr(QtGui, 'QAction', None) or QtWidgets.QAction
    action = action_class(QtGui.QIcon(ICON_PATH), tr('Constraint bindings'), toolbar)
    action.setObjectName(COMMAND)
    action.setToolTip(tr('Show all explicit sketch constraint references'))
    action.triggered.connect(lambda checked=False: Gui.runCommand(COMMAND))
    toolbar.addAction(action)


def _workbench_activated(name):
    if name == 'SketcherWorkbench':
        # Let FreeCAD finish rebuilding its toolbars before attaching.
        QtCore.QTimer.singleShot(0, attach)


def install():
    """Install once at addon startup; also supports an already-active Sketcher."""
    global _installed
    if not _installed:
        Gui.getMainWindow().workbenchActivated.connect(_workbench_activated)
        _installed = True
    attach()
