clean:
	rm -rf _site
build: clean
	jekyll build
serve: build
	jekyll serve
