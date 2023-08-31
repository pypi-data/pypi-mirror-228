from importlib import metadata

# TODO: Delete when ase is updated
try:
    import ase  # noqa: F401
except ModuleNotFoundError:
    raise RuntimeError(
        "Module ase is missing. Master branch of ase needs to be installed."
        " Please install it via \n"
        "pip install git+https://gitlab.com/ase/ase.git@master"
    )
else:
    from ._ase_compatibility import _ase_compatibility

    if not _ase_compatibility():
        raise RuntimeError(
            "Installed ase version is not compatible. "
            "Master branch of ase needs to be installed. Please install it via \n"
            "pip install git+https://gitlab.com/ase/ase.git@master"
        )
# TODO END delete when ase is updated

from postopus.octopus_nested_runs import nestedRuns  # noqa: F401
from postopus.octopus_run import Run  # noqa: F401

__version__ = metadata.version("postopus")
