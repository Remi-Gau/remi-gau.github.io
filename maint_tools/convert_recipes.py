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
    format_recipes()
    validate_recipes()
    list_ingredients()
    copy_images()
    update_markdowns()

    print(sorted(unknown_ingredient))


def update_markdowns() -> None:
    """Clean markdown and add calorie per serving."""
    os.chdir(recipe_folder)

    for recipe in _list_recipes(recipe_folder):
        markdown_file = root_folder / _output_file(
            output_folder, recipe, ".md"
        )
        json_file = root_folder / _output_file(output_folder, recipe, ".json")
        print(f"\nCleaning {markdown_file.name}")

        with json_file.open("r") as f:
            recipe = json.load(f)
        locale = json_file.parents[0].stem
        servings = recipe.get("metadata").get("map").get("servings")

        calories, price = _compute_details_recipe(recipe)
        if calories is not None and servings is not None:
            calories /= servings
            calories = int(calories)
        else:
            calories = None

        if price is not None:
            print(f"{price=}")

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
                        line = f"calories: {calories}\n{line}"
                        print(f"calories / serving: {calories}")
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


def _all_known_ingredients() -> list[str]:
    with ingredients_json.open("r", encoding="utf-8") as f:
        ingredients_json_content = json.load(f)

    # rewrite json in sorted order
    tmp = {}
    for x in sorted(ingredients_json_content):
        tmp[x] = ingredients_json_content[x]
        tmp[x]["other_names"] = sorted(tmp[x]["other_names"])
    with ingredients_json.open("w", encoding="utf-8") as f:
        json.dump(tmp, f, indent=4, ensure_ascii=False)

    known_ingredients = []
    for x in ingredients_json_content:
        known_ingredients.extend(
            [x, *ingredients_json_content[x]["other_names"]]
        )
    return known_ingredients


def _compute_details_recipe(recipe: dict) -> tuple[float | None, float | None]:
    """Compute calories and price recipe."""
    known_ingredients = _all_known_ingredients()

    all_ingredients = [x["name"] for x in recipe["ingredients"]]

    if missing_ingredients := list(
        set(all_ingredients) - set(known_ingredients)
    ):
        print(f"\tunknown ingredients for this recipe: {missing_ingredients}")
        tmp = list(
            set(all_ingredients)
            - set(known_ingredients)
            - (set(unknown_ingredient))
        )
        unknown_ingredient.extend(tmp)
        return None, None

    calories = 0.0
    price: float | None = 0.0
    for ingredient in recipe["ingredients"]:
        cal, pr = _compute_calories_and_price(ingredient)
        if cal:
            calories += cal
        if pr is None:
            price = None
        elif price is not None:
            price += pr

    return calories, price


def _compute_calories_and_price(
    ingredient: dict,
) -> tuple[float, float | None]:
    """Compute calories and price for a given ingredient.

    Adapt if ingredients have calories expressed per unit or per 100 gr.
    """
    if ingredient["quantity"] is None:
        return 0.0, 0.0

    name = ingredient["name"]
    unit = ingredient["quantity"]["unit"]

    with ingredients_json.open("r") as f:
        ingredients_json_content = json.load(f)

    for x in ingredients_json_content:
        if name in [x, *ingredients_json_content[x]["other_names"]]:
            ingredient_key = x
            break

    ingredient_unit = ingredients_json_content[ingredient_key]["unit"]
    ingredient_calories = ingredients_json_content[ingredient_key]["calories"]
    ingredient_price = ingredients_json_content[ingredient_key]["price_euro"]

    ingredient_quantity = ingredient["quantity"]["value"]["value"]["value"]

    if ingredient_calories == 0:
        cal = 0
    elif unit == ingredient_unit:
        cal = ingredient_quantity * ingredient_calories
    elif unit == "Kg" and ingredient_unit == "g":
        cal = ingredient_quantity * 1000 * ingredient_calories
    else:
        print(f"\tunknown unit for {name}: {unit}")
        cal = 0

    if ingredient_price is None:
        print(f"\tunknown price for {name}")
        pr = None
    elif unit == ingredient_unit:
        pr = ingredient_quantity * ingredient_price
    elif unit == "Kg" and ingredient_unit == "g":
        pr = ingredient_quantity * 1000 * ingredient_price
    else:
        print(f"\tunknown unit for {name}: {unit}")
        pr = None

    return cal, pr


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
                print(metadata)
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
    """Format .cook recipes.

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
