stem=pubs
all:
	latexmk -pdf $(stem)
	open $(stem).pdf
clean:
	rm *bbl
	latexmk -C
