from django.test import SimpleTestCase
from extractions.models import Extraction


class ExtractionBagTypeTests(SimpleTestCase):
    def test_type_bag_maps_to_physical_bag_quantity(self):
        self.assertEqual(
            Extraction.BAGS_QUANTITY_BY_TYPE,
            {
                'SIMPLE': 1,
                'DOBLE': 2,
                'TRIPLE': 3,
                'CUADRUPLE': 4,
                'CUADRUPLE_CON_FILTRO': 4,
                'SET_AFERESIS': 2,
            },
        )

    def test_invalid_type_bag_is_rejected_before_saving(self):
        with self.assertRaises(ValueError):
            Extraction(type_bag='NO_VALIDO').save()
