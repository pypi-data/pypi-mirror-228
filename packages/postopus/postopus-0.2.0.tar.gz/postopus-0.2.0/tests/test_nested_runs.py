from pathlib import Path

import pandas as pd
import pytest
import xarray as xr

from postopus import nestedRuns


def test_nested_runs():
    n = nestedRuns(Path("tests/data/nested_runs/"))
    nruns = n.tests.data.nested_runs

    # convergence
    convergence = pd.concat(nruns.apply(lambda run: run.default.scf.convergence))
    level_values = convergence.index.get_level_values(None)  # get values of deltas
    expected_deltas = ["deltax_0.6", "deltax_0.5", "deltax_0.4"]
    assert all(element in level_values for element in expected_deltas) is True
    assert len(convergence) == 48
    assert pytest.approx(-133.932888) in sorted(convergence["energy"].values)
    assert pytest.approx(-120.397692) in sorted(convergence["energy"].values)
    assert pytest.approx(-136.33116) in sorted(convergence["energy"].values)

    # density fields
    fields = nruns.apply(lambda run: run.default.scf.density.get_all())
    assert type(fields["deltax_0.6"]) == xr.DataArray
    assert fields["deltax_0.6"].max() == pytest.approx(2.41953472)
