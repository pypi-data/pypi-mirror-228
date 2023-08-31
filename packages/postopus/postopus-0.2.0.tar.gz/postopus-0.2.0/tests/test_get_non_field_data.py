import pytest

from postopus import Run
from postopus.datacontainers.field import ScalarField as fld


def test_get_non_field_sources(tmp_path, mock_inp_and_parser_log_and_output):
    """
    Test the behavior if the user chooses a non-field extension for the get method.
    """
    run = Run(tmp_path)
    # Handle non-field extensions
    with pytest.raises(ValueError, match=r"xyz is not a known field [a-zA-Z0-9/.!()']"):
        run.default.scf.test_structures.get(1, "xyz")

    # Don't show non-field extensions as available parsers nor sources
    with pytest.raises(ValueError) as excinfo:
        run.default.scf.test_structures.get(1, "sfdjk")
    assert "We did not find" in str(excinfo.value)
    assert any(x not in str(excinfo.value) for x in fld.NON_FIELD_SOURCES)
