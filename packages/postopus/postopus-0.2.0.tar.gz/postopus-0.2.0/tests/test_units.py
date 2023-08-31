import pathlib

import pytest

from postopus.octopus_run import Run

test_au_data_dir = pathlib.Path(__file__).parent / "data" / "methane"
run_au = Run(test_au_data_dir)

test_ev_angstrom_data_dir = pathlib.Path(__file__).parent / "data" / "benzene"
run_ev_angstrom = Run(test_ev_angstrom_data_dir)


def test_au_units():
    xarr1 = run_au.default.scf.density.get_converged("xsf")
    xarr2 = run_au.default.scf.density.get([1, 2], "vtk")
    xarr3 = run_au.default.scf.density.iget(-1, "ncdf")
    xarr4 = run_au.default.td.density.get_all("ncdf")
    xarr5 = run_au.default.td.current.get(1, "ncdf")
    xarr6 = run_au.default.td.current.x.iget(-1, "ncdf")
    xarr7 = run_au.default.td.current.get_all("ncdf")

    # units of whole xarray == au
    assert (
        xarr1.units
        == xarr2.units
        == xarr3.units
        == xarr4.units
        == xarr5.units
        == xarr6.units
        == xarr7.units
        == "au"
    )

    # coord units
    for dim in "xyz":
        assert (
            xarr1[dim].units
            == xarr2[dim].units
            == xarr3[dim].units
            == xarr4[dim].units
            == xarr5[dim].units
            == xarr6[dim].units
            == xarr7[dim].units
            == "Bohr"
        )

    assert xarr4.t.units == xarr5.t.units == xarr6.t.units == xarr7.units == "au"

    with pytest.raises(
        AttributeError, match=r"'DataArray' object has no attribute 'units'"
    ):
        xarr1.step.units  # step doesn't have a physical unit


def test_ev_angstrom_units():
    # TODO: This is incomplete: test data is missing, e.g no td eV_Angstrom data
    xarr1 = run_ev_angstrom.default.scf.density.get_converged("xsf")
    xarr2 = run_ev_angstrom.default.scf.density.get_converged("cube")
    xarr3 = run_ev_angstrom.default.scf.density.get_converged("vtk")
    xarr4 = run_ev_angstrom.default.scf.density.get_converged("z=0")
    xarr5 = run_ev_angstrom.default.scf.density.get_converged("y=0,z=0")

    # units of whole xarray == au
    assert xarr1.units == xarr3.units == xarr4.units == xarr5.units == "eV_Ångstrom"

    # units of cube always au, independent of UnitsOutput in parser.log
    xarr2.units == "au"

    # coord units
    for dim in "xyz":
        assert xarr1[dim].units == xarr3[dim].units == "Ångstrom"
        assert xarr2[dim].units == "Bohr"
        if dim in "xy":  # z=0
            assert xarr4[dim].units == "Ångstrom"
        if dim == "x":  # y=0, z=0
            assert xarr5[dim].units == "Ångstrom"

    with pytest.raises(
        AttributeError, match=r"'DataArray' object has no attribute 'units'"
    ):
        xarr1.step.units  # step doesn't have a physical unit
