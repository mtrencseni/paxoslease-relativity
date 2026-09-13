LATEXMK   ?= latexmk
PYTHON    ?= python3
BUILD     := build
PAPER_TEX := paper/PaxosLease-Relativity.tex
PAPER_PDF := paper/PaxosLease-Relativity.pdf
FIGDIR    := figures

.PHONY: all pdf figures clean

all: pdf

paper-source:
	test -f $(PAPER_TEX)

figures:
	cd $(FIGDIR) && $(PYTHON) figs.py

pdf: paper-source
	mkdir -p $(BUILD)/latex
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error \
		-outdir=$(BUILD)/latex $(PAPER_TEX)
	cp $(BUILD)/latex/PaxosLease-Relativity.pdf $(PAPER_PDF)

clean:
	rm -rf $(BUILD)
