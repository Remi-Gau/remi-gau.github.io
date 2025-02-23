clean:
	rm -rf _site

serve:
	bundle exec jekyll serve

all: clean get_cook_cli convert_recipe

get_cook_cli:
	bash maint_tools/get_cook_cli.sh

convert_recipe:
	python maint_tools/convert_recipes.py
