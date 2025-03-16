"""Common functions."""

import pathlib

root_folder = pathlib.Path(__file__).parents[1]
recipe_folder = root_folder / "cooklang_recipes"
output_folder = root_folder / "_recipes"
static_folder = root_folder / "static"
ingredients_tsv = recipe_folder / "ingredients.tsv"
calories_json = recipe_folder / "calories.json"
