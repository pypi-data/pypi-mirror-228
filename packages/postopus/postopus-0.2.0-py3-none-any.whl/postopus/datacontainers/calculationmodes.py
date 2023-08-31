import pathlib
from typing import Dict, List, Tuple, Union

import pandas as pd

from postopus.datacontainers.field import ScalarField, TDGeneralVectorField, VectorField
from postopus.datacontainers.util.convenience_dict import ConvenienceDict
from postopus.datacontainers.util.special_characters import handle_fields_special_chars
from postopus.files import openfile
from postopus.files.vtk import VTKFile


class CalculationModes(ConvenienceDict):
    # Set name of dict in ConvenienceDict
    __dict_name__ = "fields"

    def __init__(
        self,
        mode: str,
        fields_in_mode: Dict[
            str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
        ],
        systemdir: str,
        systemname: str,
    ) -> None:
        """
        Class that build a dict of all fields present in a system for a given
        CalculationMode output.

        Parameters
        ----------
        mode : str
            Name of the calculation mode in the output. Naming like in Octopus'
            output (e. g. 'td', 'scf', ...)
        fields_in_mode : dict
            fields contained in the given calculation mode for this system
        systemdir : pathlib.Path
            directory in the filesystem which contains the output (folder 'output_iter')
            for one of the simulated systems in a run with Octopus
        systemname : str
            Name of the system, as found in OutputCollector.

        """
        # Init system dict in super
        super().__init__()

        self.mode = mode
        self.systemdir = systemdir
        try:
            self._containingfields = fields_in_mode["fields"]
        except KeyError:
            # This happend, if we have a folder "static" or "td.general", but no fields
            # were written out to "output_iter". Example inp for this is benzene
            self._containingfields = []

        self.fields = {}
        for field in self._containingfields:
            # self.fields is available through ConvenienceDict
            fieldaccessor, is_vector_field = self._is_vector_field(
                field, fields_in_mode
            )

            # Only add the vector field as a whole and not each component separately
            if handle_fields_special_chars(fieldaccessor) in self.fields.keys():
                continue

            if is_vector_field:
                self.fields[handle_fields_special_chars(fieldaccessor)] = VectorField(
                    fieldaccessor,
                    systemdir,
                    systemname,
                    self.mode,
                    fields_in_mode,
                )

            # Scalar fields
            else:
                self.fields[handle_fields_special_chars(field)] = ScalarField(
                    field,
                    systemdir,
                    systemname,
                    self.mode,
                    fields_in_mode,
                )

        # Some CalculationModes have special outputs, e. g. 'gs' writes stuff like
        # 'info' or 'forces' into a folder 'static'.
        # 'td' produces a folder 'td.general' per system with outputs like 'laser',
        # or 'energy'. These files do not have an extension.
        # We use this for identification of such files.
        if mode == "scf":
            if "static" in fields_in_mode:
                self._static_fields(fields_in_mode)

        if mode == "td":
            if "tdgeneral" in fields_in_mode:
                self._tdgeneral_fields(fields_in_mode)

    def _static_fields(
        self,
        fields_in_mode: Dict[
            str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
        ],
    ):
        """
        Loads the fields of the static folder into self.fields

        Parameters
        ----------
        fields_in_mode : dict
            fields contained in the given calculation mode for this system

        Returns
        -------
        None
        """
        for sf in fields_in_mode["static"]:
            _fileobj = openfile(sf)
            self.fields[sf.name] = _fileobj.values
            if type(self.fields[sf.name]) == pd.DataFrame:
                self.fields[sf.name].attrs = _fileobj.attrs
        return None

    def _tdgeneral_fields(
        self,
        fields_in_mode: Dict[
            str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
        ],
    ):
        """
        Loads the fields of the td.general folder into self.fields

        Parameters
        ----------
        fields_in_mode : dict
            fields contained in the given calculation mode for this system

        Returns
        -------
        dict
            Dictionary with the fields in the td.general folder.
        """
        for tf in fields_in_mode["tdgeneral"]:
            # Vector fields in td.general
            # TODO: Probably also handle the vtk files differently?
            #  - Don't have any examples yet
            if tf.name.endswith(("_x", "_y", "_z")):
                vfield_name = tf.name[:-2]
                if vfield_name in self.fields:
                    continue
                self.fields[vfield_name] = TDGeneralVectorField(
                    vfield_name, fields_in_mode["tdgeneral"]
                )
            # Scalar fields in td.general
            else:
                _fileobj = openfile(tf)
                self.fields[tf.name] = _fileobj.values
                # Adding units attribute, NOT a column of the dataframe.
                self.fields[tf.name].attrs = _fileobj.attrs

    def _is_vector_field(
        self,
        field: str,
        fields_in_mode: Dict[
            str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
        ],
    ):
        """
        Check if a field is a vector field or not.

        Scalar fields are written to a single file, vector fields are usually stored in
        three files, consisting of the field name and a suffix '-x', '-y' or '-z'.
        Each of them representing a component.
        Although sometimes, like in the vtk case, all the vector components of a field
        are stored in a single file. In this cases it may be non-trivial to identify if
        a field is a vector field or a scalar field.

        So there are three possibilites for identifying a vector field:
        1. The field name ends with '-[xyz]'
        2. The field name doesn't end with '-[xyz]' but the field is present in multiple
         extensions in the data and at least one of them can be identified using the
         first rule.
        3. The field name doesn't end with '-[xyz]' and its extension stores the scalar
         fields and the vector fields in one single file. This is the non-trivial case.
         For this last case, the algorithm will vary depending on the extension. For
         example, in the vtk case one needs to read  the header of the file to identify
         if the field is a vector field or not.

        self.fields keys should only be the field names, for vector fields the
        suffix should be removed. Vector field orientation then is accessible
        via e. g. 'self.field_name.x' for the 'x' component. So that the fieldaccesor
        will always be the name of the field without the suffix.

        Parameters
        ----------
        field : str
            Name of the field
        fields_in_mode : Dict[
                str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]
            ]
            fields contained in the given calculation mode for this system

        Returns
        -------
        fieldaccessor : str
            Name of the field without the suffix
        is_vector_field : bool
            True if the field is a vector field, False otherwise
        """

        # the dashes are replaced by underscores, since they are a special char.
        dimension_keys = ("-x", "-y", "-z")
        # todo: Need an example folder with current only in vtk to test case 3

        def is_case_1(field: str) -> bool:
            return field.endswith(dimension_keys)

        def is_case_2(field: str) -> bool:
            return any(field + key in self._containingfields for key in dimension_keys)

        def is_case_3(field: str) -> bool:
            # vtk
            if any(ext in VTKFile.EXTENSIONS for ext in fields_in_mode["extensions"]):
                n_components = VTKFile.is_vector_field_vtk(
                    self.systemdir, self.mode, field
                )
                return n_components > 1
            return False

        if is_case_1(field):
            return field[:-2], True
        elif is_case_2(field):
            return field, True
        elif is_case_3(field):
            return field, True
        else:
            return field, False
