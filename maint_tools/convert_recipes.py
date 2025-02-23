import pathlib
from subprocess import run
import os

root_folder = pathlib.Path(__file__).parents[1]
recipe_folder = root_folder / "cooklang_recipes"
output_folder  = root_folder / "_recipes"

os.chdir(recipe_folder)

for recipe in recipe_folder.glob("*.cook"):
    recipe = recipe.relative_to(recipe_folder)
    output_file = output_folder.relative_to(root_folder) / f"{recipe.stem}.md"
    cmd = f"cook recipe {recipe} -o ../{output_file}"
    print(cmd)
    run(cmd.split())

for recipe in output_folder.glob("*.md"):
    with recipe.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    # Remove lines that only contain "# "
    cleaned_lines = [line for line in lines if line.strip() != "#"]

    with recipe.open("w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)
