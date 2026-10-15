# SPDX-License-Identifier: LGPL-2.1-or-later

"""English UI with Finnish translations, following FreeCAD's language setting.

Reopen the panel after changing language. FreeCAD identifiers remain unchanged.
"""


_FINNISH = {
    'Constraint bindings': 'Rajoitteiden sidonnat',
    'Show all explicit sketch constraint references':
        'Näytä luonnoksen rajoitteiden kaikki suorat viittaukset',
    'Constraint': 'Rajoite',
    'Type': 'Tyyppi',
    'Reference 1': 'Osapuoli 1',
    'Reference 2': 'Osapuoli 2',
    'Reference 3': 'Osapuoli 3',
    'Select a constraint in Sketcher to highlight its row here.\n'
    'Only explicit references are shown; indirect dependencies are not expanded.\n'
    'Hover over a cell to see raw identifiers.':
        'Valitse rajoite Sketcherissä: vastaava rivi korostuu tässä.\n'
        'Näkyvissä ovat suorat viittaukset; epäsuoria riippuvuuksia ei laajenneta.\n'
        'Vie hiiri solun päälle nähdäksesi raakatunnisteet.',
    'Origin': 'Origo',
    'Horizontal axis (X)': 'Vaaka-akseli (X)',
    'Vertical axis (Y)': 'Pystyakseli (Y)',
    'Geometry ID {}': 'Geometria ID {}',
    'External geometry ID {}': 'Ulkoinen geometria ID {}',
    ' / start point': ' / alkupiste',
    ' / end point': ' / loppupiste',
    ' / center point': ' / keskipiste',
    ' / point {}': ' / piste {}',
    'Edit or select a sketch to inspect its constraints.':
        'Avaa luonnos muokkaustilaan tai valitse luonnos.',
    '{} / {} — constraints: {}': '{} / {} — rajoitteita: {}',
}


def tr(text, language=None):
    """Translate known UI strings; unsupported languages fall back to English."""
    if language is None:
        import FreeCAD as App
        language = App.ParamGet('User parameter:BaseApp/Preferences/General').GetString(
            'Language', 'English')
    language = language.lower().replace('-', '_')
    if language in ('finnish', 'suomi', 'fi') or language.startswith('fi_'):
        return _FINNISH.get(text, text)
    return text
