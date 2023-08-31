import pathlib
from typing import Dict, List, Tuple, Union

from postopus.datacontainers.calculationmodes import CalculationModes
from postopus.datacontainers.util.convenience_dict import ConvenienceDict


class System(ConvenienceDict):
    # Set name of dict in ConvenienceDict
    __dict_name__ = "system_data"

    def __init__(
        self,
        systemname: str,
        systempath: pathlib.Path,
        modes: List[str],
        mode_field_info: Dict[
            str, Dict[str, Union[Tuple[str, List[str]], List[pathlib.Path], List[str]]]
        ],
    ) -> None:
        """
        System class provides a dict with all found calculation modes written for the
        system.
        Parameters
        ----------
        systemname : str
            Name of this system
        systempath : pathlib.Path
            path to the Octopus output (not system folder)
        modes : List[str]
            calculation modes in this field
        mode_field_info : Dict[str, Dict[str, Union[Tuple[str, List[str]],
                                              List[pathlib.Path],
                                              List[str]]
                                        ]]
            fields in the calculation modes in this system
        """
        # Init system dict in super
        super().__init__()

        self.systemname = systemname
        self.path = systempath
        self.mode_field_info = mode_field_info

        for m in modes:
            # self.modes is available through ConvenienceDict
            self.system_data[m] = CalculationModes(
                m,
                mode_field_info[m],
                self.path,
                self.systemname,
            )
