import pathlib
import sys
import warnings
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import xarray

from postopus.datacontainers.util.convenience_dict import ConvenienceDict
from postopus.datacontainers.util.special_characters import handle_fields_special_chars
from postopus.files import extension_loader_map, openfile
from postopus.files.vtk import VTKFile
from postopus.namespace_utils import build_namespaces
from postopus.utils import check_avail_memory, humanise_size, parser_log_retrieve_value


class ScalarField:
    NON_FIELD_SOURCES = ["xyz"]

    def __init__(
        self,
        ftype: str,
        path: pathlib.Path,
        systemname: str,
        calculationmode: str,
        fields_in_mode: Dict[
            str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
        ],
    ) -> None:
        """
        Class represents a scalar field. Will find all the iterations where this field
        is written out and provides methods to load data.

        Parameters
        ----------
        ftype : str
            type of field stored in the object. Name of the field equals the
            name of the file written by Octopus (without file suffix and
            dimension of the vector "-[xyz]").
        path : pathlib.Path
            /path/to/octopus/output (containing inp)
        systemname : str
            Name of the system containing this field
        calculationmode : str
            CalculationMode value of the run that wrote this field
        fields_in_mode : Dict[
                            str, Union[
                                Tuple[str, List[str]], List[pathlib.Path], List[str]
                            ]
                         ]
            All information on this field, as found in OutputCollector.

        """
        self.ftype = ftype
        self._path = path
        self._calculationmode = calculationmode
        self._systemname = systemname

        self._filename = self.ftype

        # count iterations, where we can find an output file containing this
        # field (method from super)
        iterations_store = [
            iter
            for iter, fields, extensions in fields_in_mode["iterations"]
            if self.ftype in fields
        ]
        # iterations_store could be empty, when only 'static' or 'td.general' exists,
        # but no actual content in output_iter
        if iterations_store != [""]:
            self.iteration_ids = tuple(sorted([int(i) for i in iterations_store]))
        else:
            self.iteration_ids = tuple()
        self.n_iterations = len(self.iteration_ids)
        # try because there might be no output_iter, only "static" or "td.general"
        try:
            self.digits_in_iter_id = len(iterations_store[0])
        except IndexError:
            self.digits_in_iter_id = 0

        # CalculationMode 'gs' in Octopus writes the final results to the 'static'
        # folder on the same level as 'inp'
        # TODO: This will change in the future, 'static' will be in system folders
        if calculationmode == "scf":
            try:
                self._static_avail = not fields_in_mode["static"] == []
            except KeyError:
                # happens if no folder "static" exists
                self._static_avail = False
            if self._static_avail:
                # if we have static data we need to add it as a dedicated iteration
                # in self.iterations, otherwise loading with get is impossible.
                step_size = np.diff(self.iteration_ids)
                if len(set(step_size)) == 1:
                    # all steps are equidistant, we can simply add a new step
                    # parse it from a np.int64 to python int
                    static_iter_num = self.iteration_ids[-1] + int(step_size[0])
                else:
                    if (
                        parser_log_retrieve_value(
                            self._path / "exec" / "parser.log",
                            "OutputDuringSCF",
                            conversion=int,
                        )
                        == 1
                    ):
                        # not all steps are spaced apart the same distance. Inform
                        # the user
                        warnings.warn(
                            "Your scf data might have missing simulation steps. "
                            "Distance between all steps is not consistent. Still "
                            "loading your data. The converged field will have 'step = "
                            "number_of_last_found_step + 1'.",
                            UserWarning,
                        )
                    try:
                        static_iter_num = self.iteration_ids[-1] + 1
                    except IndexError:
                        # this happens when no iterations are in self.iteration_ids,
                        # e. g. with benzene example.
                        # Just add iteration '1', good enough.
                        static_iter_num = 1
                # set new values for self.iteration_ids and self.n_iterations
                tmp_iters = list(self.iteration_ids)
                tmp_iters.append(static_iter_num)
                self.iteration_ids = tuple(tmp_iters)
                self.n_iterations = len(self.iteration_ids)
        else:
            # check if all outputs are there or if we are missing a step in the data
            step_size = np.diff(self.iteration_ids)
            if len(set(step_size)) != 1:
                warnings.warn(
                    "Your data might have missing simulation steps. Distance "
                    "between all steps is not consistent. Still loading "
                    "your data."
                )
            self._static_avail = None

    def _get_steps(self, steps: Union[str, int, List[int], None]) -> List[int]:
        """
        Get steps to be loaded.

        Parameters
        ----------
        steps steps input from the user

        Returns
        -------
        The corresponding iteration(s)

        """
        # step not provided and static data does not exist
        if steps is None and self._static_avail is False:
            # CalculationMode is 'gs', but there is no static data available
            # (maybe deleted or moved?)
            raise ValueError(
                "There is no static data available, please provide "
                "a value for iter_index."
            )

        # calculationmode is not 'scf' (results in self._static_avail = None)
        # and step was not provided
        if steps is None and self._static_avail is None:
            # raised, if step is not filled and CalculationMode is not 'gs'
            raise ValueError(
                "Please provide a value for iter_index! Only not required "
                "if CalculationMode is 'gs'."
            )

        # (step not provided and static data exists) or (static iteration number was
        #                                                provided)
        if (steps is None and self._static_avail is True) or (
            steps == self.iteration_ids[-1] and self._static_avail is True
        ):
            steps = [self.iteration_ids[-1]]  # in case it was None

        if steps == "all":
            steps = self.iteration_ids
        if isinstance(steps, int):
            steps = [steps]

        self._check_steps_exist(steps)
        return steps

    def _get_xarray_from_steps(
        self, load_steps: List[int], source: str = "auto", ignore_warnings: bool = False
    ):
        """
        Get an xarray from the specified steps (from a specified source).

        The time coordinate values are converted to a natural/physical time by
        multiplying the step number with the magnitude of one timestep.

        Parameters
        ----------
        load_steps : List[int]
            List of simulation steps to load for this field
        source : str
            file suffix of the file to load (Default value = "auto")
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Field for all chosen iteration in an Xarray.DataArray

        Notes
        -----
        The first time step is loaded spearately to get the shape of the final np.array.
        With this information we can initialize the empty placeholder.
        This is for saving memory. Using xarray.concat() would be memory inefficient.

        """
        file0 = self._load_file(load_steps[0], source)

        if not ignore_warnings:
            self._check_required_memory(load_steps, file0)

        arrs = np.empty(
            shape=(len(load_steps), *file0.values.shape), dtype=file0.values.dtype
        )
        arrs[0] = file0.values

        if len(load_steps) > 1:
            for indx, iter in enumerate(load_steps[1:]):
                fileobj = self._load_file(iter, source)
                arrs[indx + 1] = fileobj.values  # +1, because file0 already loaded
        else:
            fileobj = file0

        possible_namespaces = build_namespaces(self._systemname)
        calc_mode_steps, name_step_coord = self._get_xarray_steps_label(
            possible_namespaces, load_steps
        )

        fileobj._coords = {name_step_coord: np.array(calc_mode_steps), **file0.coords}
        fileobj._dims = (name_step_coord, *file0.dims)
        fileobj._values = arrs

        return fileobj.xarray()

    def _load_file(self, step: int, source: str) -> Any:
        """
        Build the path for a file and loads it using Postopus' openfile.

        Parameters
        ----------
        step : int
            simulation step number
        source : str
            filetype

        Returns
        -------
        Any
            file object from module `postopus.files`

        """
        if (
            step == self.iteration_ids[-1]
            and self._calculationmode == "scf"
            and self._static_avail
        ):
            # this iter is the converged iteration. It is not stored in
            # 'output_iter', but in 'static'!
            # TODO: This path will change, when Octopus moves output of static into
            #  the systems themselves
            path_without_source = pathlib.Path(
                self._path,
                "static",
                self._filename,
            )
        else:
            # Build the path to the file containing the field from predetermined
            # values. Compatible with single and multisystems.
            sysname_in_path = ""
            if self._systemname != "default":
                sysname_in_path = self._systemname.split(".")

            path_without_source = pathlib.Path(
                self._path,
                *sysname_in_path,
                "output_iter",
                self._calculationmode + "." + str(step).zfill(self.digits_in_iter_id),
                self._filename,
            )
        if self._filename.endswith(("-x", "-y", "-z")) and any(
            source in vtk_source for vtk_source in VTKFile.EXTENSIONS
        ):
            raise ValueError(
                "We don't support the syntax 'vector_field.dim.get()' for vtk files.\n"
                "Instead, use 'vector_field.get()' to get the vector field xarray.\n"
                "Then you can access the components with '.sel(component=dim)'.\n"
                "For example, instead of 'run.default.td.current.x.get(15, 'vtk')',\n"
                "use 'run.default.td.current.get(15, 'vtk')."
            )
        avail_sources = self._get_available_sources(path_without_source)
        if source == "auto":
            source = self._get_auto_source(avail_sources, path_without_source)
        self._check_if_source_exist(source, avail_sources, path_without_source)

        source = "." + source
        filepath = path_without_source.with_suffix(source)
        return openfile(filepath)

    def _get_auto_source(
        self, avail_sources: List[str], path_without_source: str
    ) -> str:
        """
        Gets automatic source.

        If there is only one available source,this is selected as the
        automatic source. Otherwise prints out the available sources for the user.


        Parameters
        ----------
        path_without_source path to the field without the source.

        Returns
        -------
        Either a unique source or a ValueError.

        """

        if len(avail_sources) == 1:
            return avail_sources[0]
        else:
            raise ValueError(
                "There is more than one available source for the selected file:  \n"
                f"{path_without_source}.  \n"
                "You need to add the parameter source=... to the function call.  \n"
                f"Following available sources were found: {avail_sources}"
            )

    def _get_available_sources(self, path_without_source: pathlib.Path) -> List[str]:
        """
        Get available sources for the requested path (field)

        Parameters
        ----------
        path_without_source path to the field, without the extension

        Returns
        -------
        avail_sources list of available sources for this field.

        """
        avail_sources = [
            path.suffix[1:]  # without dot
            for path in path_without_source.parent.iterdir()
            if path_without_source.stem in str(path)
            and path.suffix[1:] not in self.NON_FIELD_SOURCES
        ]
        return avail_sources

    def get_all(
        self,
        source: str = "auto",
        ignore_warnings: bool = False,
    ) -> xarray.DataArray:
        """
        Load all available simulation steps (including the converged step)

        Also check if enough memory is available.

        Parameters
        ----------
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.
        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step" or "t" (if
            time dependent) for selecting the simulation steps.

        Examples
        --------
        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir / "benzene")
        >>> run.default.scf.density.get_all(source="xsf")
        >>> <xarray.DataArray...

        """
        return self._get_xarray_from_steps(
            self._get_steps("all"), source, ignore_warnings
        )

    def get_converged(
        self,
        source: str = "auto",
        ignore_warnings: bool = False,
    ) -> xarray.DataArray:
        """
        Get converged scf iteration

        Parameters
        ----------
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step" or "t" (if
            time dependent) for selecting
            the simulation steps.

        Examples
        --------
        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir)
        >>> run.default.scf.density.get_converged(source="xsf")
        >>> <xarray.DataArray...

        """
        return self._get_xarray_from_steps(
            self._get_steps(None), source, ignore_warnings
        )

    def get(
        self,
        steps: Union[int, List[int]] = None,
        source: str = "auto",
        ignore_warnings: bool = False,
    ) -> xarray.DataArray:
        """
        Method used to load data for a field. Fields can be loaded for one or multiple
        simulation steps.

        Parameters
        ----------
        steps : Union[int, List[int]]
            Which simulation steps to load. Either a single step, a list of steps.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step"or "t" (if
            time dependent) for selecting
            the simulation steps.

        Examples
        --------
        Single iteration:

        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir)
        >>> run.default.scf.density.get(steps=1, source="xsf")
        >>> <xarray.DataArray...

        List of iterations:

        >>> run.default.scf.density.get(steps=[1, 2], source="xsf")
        >>> <xarray.DataArray...

        """
        if isinstance(steps, int) or (
            isinstance(steps, list) and all(isinstance(step, int) for step in steps)
        ):
            return self._get_xarray_from_steps(
                self._get_steps(steps), source, ignore_warnings
            )
        else:
            raise TypeError(
                "steps parameter needs to be provided. It needs to be either an integer"
                " or a list of integers. \n   Hint: You can also make use of"
                " get_all(),"
                " get_converged(),"
                " or iget()."
            )

    def iget(
        self,
        indices: Union[int, List[int], slice] = None,
        source: str = "auto",
        ignore_warnings: bool = False,
    ):
        """
        Method used to load data for a field. Fields can be loaded for one or multiple
        simulation steps. The selection is done by index.

        Parameters
        ----------
        indices: Union[int, List[int], slice]
            Which simulation steps to load, by index. Either a single index,
            a list of indices or a slice(int, int) object. Negative integers are also
            allowed.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step"or "t" (if
            time dependent) for selecting
            the simulation steps.

        Examples
        --------
        Single iteration:

        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir)
        >>> run.default.scf.density.iget(-1, source="xsf")
        >>> <xarray.DataArray...

        List of iterations:

        >>> run.default.scf.density.iget([5, 7], "ncdf")
        >>> <xarray.DataArray...  # two iterations

        Slice:

        >>> run.default.scf.density.iget(slice(0, 3), "ncdf")
        >>> <xarray.DataArray...  # three iterations


        """
        if isinstance(indices, int):
            selected_indices = [self.iteration_ids[indices]]
        elif isinstance(indices, slice):
            selected_indices = list(self.iteration_ids[indices])
        elif isinstance(indices, list) and all(
            isinstance(index, int) for index in indices
        ):
            selected_indices = [self.iteration_ids[index] for index in indices]
        else:
            raise TypeError(
                "indices parameter needs to be provided. It needs to be either an"
                " integer, a list of integers, or a slice(int, int) object.\n"
                " Negative integers are allowed. \n"
                " Hint: You can also make use of"
                " get_all(),"
                " get_converged(),"
                " or get()."
            )
        return self._get_xarray_from_steps(
            self._get_steps(selected_indices), source, ignore_warnings
        )

    def _check_required_memory(self, load_steps: List[int], single_file: Any):
        """
        Check if data fits into available memory

        Calculating required size of memory by checking size of the field for a single
        iteration and multiplying by the number of steps to load.
        If required memory exceeds available memory, proactively raise a MemoryError.
        This MemoryError can be ignored by providing `ignore_warnings` to get()

        Parameters
        ----------
        load_steps : List[int]
            List of all simulation steps that shall be loaded
        single_file :
            Data of one iteration. The data type will correspond to the parser used for
            reading this file. This will be given by the "source" parameter that the
            user gives to the corresponding get() method.

        Returns
        -------
        None
            Raises a MemoryError if things go south and the user wants to allocate to
            much memory - but will not return anything per se.

        Notes
        -----
        Total size = size of values + size of list of dims + size of coords np.arrays
        this is not 100% on point (would need recursive summation, e. g. every string
        in single_file.dims + single_file.dims size, which is a list), but it gets the
        larger chunks
        """

        size_in_mem = (
            single_file.values.nbytes
            + sys.getsizeof(single_file.dims)
            + sum([arr.nbytes for arr in single_file.coords.values()])
        )

        if not check_avail_memory(size_in_mem * len(load_steps)):
            tot_size = humanise_size(size_in_mem * len(load_steps))
            raise MemoryError(
                f"You are trying to load (approx.) {tot_size[0]} {tot_size[1]}!"
                f"Your system has less memory available than this. You "
                f"have been warned - but if you still want to try, set the "
                f"'ignore_warnings' parameter to True (worst case: your program will"
                f"crash. Best case: might work :) )."
            )

    def _check_if_source_exist(
        self, source: str, avail_sources: List[str], path_without_source: pathlib.Path
    ) -> None:
        """
        Check if source exist for the current file.
        Parameters
        ----------
        source:
            selected source
        avail_sources:
            Found field-sources associated with the requested field


        Returns
        -------

        """
        field_sources_with_parser = [
            extension
            for extension in extension_loader_map.keys()
            if extension not in self.NON_FIELD_SOURCES
        ]
        found_sources_and_parsers = (
            f" Found sources: \n "
            f"{avail_sources}.\n"
            f"Field extensions for which we have a parser:\n"
            f"{field_sources_with_parser}."
        )

        # TODO: Edit the error message when parsing xyz files becomes possible
        if source in self.NON_FIELD_SOURCES:
            raise ValueError(f"{source} is not a known field source.")

        if (source in avail_sources) and (source not in field_sources_with_parser):
            raise NotImplementedError(
                f"Existing file {path_without_source}.{source}\n"
                f" found, but we don't have a parser for it."
                f" Contact us if you need it! \n"
                f"{found_sources_and_parsers}"
            )

        if (source not in avail_sources) and (source in field_sources_with_parser):
            raise ValueError(
                f"File does not exist: {path_without_source}.{source} .\n"
                f"Available sources: \n"
                f"{avail_sources}"
            )

        if (source not in avail_sources) and (source not in field_sources_with_parser):
            raise ValueError(
                f"We did not find {path_without_source}.{source} \n"
                f", nor do we have a parser for it. Maybe a typo? \n"
                f"{found_sources_and_parsers}"
            )

    def _check_steps_exist(self, load_steps: List[int]):
        """
        Checks if the provided list of steps exists in the output of the Octopus output.

        Parameters
        ----------
        load_steps : List[int]
            List of steps which shall be loaded

        """
        for step in load_steps:
            # Check if data exists for the requested iteration
            if step not in self.iteration_ids:
                raise ValueError(
                    f"Requested iteration '{step}' does not exist for '{self.ftype}'."
                )

    def _get_xarray_steps_label(self, namespaces: List[str], load_steps: List[int]):
        """
        Get the step label (coord values + dim name) for the xarray

        The iteration/step dimension depends on the calculation mode that we are
        dealing with. For example, in the calculation mode "td" we have an actual time
        dimension, whereas in the "scf" mode we are just dealing with optimization
        steps and we don't have any physical time, so we would return the load_step
        unchanged.

        For the td mode we retrieve the TDTimeStep value from the parser log file.
        The searching routine tries all the possible namespaces for finding it.
        Parameters
        ----------
        namespaces: All possible namespaces given the present systemname. Only used for
        td calculation mode.
        load_steps: Loading steps as in filesystem structure

        Returns
        -------
        - steps (coordinate values) intrinsic to the calculation mode that we are
         dealing with
        - the name of the intrinsic step variable (dimension name)

        """
        path_to_parser_log_file = pathlib.Path(f"{self._path}/exec/parser.log")
        if self._calculationmode == "td":
            try:
                sysname = namespaces[-1]
                namespaces.pop(-1)
                timestep_key = f"{sysname}.TDTimeStep"
                timestep = parser_log_retrieve_value(
                    path_to_parser_log_file, timestep_key, conversion=float
                )
            except ValueError:
                if namespaces:
                    # TODO: Not yet tested, we don't have examples
                    self._get_xarray_steps_label(namespaces, load_steps)
                else:
                    timestep = parser_log_retrieve_value(
                        path_to_parser_log_file, "TDTimeStep", conversion=float
                    )
            load_time_steps = [load_step * timestep for load_step in load_steps]
            return load_time_steps, "t"
        else:
            # TODO: Not yet tested, we don't have examples
            if self._calculationmode != "scf":
                warnings.warn(
                    f"We don't have any practical experience with "
                    f"{self._calculationmode} calculation modes. We are assuming that "
                    f"no "
                    f"physical units are associated with "
                    f"the iteration/step dimension. "
                    f"So we will just call it 'step' and it will just consist"
                    f" of a list of integers, imitating"
                    f" the filesystem's structure."
                )
            return load_steps, "step"


