# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Octopus Sensing'
copyright = '2021, Nastaran Saffaryazdi, Aidin Gharibnavaz'
author = 'Nastaran Saffaryazdi, Aidin Gharibnavaz'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode']

# Napoleon settings
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

autodoc_default_options = {
    'members': 'var1, var2',
    'member-order': 'bysource',
    'undoc-members': True,
    'private_members': False,
    'exclude-members': '__weakref__',
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
# -- Options for HTML output -------------------------------------------------

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_sidebars = { '**': ['globaltoc.html',
                         'relations.html',
                         'sourcelink.html',
                         'searchbox.html']}

html_context = {
    'source_url_prefix': "https://github.com/octopus-sensing/octopus-sensing/blob/master/docs/",
    "display_github": True,
    "github_host": "github.com",
    "github_user": "octopus-sensing",
    "github_repo": "octopus-sensing",
    "github_version": "master",
    "conf_py_path": "/docs/",
    "source_suffix": '.rst',
}

html_favicon = "_static/favicon.png"
