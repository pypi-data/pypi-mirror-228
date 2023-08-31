import re

import postopus


def test_version():
    """ "
    Test valid python version.
    https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
    """
    return (
        re.match(
            r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)"
            r"(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
            postopus.__version__,
        )
        is not None
    )
