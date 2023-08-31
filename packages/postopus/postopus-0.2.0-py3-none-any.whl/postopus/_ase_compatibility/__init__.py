import sys

from ase.io.xsf import read_xsf

if sys.version_info < (3, 9):
    from importlib_resources import as_file, files
else:
    from importlib.resources import as_file, files


def _ase_compatibility():
    with as_file(files("postopus").joinpath("_ase_compatibility/density.xsf")) as file:
        with open(file) as f:
            return len(read_xsf(f, index=-1, read_data=True)) == 4
