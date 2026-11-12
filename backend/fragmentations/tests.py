from types import SimpleNamespace

from django.test import SimpleTestCase

from fragmentations.mutation import (
    release_is_blocked_by_irregular_antibodies,
    validate_release_items,
)


def make_item(blocks_release, has_irregular_antibodies, name='PLASMA FRESCO CONGELADO'):
    immunohematology = SimpleNamespace(
        exists_irregular_antibodies=has_irregular_antibodies
    )
    donation = SimpleNamespace(immunohematology=immunohematology)
    extraction = SimpleNamespace(donation=donation)
    fragmentation = SimpleNamespace(extraction=extraction)
    typehemocomponent = SimpleNamespace(
        name=name,
        blocks_release_with_irregular_antibodies=blocks_release
    )
    return SimpleNamespace(
        typehemocomponent=typehemocomponent,
        fragmentation=fragmentation,
        donor_code=12345
    )


class IrregularAntibodyReleaseTests(SimpleTestCase):
    def test_restricted_hemocomponent_is_blocked_for_positive_result(self):
        item = make_item(blocks_release=True, has_irregular_antibodies=True)

        self.assertTrue(release_is_blocked_by_irregular_antibodies(item))

    def test_other_hemocomponent_is_not_blocked(self):
        item = make_item(
            blocks_release=False,
            has_irregular_antibodies=True,
            name='CONCENTRADO DE HEMATIES'
        )

        self.assertFalse(release_is_blocked_by_irregular_antibodies(item))

    def test_restricted_hemocomponent_is_allowed_for_negative_result(self):
        item = make_item(blocks_release=True, has_irregular_antibodies=False)

        self.assertFalse(release_is_blocked_by_irregular_antibodies(item))

    def test_validation_reports_blocked_hemocomponent(self):
        item = make_item(blocks_release=True, has_irregular_antibodies=True)

        with self.assertRaisesRegex(ValueError, 'PLASMA FRESCO CONGELADO'):
            validate_release_items([item])
