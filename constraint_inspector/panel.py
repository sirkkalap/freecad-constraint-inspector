# SPDX-License-Identifier: LGPL-2.1-or-later

"""FreeCAD constraint bindings inspector.

Read-only dock showing every explicit constraint reference, including origin/axes.
Uses FreeCAD's bundled Python and PySide; no additional dependencies.
"""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

from .i18n import tr
from .references import describe_reference


class ConstraintInspector(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__(tr('Constraint bindings'), parent)
        self.setObjectName('ConstraintBindingsInspector')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        self.caption = QtWidgets.QLabel()
        self.caption.setWordWrap(True)
        layout.addWidget(self.caption)
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            [tr('Constraint'), tr('Type'), tr('Reference 1'), tr('Reference 2'), tr('Reference 3')])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        layout.addWidget(self.table)
        note = QtWidgets.QLabel(
            tr('Select a constraint in Sketcher to highlight its row here.\n'
               'Only explicit references are shown; indirect dependencies are not expanded.\n'
               'Hover over a cell to see raw identifiers.'))
        note.setWordWrap(True)
        layout.addWidget(note)
        self.setWidget(widget)
        self.signature = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(400)
        self.refresh()

    def sketch(self):
        doc = Gui.activeDocument()
        if doc:
            editing = doc.getInEdit()
            if editing and editing.Object.isDerivedFrom('Sketcher::SketchObject'):
                return editing.Object
        for obj in Gui.Selection.getSelection():
            if obj.isDerivedFrom('Sketcher::SketchObject'):
                return obj
        return None

    def refresh(self):
        try:
            sketch = self.sketch()
            if sketch is None:
                self.caption.setText(tr('Edit or select a sketch to inspect its constraints.'))
                self.table.setRowCount(0)
                self.signature = None
                return
            constraints = sketch.Constraints
            rows = []
            for i, c in enumerate(constraints):
                refs = [(c.First, c.FirstPos), (c.Second, c.SecondPos),
                        (c.Third, c.ThirdPos)]
                label = 'Constraint{}'.format(i + 1)
                if getattr(c, 'Name', ''):
                    label += ' ({})'.format(c.Name)
                rows.append((label, c.Type, refs))
            signature = (sketch.Document.Name, sketch.Name, repr(rows),
                         tuple(g.TypeId for g in sketch.Geometry))
            self.caption.setText(tr('{} / {} — constraints: {}').format(
                sketch.Document.Label, sketch.Label, len(rows)))
            if signature != self.signature:
                self.table.setRowCount(len(rows))
                for row, (label, kind, refs) in enumerate(rows):
                    values = [label, kind] + [describe_reference(sketch, *r, tr=tr) for r in refs]
                    for col, value in enumerate(values):
                        item = QtWidgets.QTableWidgetItem(value)
                        if col >= 2:
                            item.setToolTip('GeoId={}, PointPos={}'.format(*refs[col - 2]))
                        self.table.setItem(row, col, item)
                self.signature = signature
            selected = set()
            for selection in Gui.Selection.getSelectionEx():
                if selection.Object == sketch:
                    for sub in selection.SubElementNames:
                        if sub.startswith('Constraint') and sub[10:].isdigit():
                            selected.add(int(sub[10:]) - 1)
            self.table.clearSelection()
            for row in selected:
                if 0 <= row < self.table.rowCount():
                    index = self.table.model().index(row, 0)
                    self.table.selectionModel().select(
                        index, QtCore.QItemSelectionModel.Select |
                        QtCore.QItemSelectionModel.Rows)
        except (RuntimeError, ReferenceError):
            self.signature = None  # Document may have closed between callbacks.



def show_panel():
    """Open the inspector without changing the active workbench or document."""
    window = Gui.getMainWindow()
    previous = window.findChild(QtWidgets.QDockWidget, 'ConstraintBindingsInspector')
    if previous:
        previous.close()
    panel = ConstraintInspector(window)
    window.addDockWidget(QtCore.Qt.BottomDockWidgetArea, panel)
    panel.show()
    return panel
