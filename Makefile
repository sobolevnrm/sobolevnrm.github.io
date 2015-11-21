.PHONY: default github brown cv

all: cv github brown
cv:
	cd cv && make all
github:
	cd pelican && pelican content -o .. -s pelicanconf.py
	git status
	@echo "*** Now you need to commit and push the changes to GitHub"
brown:
	cd pelican && pelican content -o brown_website -s pelicanconf.py
	cd pelican && rsync -az -e ssh brown_website fritz:web/
	@echo "*** Now you need to move the files to monitor:/export/data/dam/dam-web/htdocs/people/baker"
