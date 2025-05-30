"""read_recipes.py

Purpose is to read in recipes to be used by other functions
"""

import json


with open('recipes/main_recipes.json', 'r', encoding='utf-8') as file:
    file_main_recipes = json.load(file)
    main_recipes = file_main_recipes["recipes"]

with open('recipes/dessert_recipes.json', 'r', encoding='utf-8') as file:
    file_desserts = json.load(file)
    desserts = file_desserts["recipes"]

with open('recipes/bread_recipes.json', 'r', encoding='utf-8') as file:
    file_breads = json.load(file)
    bread = file_breads["recipes"]


## Debug Information
# print(main_recipes)
# print(desserts)
