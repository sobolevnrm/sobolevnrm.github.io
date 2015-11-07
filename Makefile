.PHONY: default github brown

github:
	cd pelican && pelican content -o .. -s pelicanconf.py
	git status
	@echo "*** Now you need to commit and push the changes to GitHub"
brown:
	cd pelican && pelican content -o brown_website -s pelicanconf.py
	cd pelican && rsync -avz -e ssh brown_website ${FRITZ}:web/
	@echo "*** Now you need to move the files to monitor:/export/data/dam/dam-web/htdocs/people/nbaker2"
