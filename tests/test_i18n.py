# SPDX-License-Identifier: LGPL-2.1-or-later
"""Translation behavior; runnable without FreeCAD or Qt."""
import ast
from pathlib import Path
from string import Formatter
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from constraint_inspector.i18n import _FINNISH, tr


class TranslationTests(unittest.TestCase):
    def test_finnish_language_names_and_locales(self):
        for language in ('Finnish', 'suomi', 'fi', 'fi_FI', 'fi-FI', 'FI-fi'):
            with self.subTest(language=language):
                self.assertEqual(tr('Origin', language), 'Origo')

    def test_english_and_unsupported_languages_use_source(self):
        for language in ('English', 'en_US', 'German', 'sv_SE', ''):
            with self.subTest(language=language):
                self.assertEqual(tr('Origin', language), 'Origin')

    def test_unknown_string_falls_back(self):
        self.assertEqual(tr('New label', 'Finnish'), 'New label')

    def test_reads_current_freecad_language_each_time(self):
        preference = SimpleNamespace(GetString=lambda key, default: 'Finnish')
        def param_get(path):
            self.assertEqual(path, 'User parameter:BaseApp/Preferences/General')
            return preference
        with patch.dict('sys.modules', {'FreeCAD': SimpleNamespace(ParamGet=param_get)}):
            self.assertEqual(tr('Origin'), 'Origo')
            preference.GetString = lambda key, default: default
            self.assertEqual(tr('Origin'), 'Origin')

    def test_translations_preserve_format_fields_and_line_breaks(self):
        def fields(text):
            return [field for _, field, _, _ in Formatter().parse(text) if field is not None]
        for source, translated in _FINNISH.items():
            with self.subTest(source=source):
                self.assertEqual(fields(source), fields(translated))
                self.assertEqual(source.count('\n'), translated.count('\n'))

    def test_all_literal_ui_translation_calls_have_finnish_entries(self):
        root = Path(__file__).resolve().parents[1] / 'constraint_inspector'
        for filename in ('panel.py', 'commands.py', 'references.py'):
            tree = ast.parse((root / filename).read_text())
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id == 'tr' and node.args
                        and isinstance(node.args[0], ast.Constant)):
                    with self.subTest(file=filename, text=node.args[0].value):
                        self.assertIn(node.args[0].value, _FINNISH)
