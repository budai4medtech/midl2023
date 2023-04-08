
OS_VERSION:=$(shell lsb_release -a 2>/dev/null | grep Description | awk '{ print $$2 "-" $$3 }')
$(eval $(shell grep VERSION_ID /etc/os-release))
#ifeq ($(VERSION_ID), 22.04)
ifeq ($(OS_VERSION), Ubuntu-22.04.1)
EXPORT_ID = --export-filename
else
EXPORT_ID = --export-png
endif
# https://stackoverflow.com/questions/714100/os-detecting-makefile

INKSCAPE?=inkscape --export-dpi=200 $(EXPORT_ID)


#dPDFSETTINGS=screen #lower quality, smaller size. (72 dpi)
#dPDFSETTINGS=ebook #for better quality, but slightly larger pdfs. (150 dpi)
#dPDFSETTINGS=prepress #output similar to Acrobat Distiller "Prepress Optimized" setting (300 dpi)
#dPDFSETTINGS=printer #selects output similar to the Acrobat Distiller "Print Optimized" setting (300 dpi)
dPDFSETTINGS=default #selects output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file

GS?=gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/$(dPDFSETTINGS) -dNOPAUSE -dQUIET -dBATCH -sOutputFile=

FIGURES_SVG=$(wildcard vectors/*.svg)
FIGURES_PNG=$(subst vectors/,outputs/,$(FIGURES_SVG:.svg=.png))
FIGURES_PDF=$(subst vectors/,outputs/,$(FIGURES_SVG:.svg=.pdf))
FIGURES_PDF_REDUCED_SIZE=$(subst vectors/,outputs/,$(FIGURES_SVG:.svg=_reduced_size.pdf))

# Pattern rule for converting SVG to PNG and PDF
png:	$(FIGURES_PNG)
outputs/%.png: vectors/%.svg
	$(INKSCAPE) $(@) $(<)

pdf:	$(FIGURES_PDF)
outputs/%.pdf: vectors/%.svg
	$(INKSCAPE) $(@) $(<)

edit:
	inkscape $(FIGURES_SVG)

view-png:
	eog $(FIGURES_PNG)

view-pdf:
	evince $(FIGURES_PDF)

reduce-pdf-size:
	$(GS)$(FIGURES_PDF_REDUCED_SIZE) $(FIGURES_PDF)

clean:  ##  output figure files
	rm -f $(FIGURES_PNG) $(FIGURES_PDF) outputs/*.pdf

test:
	echo $(VERSION_ID)
	echo $(OS_VERSION)
	echo $(EXPORT_ID)
