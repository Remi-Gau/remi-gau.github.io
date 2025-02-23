import pathlib
from subprocess import run
import os

root_folder = pathlib.Path(__file__).parents[1]
recipe_folder = root_folder / "recipes"
output_folder  = root_folder / "_recipes"

os.chdir(recipe_folder)

for recipe in recipe_folder.glob("*.cook"):
    recipe = recipe.relative_to(recipe_folder)
    output_file = output_folder.relative_to(root_folder) / f"{recipe.stem}.md"
    cmd = f"cook recipe {recipe} -o ../{output_file}"
    print(cmd)
    run(cmd.split())
