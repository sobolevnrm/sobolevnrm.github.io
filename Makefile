.PHONY: default github brown cv

all: cv github brown
cv:
	cd cv && make all
github:
	python bibtex_to_markdown.py
	cd pelican && pelican content -o .. -s pelicanconf.py
	git status
	@echo "*** Now you need to commit and push the changes to GitHub"
brown:
	python bibtex_to_markdown.py
	cd pelican && pelican content -o brown_website -s pelicanconf.py
	cd pelican && rsync -avz -e ssh brown_website fritz:web/
	@echo "*** Now you need to move the files to monitor:/export/data/dam/dam-web/htdocs/people/baker"
