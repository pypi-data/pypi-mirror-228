import pathlib
from typing import Dict, Tuple

import numpy
import numpy as np
from ase.io.xsf import read_xsf

from postopus.files.file import File
from postopus.files.utils.units import get_units


class XCrySDenFile(File):
    EXTENSIONS = ["xsf"]

    def __init__(self, filepath: pathlib.Path):
        """
        Enable Postopus to read data, stored in xcrysen files

        Parameters
        ----------
        filepath : pathlib.Path
            path to the file in xcrysden format

        """
        self.filepath = filepath

    def _get_coords(self) -> Dict[str, numpy.ndarray]:
        """
        Get coords.

        Coords is analogous to xarray.Dataset.coords

        This code should handle one, two or three dimensions.
        Nonetheless, the current version of read_xsf only handles
        three dimensions.

        Returns
        -------
        Dict[str, numpy.ndarray]
            Dictionary with one key-value pair for each dimension.
            The key is the dimension name. The value represents the domain
            of the dimension. It starts at the origin and goes, in evenly
            spaced steps, until the length of the span vector of this dimension.

        """
        coords = {
            self.dims[dim]: np.linspace(
                self._origin[dim],
                self._origin[dim] + self._span_vectors[dim][dim],
                self._values.shape[dim],
            )
            for dim in range(len(self._dims))
        }
        return coords

    def _get_dims(self) -> Tuple[str]:
        # TODO: What if the dimensions are not x, y, z
        """
        Returns the dimension names in a tuple.

        This can only handle the cases where the coordinates are
         "x", "y", "z" (3D case)

        A case like "x", "z", "y" is not covered, right now.

        Returns
        -------
        Tuple[str]
            A tuple with the name of each dimension.

        """
        dim_names = ["x", "y", "z"]
        return tuple(dim_names[: len(self._origin)])

    def _readfile(self):
        """Sets up internal variables."""
        with open(self.filepath) as file_obj:
            try:
                self._values, self._origin, self._span_vectors, _ = read_xsf(
                    file_obj, index=-1, read_data=True
                )
            except AssertionError as ae:
                raise AssertionError(
                    "xcrysden per se supports 2D and 3D data. "
                    "Nonetheless, right now, the ase module only supports "
                    "the reading of 3D data. See iread_xsf() in "
                    "https://gitlab.com/ase/ase/-/blob/master/ase/io/xsf.py."
                ) from ae

            self._dims = self._get_dims()
            self._coords = self._get_coords()
            self._units = get_units(self.filepath)
