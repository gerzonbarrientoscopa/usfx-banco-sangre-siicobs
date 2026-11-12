from django.test import SimpleTestCase

from laboratories.models import Immunohematology


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
