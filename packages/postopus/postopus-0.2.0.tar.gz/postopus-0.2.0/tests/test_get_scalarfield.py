import pathlib
import shutil

import numpy
import numpy as np
import numpy.testing as npt
import pytest

from postopus.octopus_run import Run

testdata_dir = pathlib.Path(__file__).parent / "data" / "methane"
run = Run(testdata_dir)
tdtimestep = 0.05

run2 = Run(testdata_dir.parent / "methane_min_no_static")
run3 = Run(testdata_dir.parent / "methane_missing_td_extensions")


def test_get_single_index():
    index_to_load = 1
    xarr = run.default.scf.density.iget(index_to_load, "xsf")
    # check available dimensions
    assert xarr.dims == ("step", "x", "y", "z")
    # check for only one time step
    assert sorted(xarr.coords["step"].values) == numpy.array([2])

    assert xarr.sel(step=2).values.shape == (27, 27, 27)

    # td
    xarr = run.default.td.density.get(index_to_load, "ncdf")
    # check available dimensions
    assert xarr.dims == ("t", "x", "y", "z")
    assert xarr.coords["t"].values == np.array(
        [index_to_load * tdtimestep]
    )  # explicit time values

    # negative integer scf
    index_to_load = -1
    xarr = run.default.scf.density.iget(index_to_load, "xsf")
    xarr_converged = run.default.scf.density.get_converged("xsf")
    assert np.all(xarr == xarr_converged)

    # negative integer td
    ixarr = run.default.td.density.iget(-1, "ncdf")
    xarr = run.default.td.density.get(30, "ncdf")
    assert np.all(ixarr == xarr)


def test_get_single_step():
    step_to_load = 1
    xarr = run.default.scf.density.get(step_to_load, "xsf")
    # check available dimensions
    assert xarr.dims == ("step", "x", "y", "z")
    # check for only one time step
    assert sorted(xarr.coords["step"].values) == numpy.array([step_to_load])

    assert xarr.sel(step=1).values.shape == (27, 27, 27)

    # td
    xarr = run.default.td.density.get(step_to_load, "ncdf")
    # check available dimensions
    assert xarr.dims == ("t", "x", "y", "z")
    assert xarr.coords["t"].values == np.array(
        [step_to_load * tdtimestep]
    )  # explicit time values

    # source auto
    axarr = run3.default.td.density.get(step_to_load)
    assert np.all(axarr == xarr)


def test_get_list_of_steps():
    steps_to_load = [5, 7, 12, 1]
    xarr = run.default.scf.density.get(steps_to_load, "xsf")
    # check available dimensions
    assert xarr.dims == ("step", "x", "y", "z")
    # check for only one time step
    npt.assert_equal(xarr.coords["step"].values, numpy.array(steps_to_load))

    assert xarr.sel(step=5).values.shape == (27, 27, 27)

    # td
    xarr = run.default.td.density.get(steps_to_load, "ncdf")
    # check available dimensions
    assert xarr.dims == ("t", "x", "y", "z")
    npt.assert_equal(
        xarr.coords["t"].values, np.array([step * tdtimestep for step in steps_to_load])
    )

    # source auto
    axarr = run3.default.td.density.get(steps_to_load)
    assert np.all(xarr == axarr)


def test_get_list_of_indices():
    """
    In td mode, the indices are the same as the steps. In scf mode steps start at 1.
    """
    indices_to_load = [4, 6, 11, 0]
    xarr = run.default.scf.density.iget(indices_to_load, "xsf")
    # check available dimensions
    assert xarr.dims == ("step", "x", "y", "z")
    # check for only one time step
    npt.assert_equal(xarr.coords["step"].values, numpy.array([5, 7, 12, 1]))

    assert xarr.sel(step=5).values.shape == (27, 27, 27)

    # td
    indices_to_load_td = [i + 1 for i in indices_to_load]
    xarr = run.default.td.density.iget(indices_to_load_td, "ncdf")
    # check available dimensions
    assert xarr.dims == ("t", "x", "y", "z")
    npt.assert_equal(
        xarr.coords["t"].values,
        np.array([step * tdtimestep for step in indices_to_load_td]),
    )

    # source "auto"
    axarr = run3.default.td.density.iget(indices_to_load_td)
    assert np.all(axarr == xarr)


def test_get_slice_of_indices():
    slice_to_load = slice(7, 10)
    xarr = run.default.scf.density.iget(indices=slice_to_load, source="xsf")
    assert xarr.shape == (3, 27, 27, 27)
    assert np.all(xarr.step.values == np.array([8, 9, 10]))


def test_get_all_steps():
    existing_steps = list(range(1, 19))
    xarr = run.default.scf.density.get_all("xsf")
    # check available dimensions
    assert xarr.dims == ("step", "x", "y", "z")
    # check for only one time step
    npt.assert_equal(sorted(xarr.coords["step"].values), numpy.array(existing_steps))

    assert xarr.sel(step=5).values.shape == (27, 27, 27)


