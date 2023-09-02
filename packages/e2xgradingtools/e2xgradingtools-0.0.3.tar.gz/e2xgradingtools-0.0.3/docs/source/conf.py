# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "E2X Grading Tools"
copyright = "2023, Tim Metzler"
author = "Tim Metzler"
release = "0.0.3"
github_project_url = "https://github.com/Digiklausur/e2xgradingtools"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Digiklausur/e2xgradingtools",
            "icon": "fa-brands fa-github",
        }
    ],
    "use_edit_page_button": True,
    "navbar_align": "left",
}

html_static_path = ["_static"]

html_context = {
    "github_user": "DigiKlausur",
    "github_repo": "e2xgradingtools",
    "github_version": "main",
    "doc_path": "docs/source/",
}
