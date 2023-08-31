extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "nbsphinx",
    "sphinx_rtd_theme"
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# General information about the project.
project = "postopus"
copyright = "2022, MPSD"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv"]

html_theme = "sphinx_rtd_theme"

try:
    from postopus import __version__ as version
except ImportError:
    release = ""  # The short X.Y version.
    version = ""  # The full version, including alpha/beta/rc tags.
else:
    release = version

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

