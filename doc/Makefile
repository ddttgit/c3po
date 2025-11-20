# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   = /home/c3po_tma/workspaces/workspace_di_51/TEST_DOC_DataAccessor_PhysicsDriver/virt-c3po-ub24/bin/sphinx-build
#SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
TMPDIR        = tmp

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clean

clean:
	@rm -r ${TMPDIR}