class VectorField(ConvenienceDict):
    __dict_name__ = "components"

    def __init__(
        self,
        ftype: str,
        path: pathlib.Path,
        systemname: str,
        calculationmode: str,
        fields_in_mode: Dict[
            str,
            Union[Tuple[str, List[str]], List[pathlib.Path], List[str]],
        ],
    ) -> None:
        """
        Vectorfields in Octopus are written out in three separate files. Actual fields
        (field data and values) are contained in VectorFieldDim for every direction
        (x, y, z), this class provides access to these directions.

        Parameters
        ----------
        ftype : str
            type of field stored in the object (e. g. 'magnetic_field',
            'electric_field', ...). Naming from Octopus' input file 'inp'.
        path : pathlib.Path
            /path/to/output_iter  or  /path/to/System_name_in_inp
        systemname : str
            Name of the system containing this field
        calculationmode : str
            CalculationMode value of the run that wrote this field
        fields_in_mode : Dict[
                            str, Union[
                                Tuple[str, List[str]], List[pathlib.Path], List[str]
                            ]
                         ]
            All information on this field, as found in OutputCollector

        """
        super().__init__()

        self.ftype = ftype
        self._path = path
        self._calculationmode = calculationmode
        self._systemname = systemname

        # Build the components out of ScalarFields, because they basically are just that
        self.components = {
            dim: ScalarField(
                handle_fields_special_chars(ftype) + "-" + dim,
                path,
                systemname,
                calculationmode,
                fields_in_mode,
            )
            for dim in "xyz"
        }

        x_iterations = self.components["x"].iteration_ids
        y_iterations = self.components["y"].iteration_ids
        z_iterations = self.components["z"].iteration_ids

        if not x_iterations == y_iterations or not y_iterations == z_iterations:
            msg = (
                f"Error: inconsistent number of files found for file_type {ftype}.\n"
                f"Please check for missing simulation steps!\n"
                f"Found components and steps:\n"
            )
            msg += self._output_iter_difference(
                x_iterations, y_iterations, z_iterations
            )
            raise FileNotFoundError(msg)

    def get_all(
        self,
        source: str = "auto",
        ignore_warnings: bool = False,
    ) -> xarray.DataArray:
        """
        Load all available simulation steps (including the converged step)

        Also check if enough memory is available.

        Parameters
        ----------
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.
        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step" or "t" (if
            time dependent) for selecting the simulation steps.
        Examples
        --------
        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir)
        >>> run.default.td.current.get_all(source="ncdf")
        >>> <xarray.DataArray...  # contains all 3 components + coordinate "t"

        """
        return self._get("all", source, ignore_warnings)

    def get(
        self,
        steps: Union[int, List[int]] = None,
        source: str = "auto",
        ignore_warnings: bool = False,
    ) -> xarray.DataArray:
        """
        Method used to load data for a field. Fields can be loaded for one or multiple
        simulation steps. As this method is related to VectorField it will load all
        components of the vector field

        Parameters
        ----------
        steps : Union[int, List[int]]
            Which simulation steps to load. Either a single step, a list of steps.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that too much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step" or "t" (if
            time dependent) for selecting
            the simulation steps.
        Examples
        --------
        Single iteration:

        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir)
        >>> run.default.td.current.get(steps=1, source="ncdf")
        >>> <xarray.DataArray...

        List of iterations:

        >>> run.default.td.current.get(steps=[1, 2], source="ncdf")
        >>> <xarray.DataArray...  # contains all 3 components + coordinate "t"

        """
        if isinstance(steps, int) or (
            isinstance(steps, list) and all(isinstance(step, int) for step in steps)
        ):
            return self._get(steps, source, ignore_warnings)
        else:
            raise TypeError(
                "steps parameter needs to be provided. It needs to be either an integer"
                " or a list of integers. \n   Hint: You can also make use of"
                " get_all(),"
                " or iget()."
            )

    def iget(
        self,
        indices: Union[int, List[int], slice] = None,
        source: str = "auto",
        ignore_warnings: bool = False,
    ):
        """
        Method used to load data for a field. Fields can be loaded for one or multiple
        simulation steps. The selection is done by index.

        Parameters
        ----------
        indices: Union[int, List[int], slice]
            Which simulation steps to load, by index. Either a single index,
            a list of indices or a slice(int, int) object. Negative integers are also
            allowed.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinate "step"or "t" (if
            time dependent) for selecting
            the simulation steps.

        Examples
        --------
        Single iteration:

        >>> from pathlib import Path; from postopus import Run
        >>> repodir = Path("path_to_repodir")
        >>> testdata_dir = repodir / "tests" / "data" / "methane"
        >>> run = Run(testdata_dir)
        >>> run.default.td.current.iget(-1, "ncdf")
        >>> <xarray.DataArray... # one iteration

        List of iterations:

        >>> run.default.td.current.iget([5, 7], "ncdf")
        >>> <xarray.DataArray...  # two iterations

        Slice:

        >>> run.default.td.current.iget(slice(0, 3), "ncdf")
        >>> <xarray.DataArray...  # three iterations






        """
        if isinstance(indices, int):
            return self._get(
                self.components["x"].iteration_ids[indices], source, ignore_warnings
            )
        elif isinstance(indices, slice):
            return self._get(
                list(self.components["x"].iteration_ids[indices]),
                source,
                ignore_warnings,
            )
        elif isinstance(indices, list) and all(
            isinstance(index, int) for index in indices
        ):
            selected_indices = [
                self.components["x"].iteration_ids[index] for index in indices
            ]
            return self._get(selected_indices, source, ignore_warnings)
        else:
            raise TypeError(
                "indices parameter needs to be provided. It needs to be either an"
                " integer (negative also allowed),"
                " a list of integers, or a slice(int, int) object. \n"
                " Hint: You can also make use of"
                " get_all(),"
                " get_converged(),"
                " or get()."
            )

    def _get(
        self,
        steps: Union[str, int, List[int]] = None,
        source: str = "auto",
        ignore_warnings: bool = False,
    ) -> xarray.DataArray:
        """
        Private Method used to load data for a field. Fields can be loaded for
        one or multiple
        simulation steps. As this method is related to VectorField it will load all
        components of the vector field

        Parameters
        ----------
        steps : Union[str, int, List[int]]
            Which simulation steps to load. Either a single step, a list of steps or
            string "all" to select all available. Providing no value for `steps` works
            with the "scf" calculation mode and will return converged fields.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinates "step" for
            selecting the simulation steps and "component" for the components of the
            vectors.

        """
        # Memory check START
        # Prepare list of iterations which shall be loaded
        if isinstance(steps, list):
            load_steps = steps
        elif steps == "all":
            load_steps = list(self.components["x"].iteration_ids)
        elif isinstance(steps, int):
            load_steps = [steps]

        self._check_steps_exist(load_steps)

        # special sources
        if source == "vtk":
            return self._get_vtk(load_steps, source, ignore_warnings)
        else:
            return self._get_standard(load_steps, source, ignore_warnings)

    def _output_iter_difference(self, x: List[int], y: List[int], z: List[int]) -> str:
        """
        Allows to build a table for the user to check, which simulation steps are
        missing. Setup for `build_dim_string`.

        Parameters
        ----------
        x : List[int]
            All steps found for component x
        y : List[int]
            All steps found for component y
        z : List[int]
            All steps found for component z

        Returns
        -------
        str
            Table style overview of all found steps per component with empty spaces
            when step is missing.
        """
        # get max number of step digits (assume two components are missing (value 0), so
        # we still find the correct value. If two are present, values also is correct
        digits = max(self.components[dim].digits_in_iter_id for dim in "xyz")
        all_iters = list(set(x + y + z))
        components_overview = "".join(
            self._build_dim_string(str_dim, dim, all_iters, digits)
            for (str_dim, dim) in zip("xyz", [x, y, z])
        )
        return components_overview

    def _build_dim_string(
        self, compname: str, dim: List[int], alliters: List[int], digits: int
    ) -> str:
        """
        Build and return a string that contains all the step IDs for a given component.
        If step is missing, whitespaces with the same width are added

        Parameters
        ----------
        compname : str
            Name of the component, used as prefix
        dim : List[int]
            List with all found steps for component `compname`
        alliters : List[int]
            List with all available steps between all components
        digits : int
            Number of characters that can be in the step's number (max)

        Returns
        -------
        str
            Line containing all simulation steps for this component and whitespaces,
            where a step is missing compared to other components.

        """
        # add component name
        res = f"{compname}: "
        for val in alliters:
            if val in dim:
                # add value
                res += f"{val},".rjust(digits + 2)
            else:
                # add whitespace
                res += "".rjust(digits + 2)
        # add newline
        res += "\n"
        return res

    def _check_steps_exist(self, load_steps):
        for step in load_steps:
            # Check if data exists for the requested iteration
            # __init__ guarantees components["x"].iteration_ids
            # == components["y"].iteration_ids == components["z"].iteration_ids
            if step not in self.components["x"].iteration_ids:
                raise ValueError(
                    f"Requested iteration '{step}' does not exist for '{self.ftype}'."
                )

    def _get_vtk(self, load_steps, source, ignore_warnings=False):
        """
        Get an xarray from vtk files for the given steps.

        Parameters
        ----------
        steps : List[int]
            Which simulation steps to load.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinates "step" for
            selecting the simulation steps and "component" for the components of the
            vectors. Xarray originates from a vtk source.
        """
        # We are arbitrarily selecting the x-component here. In vtk files
        # The whole vector field is stored in one file, and this is what we
        # need to read
        if self.components["x"]._filename.endswith(("-x", "-y", "-z")):
            self.components["x"]._filename = self.components["x"]._filename[:-2]
        file0 = self.components["x"]._get_xarray_from_steps(
            [load_steps[0]], source, ignore_warnings=ignore_warnings
        )

        if not ignore_warnings:
            self.components["x"]._check_required_memory(load_steps, file0)

        if len(load_steps) == 1:
            combined = file0
        else:
            n_steps = len(load_steps)
            combined_shape = (n_steps, *file0.shape[1:])
            combined_values = np.empty(combined_shape, dtype=file0.dtype)
            combined_values[0] = file0.values

            for i, step in enumerate(load_steps[1:], start=1):
                file_step = self.components["x"]._get_xarray_from_steps(
                    [step], source, ignore_warnings=ignore_warnings
                )
                combined_values[i] = file_step.values

            t_coord = np.array(load_steps, dtype=int)
            coords = {
                "component": file0.coords["component"],
                "t": (file0.dims[0], t_coord),
                "x": file0.coords["x"],
                "y": file0.coords["y"],
                "z": file0.coords["z"],
            }
            combined = xarray.DataArray(
                combined_values, coords=coords, dims=file0.dims, attrs=file0.attrs
            )

        reordered_xarray = combined.transpose("component", "t", "x", "y", "z")

        return xarray.DataArray(
            reordered_xarray.values,
            coords=reordered_xarray.coords,
            dims=reordered_xarray.dims,
            attrs=reordered_xarray.attrs,
        )

    def _load_component_data(
        self, component, load_steps, source, file0=None, ignore_warnings=False
    ):
        """
        Load field data for a single component.
        Parameters
        ----------
        component : str
            Which component to load.
        file0 : xarray.DataArray
            Xarray of the first step, if already given
        steps : List[int]
            Which simulation steps to load.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the one component of the  field,

        Notes
        -----
        Re-use checking of memory from a single field. From
        VectorField.__init__() we
        know all components exist in all steps. So we can check memory by
        trying if
        loading a ScalarField with all requested iterations would word and
        multiplying
        the number of steps by three, as we want to load this many steps for three
        total components.
        """
        #
        if file0 is None:
            file0 = self.components[component]._get_xarray_from_steps(
                [load_steps[0]], source, ignore_warnings=ignore_warnings
            )

        if len(load_steps) == 1:
            return file0

        file1toN = self.components[component]._get_xarray_from_steps(
            load_steps[1:], source, ignore_warnings=ignore_warnings
        )

        data_array = np.empty(
            shape=(len(load_steps), *file0.squeeze().values.shape),
            dtype=file0.values.dtype,
        )

        data_array[0] = file0.values
        data_array[1:] = file1toN.values

        coords = {
            file1toN.dims[0]: np.concatenate(
                (
                    file0.coords[file1toN.dims[0]].values,
                    file1toN.coords[file1toN.dims[0]].values,
                )
            ),
            **file0.squeeze(drop=True).coords,
        }

        combined = xarray.DataArray(
            data_array,
            coords=coords,
            dims=file0.dims,
            name=file0.name,
            attrs={"units": file0.units},
        )

        combined[file1toN.dims[0]].attrs = {
            "units": file1toN.coords[file1toN.dims[0]].units
        }

        return combined

    def _get_standard(self, load_steps, source, ignore_warnings=False):
        """
        Load field data for the standard case, i.e. not an especial extension like vtk.

        Parameters
        ----------
        steps : Union[str, int, List[int]]
            Which simulation steps to load. Either a single step, a list of steps or
            string "all" to select all available. Providing no value for `steps` works
            with the "scf" calculation mode and will return converged fields.
        source : str
            Target output format for the field. E. g. "z=0", "cube", "vtk", ...
        ignore_warnings : bool
            Choose whether to ignore warnings that to much memory might be used when
            loading.

        Returns
        -------
        xarray.DataArray
            Xarray contains the field, and an additional coordinates "step" for
            selecting the simulation steps and "component" for the components of the
            vectors.
        """
        dimnames = ["x", "y", "z"]

        # Check memory requirements for all components
        file0compx = self.components["x"]._get_xarray_from_steps(
            [load_steps[0]], source, ignore_warnings=ignore_warnings
        )
        if not ignore_warnings:
            self.components["x"]._check_required_memory(load_steps * 3, file0compx)

        # Load data for each component
        data_arrays = [
            self._load_component_data(
                component,
                load_steps,
                source,
                file0=file0compx if component == "x" else None,
                ignore_warnings=ignore_warnings,
            )
            for component in dimnames
        ]

        # Combine data arrays into a single array for the whole vector field
        varray = np.stack(data_arrays)

        coords = {"component": dimnames, **data_arrays[0].coords}
        dims = ("component", *data_arrays[0].dims)

        return xarray.DataArray(
            varray,
            coords=coords,
            dims=dims,
            name=data_arrays[0].name[:-2],  # remove the "-x" from name
            attrs={"units": data_arrays[0].units},
        )


class TDGeneralVectorField(ConvenienceDict):

    __dict_name__ = "dimensions"

    # TODO: CHANGE Doc and test functionality

    def __init__(self, vfield_name: str, fields_in_td_general: List[pathlib.Path]):
        """
         A class for holding the tdgeneral vector fields data.

         It groups all the dimensions of a tdgeneral vector field into one object,
         through a ConvenienceDict.

        Each of the dimensions will hold a pandas DataFrame.

        Parameters
        ----------
        vfield_name: str
         Name of the tdgeneral vector field.
        fields_in_td_general: List[pathlib.Path]
            paths to all the files stored in tdgeneral.
        """
        super().__init__()
        for vfield_comp in fields_in_td_general:
            if vfield_comp.name[:-2] == vfield_name:
                dim = vfield_comp.name[-1]
                _fileobj = openfile(vfield_comp)
                self.dimensions[dim] = _fileobj.values
                # Adding units attribute, NOT a column of the dataframe.
                self.dimensions[dim].attrs = _fileobj.attrs
