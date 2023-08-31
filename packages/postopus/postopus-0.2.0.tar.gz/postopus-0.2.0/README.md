# Postopus

[Postopus](https://gitlab.com/octopus-code/postopus/) (the POST-processing of OctoPUS data) is an environment that
can help with the analysis of data that was computed using the [Octopus](https://octopus-code.org) TDDFT package.

## Documentation

The documentation of postopus is hosted [here](https://octopus-code.gitlab.io/postopus/index.html).
To build the documentation locally: `cd docs && make html`. It will be built into: `docs/_build/html`. Open then the `index.html`

## Setup

Python versions supported: 3.8, 3.9. Python 3.10 is supported.
Release 0.2.0 will support octopus@12.0, 12.1, 12.2.

To clone the repository: `git clone https://gitlab.com/octopus-code/postopus.git`

### User Setup

Using a virtual environment is recommended.
To install the project's dependencies, navigate (`cd`) into the project directory and run (`pip >21.3` required) `pip install .`.
The `recommended` dependencies are highly recommended for all users, as they are needed to run the tutorials interactively. (`pip install .[recommended]`).

In case you did not clone the repository you can install the Postopus dependencies via `pip install postopus[recommended]`

Note: ase is not listed as a dependency, but it will be needed, so please execute: `pip install git+https://gitlab.com/ase/ase.git@master`.
Context, for those who are interested: `ase` has already merged some of our feature requests that are needed for postopus, but they are not yet tag-released.
### Developer Setup

This section is for developers wanting to contribute to Postopus.
To setup your development environment, you not only need to install the dependencies of the project's code itself but also some modules for testing and keeping the repo clean through pre-commit hooks:

- Installing Postopus with development dependencies in editable mode can be done with `pip install -e .[dev]` (`pip >21.3` required)
  (or `pip install -e '.[dev]'` if you are using mac default's `zsh`) in the project's main directory. If you also want the `docs` requirements you would need to execute `pip install -e .[dev,docs]`
- After installing, you'll need to set up the pre-commit module. Do this with `pre-commit install` in the project's root.
- Tests might require output data from Octopus, for this refer to the section below (Invoke tasks).

#### Release

Currently, the following invoke tasks are available:

- **release**:   Run the release steps, which include syncing the git repo, building the package and pushing it to PyPI
and finally tagging the release commit. By default, the task uploads to the test server; use the flag `--test=False`
to upload to the real PyPI server. Release to the main PyPI can only be done from the main branch
(use `--test=False` or `--no-test`) Example run:

```bash
$ invoke release --no-test
```

Note we highly recommend using the `--debug` flag of `invoke`, specially if something is not working as expected.
By default, invoke fails silently.

#### Testing
- `invoke  generatePytestData` generates the necessary test data to run `pytest`
in the main project directory.
