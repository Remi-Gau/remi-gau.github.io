all: clean get_cook_cli convert_recipe podcasts.html

clean:
	rm -rf _site

get_cook_cli:
	bash maint_tools/get_cook_cli.sh

convert_recipe:
	python maint_tools/convert_recipes.py

serve:
	bundle exec jekyll serve
