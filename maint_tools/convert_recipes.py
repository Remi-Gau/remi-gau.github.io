"""Convert recipes from cooklang to markdown using the cook CLI."""

import json
import os
import pathlib
import shutil
from subprocess import run
from warnings import warn

import pandas as pd
from rich import print

root_folder = pathlib.Path(__file__).parents[1]
recipe_folder = root_folder / "cooklang_recipes"
output_folder = root_folder / "_recipes"
static_folder = root_folder / "static"
ingredients_tsv = recipe_folder / "ingredients.tsv"
calories_json = recipe_folder / "calories.json"


def main():
    """Convert cooklang recipes to markdown and clean them up."""
    convert()
    validate_recipes()
    list_ingredients()
    copy_images()

    os.chdir(recipe_folder)

    for recipe in recipe_folder.glob("*.cook"):
        recipe = recipe.relative_to(recipe_folder)

        markdown_file = output_folder / f"{recipe.stem}.md"

        print(f"\n Cleaning {markdown_file.name}")

        with (markdown_file.with_suffix(".json")).open("r") as f:
            recipe = json.load(f)

        locale = recipe.get("metadata").get("map").get("locale")
        servings = recipe.get("metadata").get("map").get("servings")

        calories = 0
        if servings:
            with calories_json.open("r") as f:
                calories_json_content = json.load(f)
            known_ingredients = {
                x["locale"][locale]: {
                    "calories": x["calories"],
                    "unit": x["unit"],
                }
                for x in calories_json_content
            }

            for x in recipe["ingredients"]:
                if cal := compute_calories(x, known_ingredients):
                    calories += cal
                print(f"  {x['name']}: {cal}")

            calories /= servings

        with markdown_file.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        cleaned_lines = []
        front_matter_delim_count = 0
        for line in lines:
            if line.strip() == "#":
                continue

            if line.strip() == "---":
                front_matter_delim_count += 1
                if calories and front_matter_delim_count == 2:
                    line = f"calories: {round(calories)}\n{line}"
                    cleaned_lines.append(line)
                    continue

            if locale == "fr":
                if line.strip() == "## Ingredients":
                    line = "## Ingrédients\n"
                elif line.strip() == "## Steps":
                    line = "## Étapes\n"

            cleaned_lines.append(line)

        with markdown_file.open("w", encoding="utf-8") as file:
            file.writelines(cleaned_lines)


def compute_calories(ingredient, known_ingredients) -> int | float:
    """Compute calories for recipe.

    Adapt if ingredients have calories expressed per unit or per 100 gr.
    """
    if ingredient["quantity"] is None:
        return 0
    name = ingredient["name"]
    unit = ingredient["quantity"]["unit"]

    cal = 0
    if name in known_ingredients and (unit == known_ingredients[name]["unit"]):
        dose = 1
        if unit == "gr":
            dose = 100

        quantity = ingredient["quantity"]["value"]["value"]["value"]

        cal = quantity / dose * known_ingredients[name]["calories"]

    return cal


def convert():
    """Convert recipes to markdown and json."""
    os.chdir(recipe_folder)

    for recipe in recipe_folder.glob("*.cook"):
        recipe = recipe.relative_to(recipe_folder)

        markdown_file = (
            output_folder.relative_to(root_folder) / f"{recipe.stem}.json"
        )
        cmd = f"cook recipe {recipe} -o ../{markdown_file} -f json"
        print(f" {cmd}")
        run(cmd.split())

        json_file = (
            output_folder.relative_to(root_folder) / f"{recipe.stem}.md"
        )
        cmd = f"cook recipe {recipe} -o ../{json_file}"
        print(f" {cmd}")
        run(cmd.split())


def validate_recipes():
    """Validate the frontmatter of a recipe."""
    os.chdir(recipe_folder)

    for recipe in recipe_folder.glob("*.cook"):
        json_file = (
            output_folder.relative_to(root_folder) / f"{recipe.stem}.json"
        )
        # read json and get list of ingredients
        with (root_folder / json_file).open("r") as f:
            content = json.load(f)

        metadata = content.get("metadata").get("map")
        for key in ["category", "prep_time", "locale"]:
            if key not in metadata:
                raise ValueError(
                    f"Recipe must contain a '{key}' key.\nIn {recipe}"
                )

        for key in ["servings"]:
            if key not in metadata:
                warn(
                    f"Recipe should contain a '{key}' key.\nIn {recipe}",
                    stacklevel=2,
                )


def list_ingredients():
    """Make list of all ingredients across recipes."""
    os.chdir(recipe_folder)

    ingredients = []

    for recipe in recipe_folder.glob("*.cook"):
        json_file = (
            output_folder.relative_to(root_folder) / f"{recipe.stem}.json"
        )
        # read json and get list of ingredients
        with (root_folder / json_file).open("r") as f:
            content = json.load(f)

        ingredients.extend(x["name"] for x in content["ingredients"])

    ingredients = pd.DataFrame({"ingredients": sorted(set(ingredients))})
    ingredients.to_csv(ingredients_tsv, sep="\t", index=False)


def copy_images():
    """Copy images from the cooklang folder to the output folder."""
    os.chdir(recipe_folder)
    print()
    for image in recipe_folder.glob("*.jpg"):
        output_image = (
            static_folder / "assets" / "img" / "recipes" / image.name
        )
        print(
            f" Copying {image.relative_to(root_folder)} "
            f"to {output_image.relative_to(root_folder)}"
        )
        # copy not move
        shutil.copy(image, output_image)


if __name__ == "__main__":
    main()
