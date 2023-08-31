import pathlib
from typing import Any

from postopus.files.cube import CubeFile
from postopus.files.netcdf import NetCDFFile
from postopus.files.pandas_text import PandasTextFile
from postopus.files.text import TextFile
from postopus.files.vtk import VTKFile
from postopus.files.xcrysden import XCrySDenFile
from postopus.files.xyz import XYZFile

extension_loader_map = {
    ext: cls
    for cls in [
        CubeFile,
        NetCDFFile,
        TextFile,
        VTKFile,
        XYZFile,
        XCrySDenFile,
        PandasTextFile,
    ]
    for ext in cls.EXTENSIONS
}


def openfile(filepath: pathlib.Path) -> Any:
    """
    Will automatically choose the correct class to open a file.

    :param filepath: path to the file that shall be opened
    :return: instance class that was chosen to open the file with postopus file loaders
    """
    # Get the class to use for loading the file (without '.')
    # [1:] also work with no suffixes (must be a str thing...)
    cls = extension_loader_map[filepath.suffix[1:]]

    # instantiate object for file type
    try:
        return cls(filepath)
    # This should never happen, since we are already reading the filesystem in
    # self.check_if_source_exist
    except FileNotFoundError:
        raise FileNotFoundError(
            f"There is a  parser for '{filepath.suffix[1:]}' files,"
            f" but {filepath} was not found. Please contact the developer team if you"
            f"see this message."
        )
