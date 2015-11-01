.PHONY: default pelican

default: pelican
pelican:
	cd pelican && pelican content -o .. -s pelicanconf.py 
