# Repository Guidelines

This is a standalone FreeCAD GUI addon. Read `README.md` for installation and
runtime details. `InitGui.py` registers the workbench, `commands.py` registers
its command, and `panel.py` contains the read-only dock.

Preserve the read-only behavior: do not change geometry, constraints, selection
or document persistence from refresh callbacks. Keep Qt widgets and timers on
the FreeCAD GUI thread. Use four-space Python indentation and descriptive names.
Imports must not open widgets; `show_panel()` is the explicit UI entry point.

Do not run tests unless the user requests testing or verification. No automated
test suite is configured. Report unverified FreeCAD/Qt compatibility honestly.
Do not publish or install externally without user authorization.
