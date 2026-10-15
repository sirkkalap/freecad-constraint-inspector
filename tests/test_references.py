# SPDX-License-Identifier: LGPL-2.1-or-later
"""Reference semantics, particularly origin versus horizontal axis."""
from types import SimpleNamespace
import unittest

from constraint_inspector.i18n import tr
from constraint_inspector.references import describe_reference


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.sketch = SimpleNamespace(Geometry=(SimpleNamespace(TypeId='Part::GeomArcOfCircle'),))

    def test_origin_is_distinct_from_horizontal_axis(self):
        self.assertEqual(describe_reference(self.sketch, -1, 1), 'Origin')
        self.assertEqual(describe_reference(self.sketch, -1, 0), 'Horizontal axis (X)')
        self.assertEqual(describe_reference(self.sketch, -2, 0), 'Vertical axis (Y)')

    def test_unused_reference_is_not_geometry(self):
        self.assertEqual(describe_reference(self.sketch, -2000, 0), '—')

    def test_arc_positions_and_display_numbering(self):
        for pos, suffix in ((0, ''), (1, ' / start point'), (2, ' / end point'),
                            (3, ' / center point')):
            with self.subTest(pos=pos):
                self.assertEqual(describe_reference(self.sketch, 0, pos),
                                 'Edge1 (GeomArcOfCircle, ID 0)' + suffix)

    def test_external_geometry_preserves_raw_id(self):
        self.assertEqual(describe_reference(self.sketch, -3, 2),
                         'External geometry ID -3 / end point')

    def test_missing_geometry_and_unknown_position_remain_identifiable(self):
        self.assertEqual(describe_reference(self.sketch, 42, 7),
                         'Geometry ID 42 / point 7')

    def test_labels_can_be_translated_without_changing_ids(self):
        translate = lambda text: tr(text, 'Finnish')
        self.assertEqual(describe_reference(self.sketch, -1, 1, translate), 'Origo')
        self.assertEqual(describe_reference(self.sketch, 0, 3, translate),
                         'Edge1 (GeomArcOfCircle, ID 0) / keskipiste')
