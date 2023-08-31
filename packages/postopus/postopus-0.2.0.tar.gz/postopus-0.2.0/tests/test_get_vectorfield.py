import pathlib

import numpy
import numpy.testing as npt
import pytest

from postopus.octopus_run import Run

testdata_dir = pathlib.Path(__file__).parent / "data" / "methane"
run = Run(testdata_dir)
tdtimestep = 0.05  # From exec/parser.log


def test_get_single_index():
    index_to_load = 1
    ixarr = run.default.td.current.iget(index_to_load, "ncdf")
    # check available dimensions
    assert sorted(ixarr.dims) == sorted(["t", "x", "y", "z", "component"])
    # check for only one time step
    assert sorted(ixarr.coords["t"].values) == numpy.array([tdtimestep])

    assert ixarr.sel(t=tdtimestep).values.shape == (3, 27, 27, 27)

    # negative integer td
    ixarr = run.default.td.current.iget(-1, "ncdf")
    xarr = run.default.td.current.get(30, "ncdf")
    assert numpy.all(ixarr == xarr)


def test_get_single_step():
    step_to_load = 1
    timestep_to_load = step_to_load * tdtimestep
    xarr = run.default.td.current.get(step_to_load, "ncdf")
    # check available components
    assert sorted(xarr.dims) == sorted(["t", "x", "y", "z", "component"])
    # check for only one time step
    assert sorted(xarr.coords["t"].values) == numpy.array([timestep_to_load])

    assert xarr.sel(t=timestep_to_load).values.shape == (3, 27, 27, 27)
    assert xarr.sel(t=timestep_to_load, component="x").shape == (27, 27, 27)

    npt.assert_equal(
        xarr.sel(component="x").values,
        run.default.td.current.x.get(step_to_load, "ncdf").values,
    )


def test_get_list_of_steps():
    steps_to_load = [5, 7, 12, 1]
    timesteps_to_load = [step * tdtimestep for step in steps_to_load]
    xarr = run.default.td.current.get(steps_to_load, "ncdf")
    # check available components
    assert sorted(xarr.dims) == sorted(["t", "x", "y", "z", "component"])
    # check for only one time step
    assert sorted(xarr.coords["t"].values) == sorted(timesteps_to_load)

    assert xarr.sel(t=timesteps_to_load[0]).values.shape == (3, 27, 27, 27)
    assert xarr.sel(t=timesteps_to_load[0], component="x").shape == (27, 27, 27)

    # iget list of indices
    # indices and steps are the same by chance
    indices_to_load = [5, 7, 12, 1]
    ixarr = run.default.td.current.iget(indices_to_load, "ncdf")

    assert numpy.all(ixarr == xarr)


def test_get_all_steps():
    existing_steps = list(range(0, 31))
    existing_timesteps = [step * tdtimestep for step in existing_steps]
    xarr = run.default.td.current.get_all("ncdf")
    # check available components
    assert sorted(xarr.dims) == sorted(["t", "x", "y", "z", "component"])
    # check for only one time step
    assert sorted(xarr.coords["t"].values) == sorted(existing_timesteps)

    assert xarr.sel(t=5 * tdtimestep).values.shape == (3, 27, 27, 27)
    assert xarr.sel(t=5 * tdtimestep, component="x").shape == (27, 27, 27)

    # iget slice
    xarr_slice = xarr.sel(t=slice(0, 0.1))
    ixarr_slice = run.default.td.current.iget(indices=slice(0, 3), source="ncdf")

    assert numpy.all(ixarr_slice == xarr_slice)


def test_get_bad_params(tmp_path, mock_inp_and_parser_log_and_output):
    # Test loading non-existing single iterations
    with pytest.raises(
        ValueError, match=r"Requested iteration '[0-9].*' does not exist for '[a-z].*'."
    ):
        run.default.td.current.get(72, "ncdf")

    # Test loading non-existing single iterations
    with pytest.raises(ValueError, match=r"We don't support the syntax '[a-z].*'."):
        run.default.td.current.x.get(0, "vtk")

    # iteration number out of range
    with pytest.raises(
        ValueError, match=r"Requested iteration '[0-9].*' does not exist for '[a-z].*'."
    ):
        run.default.td.current.get([72, 19], "ncdf")

    # iteration number out of range
    with pytest.raises(
        ValueError, match=r"Requested iteration '[0-9].*' does not exist for '[a-z].*'."
    ):
        run.default.td.current.get([72, 19], "bla")

    # Found extension and no parser
    run2 = Run(tmp_path)
    with pytest.raises(NotImplementedError, match=r"Existing file [a-zA-Z0-9/.!()']"):
        run2.default.scf.mock_vectorfield.get(1, "sdfjk")

    # Not found extension and existing parser
    with pytest.raises(ValueError, match=r"File does not exist: [a-zA-Z0-9/.!()']"):
        run.default.td.current.get(1, "y=0")

    # Not found extension and no parser
    with pytest.raises(ValueError, match=r"We did not find [a-zA-Z0-9/.!()']"):
        run.default.td.current.get(1, "bla")

    # str instead of int
    with pytest.raises(TypeError, match=r"steps parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.td.current.get("bla", "ncdf")

    # float instead of int
    with pytest.raises(TypeError, match=r"steps parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.td.current.get(1.2, "ncdf")

    # source="auto" NotImplemented yet
    with pytest.raises(
        ValueError, match=r"There is more than one available source [a-zA-Z().\s']*"
    ):
        run.default.td.current.get(0)

    # source="auto" NotImplemented yet
    with pytest.raises(
        ValueError, match=r"There is more than one available source [a-zA-Z().\s']*"
    ):
        run.default.td.current.get([5, 10])

    # source="auto" NotImplemented yet
    with pytest.raises(
        ValueError, match=r"There is more than one available source [a-zA-Z().\s']*"
    ):
        run.default.td.current.get_all()

    # No indices parameter provided, TypeError
    with pytest.raises(TypeError, match=r"indices parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.td.current.iget()
