# SPDX-License-Identifier: LGPL-2.1-or-later

"""FreeCAD constraint bindings inspector.

Read-only dock showing every explicit constraint reference, including origin/axes.
Uses FreeCAD's bundled Python and PySide; no additional dependencies.
"""

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets


class ConstraintInspector(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__('Rajoitteiden sidonnat', parent)
        self.setObjectName('ConstraintBindingsInspector')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        self.caption = QtWidgets.QLabel()
        self.caption.setWordWrap(True)
        layout.addWidget(self.caption)
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ['Rajoite', 'Tyyppi', 'Osapuoli 1', 'Osapuoli 2', 'Osapuoli 3'])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        layout.addWidget(self.table)
        note = QtWidgets.QLabel(
            'Valitse rajoite Sketcherissä: vastaava rivi korostuu tässä.\n'
            'Näkyvissä ovat suorat viittaukset; muiden rajoitteiden kautta '
            'syntyviä riippuvuuksia ei laajenneta.\n'
            'Vie hiiri solun päälle nähdäksesi raakatunnisteet.')
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

    def reference(self, sketch, geo, pos):
        if geo == -2000:
            return '—'
        if geo == -1 and pos == 1:
            return 'Origo'
        if geo in (-1, -2):
            name = 'Vaaka-akseli (X)' if geo == -1 else 'Pystyakseli (Y)'
        elif geo >= 0:
            try:
                kind = sketch.Geometry[geo].TypeId.rsplit('::', 1)[-1]
                name = 'Edge{} ({}, ID {})'.format(geo + 1, kind, geo)
            except (IndexError, AttributeError):
                name = 'Geometria ID {}'.format(geo)
        else:
            name = 'Ulkoinen geometria ID {}'.format(geo)
        suffix = {0: '', 1: ' / alkupiste', 2: ' / loppupiste',
                  3: ' / keskipiste'}.get(pos, ' / piste {}'.format(pos))
        return name + suffix

    def refresh(self):
        try:
            sketch = self.sketch()
            if sketch is None:
                self.caption.setText('Avaa luonnos muokkaustilaan tai valitse luonnos.')
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
            self.caption.setText('{} / {} — {} rajoitetta'.format(
                sketch.Document.Label, sketch.Label, len(rows)))
            if signature != self.signature:
                self.table.setRowCount(len(rows))
                for row, (label, kind, refs) in enumerate(rows):
                    values = [label, kind] + [self.reference(sketch, *r) for r in refs]
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
