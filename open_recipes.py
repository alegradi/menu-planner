"""open_recipe.py

Purpose is to open a certain file which contains the last saved recipe
"""

import json


MAIN_RECIPES = './recipes/main_recipes.json'
DESSERT_RECIPES = './recipes/dessert_recipes.json'
BREAD_RECIPES = './recipes/bread_recipes.json'

def open_recipe(recipe):
    """
    Retrieve a recipe from the appropriate JSON file
    Args:
        recipe (dict): Recipe details containing 'genre' and 'name'
    Returns:
        The found recipe dictionary
    """
    if recipe['genre'].lower() == 'dessert':
        file_to_open = DESSERT_RECIPES
    elif recipe['genre'].lower() == 'bread':
        file_to_open = BREAD_RECIPES
    else:
        file_to_open = MAIN_RECIPES

    with open(file_to_open, 'r', encoding='utf-8') as file:
        file_main_recipes = json.load(file)
        for rec in file_main_recipes["recipes"]:
            if rec['name'].lower() == recipe['name'].lower():
                return rec

    return None