def test_get_bad_params(tmp_path, mock_inp_and_parser_log_and_output):
    # Test loading non-existing single iterations
    with pytest.raises(
        ValueError, match=r"Requested iteration '[0-9].*' does not exist for '[a-z].*'."
    ):
        run.default.scf.density.get(42, "xsf")

    # iteration number out of range
    with pytest.raises(
        ValueError, match=r"Requested iteration '[0-9].*' does not exist for '[a-z].*'."
    ):
        run.default.scf.density.get([42, 19], "xsf")

    # iteration number out of range
    with pytest.raises(
        ValueError, match=r"Requested iteration '[0-9].*' does not exist for '[a-z].*'."
    ):
        run.default.scf.density.get([42, 19], "bla")

    # Found extension and no parser
    run3 = Run(tmp_path)
    with pytest.raises(NotImplementedError, match=r"Existing file [a-zA-Z0-9/.!()']"):
        run3.default.scf.mock_scalarfield.get(1, "sdfjk")

    # Not found extension and existing parser
    with pytest.raises(ValueError, match=r"File does not exist: [a-zA-Z0-9/.!()']"):
        run.default.scf.density.get(1, "y=0")

    # Not found extension and no parser
    with pytest.raises(ValueError, match=r"We did not find [a-zA-Z0-9/.!()']"):
        run.default.scf.density.get(1, "bla")

    # str as step parameter, TypeError
    with pytest.raises(TypeError, match=r"steps parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.scf.density.get("bla", "xsf")

    # float as step parameter, TypeError
    with pytest.raises(TypeError, match=r"steps parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.scf.density.get(1.2, "xsf")

    # No step parameter, TypeError
    with pytest.raises(TypeError, match=r"steps parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.scf.density.get()

    # Not specifying the source, although there is more than one
    with pytest.raises(
        ValueError, match=r"There is more than one available source [a-zA-Z().\s']*"
    ):
        run.default.scf.density.get(1)

    # Not specifying the source, although there is more than one
    with pytest.raises(
        ValueError, match=r"There is more than one available source [a-zA-Z().\s']*"
    ):
        run.default.scf.density.get_all()

    # Not specifying the source, although there is more than one
    with pytest.raises(
        ValueError, match=r"There is more than one available source [a-zA-Z().\s']*"
    ):
        run.default.scf.density.get([1, 2])

    # No static data for scf, thus cannot get converged iteraiton
    with pytest.raises(ValueError, match=r"There is no static data avail[a-z., _']*"):
        run2.default.scf.density.get_converged(source="ncdf")

    # For td there are no converged iterations
    with pytest.raises(ValueError, match=r"Please provide a value for [a-zOCM., _!']"):
        run2.default.td.density.get_converged(source="ncdf")

    # Index out of range
    with pytest.raises(IndexError, match=r"tuple index out of range"):
        run.default.scf.density.iget(-19, source="ncdf")

    # Index out of range
    with pytest.raises(IndexError, match=r"tuple index out of range"):
        run.default.scf.density.iget(19, source="ncdf")

    # str as indices parameter
    with pytest.raises(TypeError, match=r"indices parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.scf.density.iget("bla", "xsf")

    # No indices parameter provided, TypeError
    with pytest.raises(TypeError, match=r"indices parameter needs t[a-zA-Z0-9/.!()']"):
        run.default.scf.density.iget()


def test_get_static_data():
    static_no_step = run.default.scf.density.get_converged(source="xsf").values
    static_by_step = run.default.scf.density.get(18, source="xsf").values
    npt.assert_array_equal(static_no_step, static_by_step)


def test_memory_size_check(tmp_path, mock_inp_and_parser_log_and_output):
    """
    Generate a numpy file with ~512MB in step 1 and simulate 500 steps. Gitlab CI
    machines have 4GB memory, but user devices might have up to 64GB, so just
    some big number of steps. Only 512MB will be on disk

    Parameters
    ----------
    tmp_path

    Returns
    -------

    """

    (tmp_path / "output_iter").mkdir(exist_ok=True)
    shutil.copy(testdata_dir / "inp", tmp_path)
    for step in range(1, 501):
        (tmp_path / "output_iter" / ("scf." + str(step).zfill(4))).mkdir(exist_ok=True)
        (
            tmp_path / "output_iter" / ("scf." + str(step).zfill(4)) / "density.z=0"
        ).touch()

    # write
    numpy.savetxt(
        tmp_path / "output_iter" / "scf.0001" / "density.z=0",
        np.array(
            list(
                zip(
                    np.linspace(-100, 100, 13500),
                    np.linspace(-50, 50, 13500),
                    np.arange(13500),
                )
            )
        ),
        header="         x                      y           "
        "          Re                     Im",
    )

    run = Run(tmp_path)
    with pytest.raises(MemoryError, match=r"You are trying to loa[0-9a-zA-Z.!-: _()']"):
        run.default.scf.density.get_all(source="z=0")
