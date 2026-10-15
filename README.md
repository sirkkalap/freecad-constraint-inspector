# FreeCAD Constraint Inspector

A standalone Python addon for inspecting Sketcher constraint bindings. The
read-only dock lists each constraint's type and all three explicit references,
including the sketch origin, horizontal/vertical axes and point positions.
The interface supports English and Finnish, following FreeCAD's language
setting. Other languages use English. Reopen the panel after changing language;
restart FreeCAD to refresh command menu labels. FreeCAD constraint types and
geometry identifiers retain their original API names.

## Installation

Requires FreeCAD's GUI, bundled Python and PySide. No pip dependencies.
The original script was run in FreeCAD 1.1.4 on macOS; this extracted addon has
not yet been tested as an installed workbench.

1. In FreeCAD's Python console, run `print(App.getUserAppDataDir())`.
2. Copy or symlink this entire project into the `Mod/ConstraintInspector`
   directory below that path. Create `Mod` if necessary.
3. Restart FreeCAD and select the **Constraint Inspector** workbench.
4. Choose **Constraint Inspector → Constraint bindings**
   (Finnish: **Rajoitteiden sidonnat**).
5. Switch to Sketcher and edit a sketch. The dock remains open and follows
   selected constraints. Close the dock to stop refreshing.

To open directly during development without installation, run in FreeCAD's
Python console (substitute the actual project path):

```python
import sys
sys.path.insert(0, '/absolute/path/to/freecad-constraint-inspector')
from constraint_inspector.panel import show_panel
show_panel()
```

## Project structure

- `InitGui.py`: workbench and menu registration.
- `constraint_inspector/commands.py`: command entry point.
- `constraint_inspector/panel.py`: dock, reference labels and selection tracking.
- `constraint_inspector/i18n.py`: English UI strings and Finnish translations.
- `constraint_inspector/references.py`: reference interpretation, independent of Qt.
- `tests/`: standard-library unit tests.

No build step is required. The GUI runs inside FreeCAD. Do not modify the
user's document while inspecting.

## Tests

Run from the project root using system Python 3; no FreeCAD, Qt or additional
packages are needed:

```sh
python3 -m unittest discover -s tests -v
```

Tests cover language selection and fallback, translation completeness and
format placeholders, and constraint references including the origin, axes,
arc endpoints/center, external IDs and missing geometry. FreeCAD preference
access is simulated in the language integration test. Qt rendering, docking,
selection synchronization and installed-workbench loading still need manual
validation in FreeCAD.

## Scope and limitations

The inspector displays explicit `First`, `Second`, `Third` and corresponding
point-position fields. Hover over cells for raw IDs. External geometry retains
its raw ID; indirect dependencies through other constraints and implicit
reference frames are not expanded. References are not selectable from the dock.
The panel polls every 400 ms and is not intended for very large sketches.

## Removal

Close FreeCAD, remove only this addon's directory/symlink from `Mod`, and restart.
No document migration is required. This project has not been published to the
Addon Manager.


## License

This project is licensed under the GNU Lesser General Public License,
version 2.1 or (at your option) any later version (`LGPL-2.1-or-later`).
See [LICENSE](LICENSE) for the full license text.

You may use, modify and redistribute the addon, including commercially,
subject to the license terms. Distributed modifications to the addon remain
under the LGPL. The software is provided without warranty.
