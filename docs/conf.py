# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "../toolbox_acclimate"))
from _version import get_versions  # isort:skip # append path before


# -- Project information -----------------------------------------------------

project = "toolbox_acclimate"
copyright = "2025"
author = "Acclimate Team"
version = get_versions()["version"]  # The short X.Y version
release = version  # The full version, including alpha/beta/rc tags


# -- General configuration ---------------------------------------------------

exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    'sphinx_rtd_theme',
    "m2r2"
    #"sphinx_autodoc_typehints",  # must be after sphinx.ext.napoleon
]
language = "en"
master_doc = "index"
needs_sphinx = "1.8"
nitpick_ignore = [
    ("py:class", "Callable"),
    ("py:class", "Optional"),
    ("py:class", "Sequence"),
    ("py:class", "Union"),
    ("py:class", "np.ndarray"),
    ("py:class", "typing.Tuple"),
    ("py:class", "typing.Union"),
]
pygments_style = "sphinx"
source_suffix = ".rst"  # ['.rst', '.md']
templates_path = ["templates"]


def skip_init(app, what, name, obj, skip, options):
    if name == "__init__":
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_init)


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["static"]
html_context = {
    "display_github": False,
    "github_user": "acclimate",
    "github_repo": "toolbox-acclimate",
    "github_version": "master",
    "conf_py_path": "/docs/",
}


# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = "toolbox-acclimate-doc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "toolbox-acclimate.tex",
        "toolbox-acclimate -- documentation",
        author,
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "acclimate", "toolbox-acclimate - documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "toolbox-acclimate",
        "toolbox-acclimate - documentation",
        author,
        "toolbox-acclimate",
        "Python library and scripts for simulations and post-processing output of the Acclimate model.",
        "Miscellaneous",
    )
]


# -- Extension configuration -------------------------------------------------

autodoc_default_options = {
    "inherited-members": None,
    "members": None,
    "private-members": None,
    "show-inheritance": None,
    "undoc-members": None,
}
coverage_write_headline = False  # do not write headlines.
intersphinx_mapping = {
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
}
napoleon_google_docstring = False
napoleon_numpy_docstring = True
set_type_checking_flag = True
