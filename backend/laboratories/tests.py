import os
import tempfile

from django.test import SimpleTestCase
from django.test import override_settings

from laboratories.models import Immunohematology
from siicobs_main.utils_billing import build_picture_barcode_bg


class IrregularAntibodyDetectionTests(SimpleTestCase):
    def test_positive_panel_reaction_is_detected(self):
        result = Immunohematology(
            fsi='-', liss='-', alb='-', coombs='-',
            p2fsi='-', p2liss='-', p2alb='-', p2coombs='-',
            p3fsi='+', p3liss='-', p3alb='-', p3coombs='-'
        )

        self.assertTrue(result.exists_irregular_antibodies)

    def test_negative_and_empty_panel_results_are_not_positive(self):
        result = Immunohematology(
            fsi='-', liss='-', alb=None, coombs='-',
            p2fsi='-', p2liss=None, p2alb='-', p2coombs='-',
            p3fsi=None, p3liss=None, p3alb=None, p3coombs=None
        )

        self.assertFalse(result.exists_irregular_antibodies)


class BloodBagBarcodeTests(SimpleTestCase):
    def test_barcode_creates_missing_media_subdirectory(self):
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                build_picture_barcode_bg('192368', '192368')

            barcode_path = os.path.join(media_root, 'laboratory', '192368.png')
            self.assertTrue(os.path.isfile(barcode_path))
