all: clean install convert_recipe

clean:
	rm -rf _site

install: get_cook_cli
	pip install -r maint_tools/requirements.txt

get_cook_cli:
	bash maint_tools/get_cook_cli.sh

convert_recipe:
	python maint_tools/convert_recipes.py

serve:
	bundle exec jekyll serve
