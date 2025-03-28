"""build_meny.py

Build the menu here
"""

import random
from read_recipes import main_recipes
from read_recipes import desserts
from read_recipes import bread

def build_main_menu():
    """Build the menu by selecting random recipes from
    main, plus a random dessert"""
    main_menu = []
    total_weight = 0

    available_recipes = main_recipes.copy()

    while total_weight < 5 and available_recipes:
        recipe = random.choice(available_recipes)
        main_menu.append(recipe)
        total_weight += recipe['weight']
        available_recipes.remove(recipe)

        ## Debug Information
        # print(total_weight)

    # Add a dessert to the menu
    main_menu.append(random.choice(desserts))

    return main_menu

def bread_suggestion():
    """Suggesting bread recipe by selecting random recipes from
    bread"""
    available_recipes = bread.copy()
    recipe = random.choice(available_recipes)
    return recipe

if __name__ == "__main__":
    menu = build_main_menu()

    ## Debug Information
    # print(menu)
