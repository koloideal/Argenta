# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	
live-ru:
	sphinx-autobuild -b html . _build/html/ru -D language=ru
	
serve-all:
	sphinx-build -b html . _build/html/ -D language=en
	sphinx-build -b html . _build/html/ru -D language=ru
	python -m http.server -d _build/html
	
update-langs:
	sphinx-build -b gettext . _build/gettext
	sphinx-intl update -p _build/gettext -l en -l ru

.PHONY: help Makefile serve-all

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
