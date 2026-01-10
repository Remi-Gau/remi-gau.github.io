"""Convert recipes from cooklang to markdown using the cook CLI."""

import json
import os
import shutil
from pathlib import Path
from subprocess import run
from warnings import warn

import pandas as pd
import yaml
from rich import print
from utils import (
    ingredients_json,
    ingredients_tsv,
    output_folder,
    recipe_folder,
    root_folder,
    static_folder,
)
from yaml import Dumper, Loader

unknown_ingredient = []


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

        calories = None
        if calories := _compute_calories_recipe(recipe) and servings:
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

                if front_matter_delim_count == 2:
                    cleaned_lines.append(f"lang: {locale}\n")

                    if calories is not None:
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

    print(sorted(unknown_ingredient))


def _list_recipes(recipe_folder) -> list[Path]:
    return [
        recipe
        for recipe in recipe_folder.glob("**/*.cook")
        if recipe.parents[0].stem != "TODO"
    ]


def _all_known_ingredients() -> list[str]:
    with ingredients_json.open("r") as f:
        ingredients_json_content = json.load(f)

    # rewrite json in sorted order
    tmp = {}
    for x in sorted(ingredients_json_content):
        tmp[x] = ingredients_json_content[x]
    with ingredients_json.open("w") as f:
        json.dump(tmp, f)

    known_ingredients = []
    for x in ingredients_json_content:
        known_ingredients.extend(
            [x, *ingredients_json_content[x]["other_names"]]
        )
    return known_ingredients


def _compute_calories_recipe(recipe: dict) -> float | None:
    known_ingredients = _all_known_ingredients()

    all_ingredients = [x["name"] for x in recipe["ingredients"]]

    if set(all_ingredients).intersection(set(unknown_ingredient)):
        return None
    if missing_ingredients := list(
        set(all_ingredients) - set(known_ingredients)
    ):
        unknown_ingredient.extend(missing_ingredients)
        print(f"unknown ingredients for this recipe: {missing_ingredients}")
        return None

    calories = 0.0
    for ingredient in recipe["ingredients"]:
        if cal := _compute_calories(ingredient):
            calories += cal
        print(f"  {ingredient['name']}: {cal}")

    return calories


def _compute_calories(ingredient) -> int | float:
    """Compute calories for recipe.

    Adapt if ingredients have calories expressed per unit or per 100 gr.
    """
    if ingredient["quantity"] is None:
        return 0

    name = ingredient["name"]
    unit = ingredient["quantity"]["unit"]

    with ingredients_json.open("r") as f:
        ingredients_json_content = json.load(f)

    for x in ingredients_json_content:
        if name in [x, *ingredients_json_content[x]["other_names"]]:
            ingredient_key = x
            break

    cal = 0
    if unit == ingredients_json_content[ingredient_key]["unit"]:
        dose = 1
        if unit == "g":
            dose = 100

        quantity = ingredient["quantity"]["value"]["value"]["value"]

        cal = (
            quantity
            / dose
            * ingredients_json_content[ingredient_key]["calories"]
        )

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
        if "_" in recipe.name:
            raise ValueError(f"no '_' allowed in file name: {recipe}")

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

        with recipe.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        with recipe.open("w") as f:
            frontmatter = False

            frontmatter_content = []

            for li in lines:
                if li == "---\n":
                    if frontmatter:
                        # dump frontmatter back into file.

                        data = yaml.load(
                            "".join(frontmatter_content), Loader=Loader
                        )
                        sorted_data = dict(sorted(data.items()))

                        new_frontmatter = yaml.dump(
                            sorted_data, Dumper=Dumper, indent=4, width=120
                        )
                        f.write(new_frontmatter)

                    frontmatter = not frontmatter

                # remove empty lines
                if frontmatter:
                    if li == "\n":
                        continue

                    if li != "---\n":
                        frontmatter_content.append(li)
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
