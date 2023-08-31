import os
import pathlib
from collections import namedtuple
from pathlib import Path
from typing import Dict, List, Tuple, Union

from postopus.datacontainers.field import ScalarField
from postopus.octopus_inp_parser.inpparse import Parser


class OutputCollector:
    def __init__(self, rootpath: pathlib.Path) -> None:
        """
        Will search for all output of Octopus in the given path. Finds system names,
        calculation modes and written fields.

        Parameters
        ----------
        rootpath : pathlib.Path
            path to the Octopus output containing inp file.

        """
        self.rootpath = Path(rootpath)

        # 'inp' will exists, as this was checked in postopus.octopus_run.Run
        self._config = Parser(self.rootpath / "inp")

        # get all directories and subdirectories
        # do this once here to reduce required IO. We make this a list, as an iterator
        # only could be used once for iteration.
        self._walkedlist = list(os.walk(rootpath))

        self._filesystem_systems = self.find_systems()
        self.output = {}
        for system in self._filesystem_systems:
            self.output[system] = self.find_iterations(system)
            fields, extensions = self.find_fields_and_extensions(system)
            for mode in fields:
                self.output[system][mode]["fields"] = fields[mode]
                self.output[system][mode]["extensions"] = extensions[mode]

    def find_systems(self) -> List[str]:
        """Find all systems present in the output.

        Returns
        -------
        List[str]
            list with all systems in the output.

        """
        systems_in_conf = self._config.systems.keys()
        systems_in_FS = []
        for system in systems_in_conf:
            # compatible with single and multisystems
            if Path(self.rootpath, *system.split(".")).is_dir() or system == "default":
                systems_in_FS.append(system)
        return systems_in_FS

    def find_iterations(
        self, system: str
    ) -> Dict[str, Dict[str, Union[List[pathlib.Path], Tuple[str, List[str]]]]]:
        """Find available iterations per calculation mode for a system.

        Parameters
        ----------
        system : str
            Name of the system, for which iterations shall be found

        Returns
        -------
        Dict[str, Dict[str, Union[List[pathlib.Path], Tuple[str, List[str]]]]]
            dict in dict, outer dict has calculation modes as keys, every
            calculation mode dict has a dict with tuples
            (iteration number, files list) as values and key "iterations". Also
            looks for data in folders "static" and "td.general".
        Notes
        -----
        Iterations namedtuples have the following form:
        >> Iterations(iteration_number='0000021',
         fields=['current-z', 'current-x', 'density', 'current-y'],
          extensions=['ncdf'])

        """
        subdir = "output_iter"
        if system == "default":
            system_path = str(self.rootpath / subdir)
        else:
            # compatible with single and multisystems
            system_path = str(Path(self.rootpath, *system.split("."), subdir))

        ##########
        # Find all calculation modes present in the output
        # Also, find all iteration numbers for these
        ##########
        modes = {}
        for roots, folders, files in self._walkedlist:
            if system_path == roots:
                for iter in folders:
                    calcmode = iter.split(".")[0]
                    iternum = iter.split(".")[1]
                    # add entry to modes dict. If calculation mode ('scf', 'td',
                    # ...) did
                    # not yet exist, add it, init iteration list
                    modes.update({calcmode: modes.get(calcmode, [])})
                    # add found iteration number
                    modes[calcmode].append(iternum)

        ##########
        # Find all output files. We need a list of all outputs from every calculation
        # mode.
        ##########
        outputs = {}
        for roots, folders, files in self._walkedlist:
            if system_path in roots:
                foldername = Path(roots).name
                try:
                    calcmode = foldername.split(".")[0]
                    iternum = foldername.split(".")[1]
                except IndexError:
                    # non-output directory
                    continue
                if calcmode not in outputs:
                    outputs.update(
                        {calcmode: {"iterations": outputs.get(calcmode, [])}}
                    )
                outputs[calcmode]["iterations"].append((iternum, files))

            # Need to create calculation modes if non-output_iter folders like
            # "static" or "td.general" are found
            if "static" in roots:
                calcmode = "scf"
                if calcmode not in outputs:
                    outputs.update({calcmode: {"iterations": []}})

            if "td.general" in roots:
                calcmode = "td"
                if calcmode not in outputs:
                    outputs.update({calcmode: {"iterations": []}})

        # clean up. remove file extensions and duplicate outputs (e. g. same field in
        # different formats)
        for mode in outputs:
            for idx, iter in enumerate(outputs[mode]["iterations"]):
                # TODO: right now, we are not making use of the extensions,
                #  might come handy in the future
                Iterations = namedtuple(
                    "Iterations", "iteration_number fields extensions"
                )
                fields = list(set([file.split(".")[0] for file in iter[1]]))
                extensions = list(
                    set(
                        [
                            file.split(".")[1]
                            for file in iter[1]
                            if file.split(".")[1] not in ScalarField.NON_FIELD_SOURCES
                        ]
                    )
                )
                outputs[mode]["iterations"][idx] = Iterations(
                    iter[0], fields, sorted(extensions)
                )

        # Find extra data from folders "static", "td.general", ...
        special_data = self.find_special_data(system, list(outputs.keys()))
        # we need to add data found in "static"/"td.general" to the other found data
        for mode in special_data:
            for data in special_data[mode]:
                if data == "iterations":
                    # ignore the iterations key here
                    continue
                # this adds the keys "static"/"tdgeneral" to the found data. The keys
                # then are used in CalculationModes to build the special outputs
                # like "convergence", "forces", "maxwell_energy", ...
                outputs[mode][data] = special_data[mode][data]
                # if the outputs dict contains no iterations for a mode, then no
                # iterations were written to "output_iter", but a folder "static" or
                # "td.general" exists. We now have to add the fields (with no iteration
                # number -> '') to outputs, so that the field later normally can be
                # loaded by calling "get()" with no params. If iterations already
                # exists, this will work automatically, as "get()" in Fields would load
                # the correct data
                if outputs[mode]["iterations"] == []:
                    outputs[mode]["iterations"] = special_data[mode]["iterations"]
        return outputs

    def find_special_data(
        self, system: str, modes: List[str]
    ) -> Dict[str, Union[List[pathlib.Path], Tuple[str, List[str]]]]:
        """Find extra data stored outside of "output_iter". Searches folders
        "static"/"td.general"/... depending on calculation mode.

        Parameters
        ----------
        system : str
            inspected system
        modes : List[str]
            list of all calculation modes for the given system

        Returns
        -------
        Dict[str, Union[List[pathlib.Path], Tuple[str, List[str]]]]
            Expanded outputs dict with more information on data from folders
            "static" and "td.general".

        """
        result = {}
        # search for special outputs which can be found in folders "static" and
        # "td.general"
        for mode in modes:
            if mode == "scf":
                searchpath = self.rootpath / "static"
                setkey = "static"
            if mode == "td":
                # need to adjust path to system if no system exists
                sysname_in_path = ""
                if system != "default":
                    sysname_in_path = system
                searchpath = Path(
                    self.rootpath,
                    # compatible with single and multisystems
                    *sysname_in_path.split("."),
                    "td.general"
                )
                setkey = "tdgeneral"

            try:
                # need to check the folder 'static' on the same level as 'inp'
                # for files without suffix.
                # use a list comprehension here, as regex is hard for this. Store
                # complete paths.
                files = [
                    fil for fil in searchpath.iterdir() if "." not in str(fil.name)
                ]
                result[mode] = {}
                result[mode][setkey] = files

                Iterations = namedtuple(
                    "Iterations", "iteration_number fields extensions"
                )

                # build a list with all fields in the "static" folder.
                fields = list(
                    {fil.stem for fil in searchpath.iterdir() if "." in str(fil.name)}
                )

                extensions = list(
                    {
                        fil.suffix[1:]
                        for fil in searchpath.iterdir()
                        if "." in str(fil.name)
                        and fil.suffix[1:] not in ScalarField.NON_FIELD_SOURCES
                    }
                )
                iterations = Iterations("", fields, sorted(extensions))

                # these fields have no iteration number, therefore use ''
                result[mode]["iterations"] = [iterations]

            except FileNotFoundError:
                # No static directory.
                pass
        return result

    def find_fields_and_extensions(self, system: str) -> Dict[str, List[str]]:
        """
        Build a list of all fields and extensions present across all iterations for
        a calculation mode.

        Parameters
        ----------
        system : str
            Name of the system to look for fields

        Returns
        -------
        Dict[str, List[str]]
            all fields per calculation mode per system

        """
        fields_dict = {}
        extensions_dict = {}

        for mode in self.output[system]:
            fields = []
            extensions = []
            for it in self.output[system][mode]["iterations"]:
                if it == "":
                    # we have no iterations for this field, only "static"/"td.general"
                    continue

                fields.extend(field for field in it.fields if field not in fields)
                extensions.extend(ext for ext in it.extensions if ext not in extensions)

            fields_dict[mode] = fields
            extensions_dict[mode] = extensions

        return fields_dict, extensions_dict
