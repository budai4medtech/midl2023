#INKSCAPE?=inkscape --export-png # Inkscape (svg support)
#INKSCAPE?=inkscape --export-filename	# Inkscape (svg support)
INKSCAPE?=inkscape --export-dpi=200 --export-filename 

OS_VERS:=$(shell lsb_release -a 2>/dev/null | grep Description | awk '{ print $$2 "-" $$3 }')
# https://stackoverflow.com/questions/30088319/using-shell-in-makefile-to-find-ubuntu-version

FIGURES_SVG=$(wildcard vectors/*.svg)
FIGURES_PNG=$(subst vectors/,outputs/,$(FIGURES_SVG:.svg=.png))
FIGURES_PDF=$(subst vectors/,outputs/,$(FIGURES_SVG:.svg=.pdf))

# Pattern rule for converting SVG to PNG and PDF
png:	$(FIGURES_PNG)
outputs/%.png: vectors/%.svg
	$(INKSCAPE) $(@) $(<)

pdf:	$(FIGURES_PDF)
outputs/%.pdf: vectors/%.svg
	$(INKSCAPE) $(@) $(<)

clean:  ##  output figure files
	rm -f $(FIGURES_PNG) $(FIGURES_PDF)

#test:
#	@echo $(OS_VERS)
