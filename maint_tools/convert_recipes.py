"""Convert recipes from cooklang to markdown using the cook CLI."""

import json
import os
import shutil
from pathlib import Path
from subprocess import run
from warnings import warn

import pandas as pd
from rich import print
from utils import (
    calories_json,
    ingredients_tsv,
    output_folder,
    recipe_folder,
    root_folder,
    static_folder,
)


def main():
    """Convert cooklang recipes to markdown and clean them up."""
    convert()
    validate_recipes()
    format_recipes()
    list_ingredients()
    copy_images()

    os.chdir(recipe_folder)

    for recipe in _list_recipes(recipe_folder):
        markdown_file = root_folder / _output_file(
            output_folder, recipe, ".md"
        )
        json_file = root_folder / _output_file(output_folder, recipe, ".json")
        print(f"\n Cleaning {markdown_file.name}")

        with json_file.open("r") as f:
            recipe = json.load(f)
        locale = json_file.parents[0].stem
        servings = recipe.get("metadata").get("map").get("servings")

        calories = 0
        if servings:
            calories = _compute_calories_recipe(recipe, locale) / servings

        with markdown_file.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        cleaned_lines = []
        front_matter_delim_count = 0
        for line in lines:
            if line.strip() == "#":
                continue

            if line.strip() == "---":
                front_matter_delim_count += 1

                if front_matter_delim_count == 2:
                    cleaned_lines.append(f"lang: {locale}\n")

                    if calories:
                        line = f"calories: {round(calories)}\n{line}"
                        cleaned_lines.append(line)
                        continue

            if locale == "fr":
                if line.strip() == "## Ingredients":
                    line = "## Ingrédients\n"
                elif line.strip() == "## Cookware":
                    line = "## Ustensiles\n"
                elif line.strip() == "## Steps":
                    line = "## Étapes\n"

            cleaned_lines.append(line)

        with markdown_file.open("w", encoding="utf-8") as file:
            file.writelines(cleaned_lines)


def _list_recipes(recipe_folder) -> list[Path]:
    return [
        recipe
        for recipe in recipe_folder.glob("**/*.cook")
        if recipe.parents[0].stem != "TODO"
    ]


def _compute_calories_recipe(recipe, locale):
    with calories_json.open("r") as f:
        calories_json_content = json.load(f)
    known_ingredients = {
        x["locale"][locale]: {
            "calories": x["calories"],
            "unit": x["unit"],
        }
        for x in calories_json_content
    }

    calories = 0
    for x in recipe["ingredients"]:
        if cal := _compute_calories(x, known_ingredients):
            calories += cal
        print(f"  {x['name']}: {cal}")
    return calories


def _compute_calories(ingredient, known_ingredients) -> int | float:
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


def convert() -> None:
    """Convert recipes to markdown and json."""
    os.chdir(recipe_folder)

    missing_translations = []

    for recipe in _list_recipes(recipe_folder):
        locale = recipe.parents[0].stem
        if locale == "TODO":
            continue

        if "/fr/" in str(recipe):
            corresponding_en = Path(str(recipe).replace("/fr/", "/en/"))
            if not corresponding_en.exists():
                missing_translations.append(recipe.name)

        markdown_file = _output_file(output_folder, recipe, ".md")
        json_file = _output_file(output_folder, recipe, ".json")

        (root_folder / markdown_file).parent.mkdir(parents=True, exist_ok=True)

        recipe = recipe.relative_to(recipe_folder)

        cmd = f"cook recipe {recipe} -o ../{json_file} -f json"
        print(f" {cmd}")
        run(cmd.split())

        cmd = f"cook recipe {recipe} -o ../{markdown_file} -f md"
        print(f" {cmd}")
        run(cmd.split())

    if missing_translations:
        raise ValueError(
            "Missing translations for the following recipes:\n\t-"
            + "\n\t-".join(missing_translations)
        )


def _output_file(output_folder, recipe, suffix):
    locale = recipe.parents[0].stem
    recipe = recipe.relative_to(recipe_folder)

    return (
        output_folder.relative_to(root_folder)
        / locale
        / f"{recipe.stem}{suffix}"
    )


def validate_recipes():
    """Validate the frontmatter of a recipe."""
    os.chdir(recipe_folder)

    for recipe in _list_recipes(recipe_folder):
        json_file = root_folder / _output_file(output_folder, recipe, ".json")
        # read json and get list of ingredients
        with json_file.open("r") as f:
            content = json.load(f)

        metadata = content.get("metadata").get("map")
        for key in ["category", "prep_time"]:
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


def format_recipes():
    """Format the recipe.

    Clean up front matter.
    """
    os.chdir(recipe_folder)

    for recipe in _list_recipes(recipe_folder):
        locale = recipe.parents[0].stem
        if locale == "TODO":
            continue

        with recipe.open("r") as f:
            lines = f.readlines()

        with recipe.open("w") as f:
            frontmatter = False

            for li in lines:
                if li == "---\n":
                    frontmatter = not frontmatter

                # remove empty lines
                if frontmatter and li == "\n":
                    continue

                f.write(li)


def list_ingredients():
    """Make list of all ingredients across recipes."""
    os.chdir(recipe_folder)

    ingredients = []

    for recipe in _list_recipes(recipe_folder):
        json_file = root_folder / _output_file(output_folder, recipe, ".json")
        # read json and get list of ingredients
        with json_file.open("r") as f:
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
