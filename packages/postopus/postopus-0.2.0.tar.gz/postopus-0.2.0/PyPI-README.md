# Postopus

[Postopus](https://gitlab.com/octopus-code/postopus/) (the POST-processing of OctoPUS data) is an environment that
can help with the analysis of data that was computed using the [Octopus](https://octopus-code.org) TDDFT package.

Note: ase is not listed as a dependency, but it will be needed, so please execute: `pip install git+https://gitlab.com/ase/ase.git@master`.
Context, for those who are interested: `ase` has already merged some of our feature requests that are needed for postopus, but they are not yet tag-released.

## Version support

Python versions supported: 3.8, 3.9 and 3.10.
Release 0.2.0 will support octopus@12.0, 12.1, 12.2.

## Recommended installation

For analyzing data, static (matplotlib) and interactive (holoviews) plotting inside Jupyter Notebooks are a common choice. Thus,
`pip install postopus[recommended]` is recommended, which will install the needed packages for this purpose.
