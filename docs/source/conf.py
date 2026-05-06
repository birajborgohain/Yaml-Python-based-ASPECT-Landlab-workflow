#====================================================================================================
#  Copyright (c) 2026,
#  Biraj Borgohain
#
#  project: Geodynamic and Surface Processes Notes
#====================================================================================================

import pathlib
import os
import sys

# -- Path setup --------------------------------------------------------------

project_root = pathlib.Path(__file__).parents[2].resolve().as_posix()
sys.path.insert(0, project_root)

# -- Project information -----------------------------------------------------

project = 'ASPECT-Landlab Test Python Framework'
copyright = '2026, Biraj Borgohain'
author = 'Biraj Borgohain'
release = '0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',          # optional (future-proof)
    'sphinxcontrib.bibtex',
]

templates_path = ['_templates']
exclude_patterns = []

# Bibliography
bibtex_bibfiles = ['References/refs.bib']
bibtex_default_style = 'apa'
bibtex_reference_style = 'author_year'

# Allow cross-folder inclusion
include_patterns = ['**']

# -- HTML output -------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "prev_next_buttons_location": "both",
}

# -- Mock imports (safe for RTD) --------------------------------------------

autodoc_mock_imports = ["pyviztools", "faulttools"]

# -- Custom substitutions ----------------------------------------------------

rst_prolog = """
.. |ASPECT| replace:: *Advanced Solver for Problems in Earth's ConvecTion*
.. |FastScape| replace:: *Landscape evolution model*
"""

html_static_path = ['_static']
html_css_files = ['custom.css']