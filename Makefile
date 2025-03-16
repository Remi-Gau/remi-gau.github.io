all: clean install convert_recipe

clean:
	rm -rf _site
	rm -rf _recipes/*.md
	rm -rf _recipes/*.json
	rm -rf _recipes/fr
	rm -rf _recipes/en

install: get_cook_cli
	pip install -r maint_tools/requirements.txt

get_cook_cli:
	bash maint_tools/get_cook_cli.sh

convert_recipe:
	python maint_tools/convert_recipes.py

serve:
	bundle exec jekyll serve
