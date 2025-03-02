"""Convert recipes from cooklang to markdown using the cook CLI."""

import os
import pathlib
import re
import shutil
from subprocess import run

import yaml
from rich import print

root_folder = pathlib.Path(__file__).parents[1]
recipe_folder = root_folder / "cooklang_recipes"
output_folder = root_folder / "_recipes"
static_folder = root_folder / "static"


def extract_frontmatter(md_text: str):
    """
    Extract frontmatter from a Markdown string and returns it as a dictionary.

    Args:
        md_text (str): The Markdown content as a string.

    Returns
    -------
        dict: A dictionary containing frontmatter data,
              or an empty dict if no frontmatter is found.
    """
    match = re.match(r"^---\n(.*?)\n---\n", md_text, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        return yaml.safe_load(frontmatter)  # Convert YAML to dict
    return {}


def validate_frontmatter(frontmatter: dict):
    """Validate the frontmatter of a recipe."""
    for key in ["category", "prep_time", "locale"]:
        if key not in frontmatter:
            raise ValueError(f"Frontmatter must contain a '{key}' key.")


def copy_images():
    """Copy images from the cooklang folder to the output folder."""
    for image in recipe_folder.glob("*.jpg"):
        output_image = (
            static_folder / "assets" / "img" / "recipes" / image.name
        )
        print(f" Copying {image} to {output_image}")
        # copy not move
        shutil.copy(image, output_image)


def main():
    """Convert cooklang recipes to markdown and clean them up."""
    os.chdir(recipe_folder)

    for recipe in recipe_folder.glob("*.cook"):
        recipe = recipe.relative_to(recipe_folder)
        output_file = (
            output_folder.relative_to(root_folder) / f"{recipe.stem}.md"
        )
        cmd = f"cook recipe {recipe} -o ../{output_file}"
        print(f" {cmd}")
        run(cmd.split())

    for recipe in output_folder.glob("*.md"):
        print(f" Cleaning {recipe}")

        with recipe.open("r", encoding="utf-8") as file:
            content = file.read()
        frontmatter = extract_frontmatter(content)
        validate_frontmatter(frontmatter)

        with recipe.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        cleaned_lines = []
        for line in lines:
            if line.strip() == "#":
                continue
            if frontmatter["locale"] == "fr":
                if line.strip() == "## Ingredients":
                    line = "## Ingrédients\n"
                elif line.strip() == "## Steps":
                    line = "## Étapes\n"
            cleaned_lines.append(line)

        with recipe.open("w", encoding="utf-8") as file:
            file.writelines(cleaned_lines)

    copy_images()


if __name__ == "__main__":
    main()
