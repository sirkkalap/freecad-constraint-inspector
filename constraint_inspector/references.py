# SPDX-License-Identifier: LGPL-2.1-or-later

"""Read-only formatting of FreeCAD constraint geometry references."""


def describe_reference(sketch, geo, pos, tr=lambda text: text):
    if geo == -2000:
        return '—'
    if geo == -1 and pos == 1:
        return tr('Origin')
    if geo in (-1, -2):
        name = tr('Horizontal axis (X)') if geo == -1 else tr('Vertical axis (Y)')
    elif geo >= 0:
        try:
            kind = sketch.Geometry[geo].TypeId.rsplit('::', 1)[-1]
            name = 'Edge{} ({}, ID {})'.format(geo + 1, kind, geo)
        except (IndexError, AttributeError):
            name = tr('Geometry ID {}').format(geo)
    else:
        name = tr('External geometry ID {}').format(geo)
    suffix = {0: '', 1: tr(' / start point'), 2: tr(' / end point'),
              3: tr(' / center point')}.get(pos, tr(' / point {}').format(pos))
    return name + suffix

