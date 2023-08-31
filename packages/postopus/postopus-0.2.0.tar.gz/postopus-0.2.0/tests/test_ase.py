import os

import pytest


@pytest.mark.skipif(
    os.getenv("TEST_POSTOPUS_ASE_COMPATIBILITY") is None,
    reason="Only for pipeline testing",
)
def test_ase_old_tag():
    """ "
    Test if the ase has still the old tag. If this fails, the ase version has been
    updated and could be added as a dependency. Moreover, the ase_compatibility module
    wouldn't be needed anymore. Also delete the note in the README.md and this test.
    """
    with pytest.raises(RuntimeError):
        import postopus  # noqa: F401
