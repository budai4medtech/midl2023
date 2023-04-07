fileinfo := LaTeX Makefile
author := Miguel Xochicale

## Tools
LATEXMK = latexmk
RM = rm -f
EVINCE = evince
FLAGS = -pdf -pdflatex="pdflatex -interaction=nonstopmode -shell-escape -file-line-error %O %S" -use-make

##Project name
PROJNAME=midl-shortpaper

## Rules
$(PROJNAME).pdf: $(PROJNAME).tex
	$(LATEXMK) $(FLAGS) $<

view:
	$(EVINCE) $(PROJNAME).pdf

mostlyclean:
	$(LATEXMK) -silent -C

clean: mostlyclean
	$(LATEXMK) -silent -c
	$(RM) $(PROJNAME).pdf $(PROJNAME).bbl *.nav *.snm


