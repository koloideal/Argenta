# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Argenta"
copyright = "2025, kolo"
author = "kolo"
root_doc = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"
html_extra_path = ["robots.txt", "sitemap.xml", "llms.txt"]

html_theme_options = {
  "accent_color": "cyan",
  "nav_links": [
         {
             "title": "Sponsor me",
             "url": "https://github.com/sponsors/koloideal"
         },
     ],
    "github_url": "https://github.com/koloideal/Argenta",
    "linkedin_url": "https://www.linkedin.com/in/dmitry-shevelev-31b9a6324"
}

