import json

"""read_recipes.py

Purpose is to read in recipes to be used by other functions
"""

with open('recipes/main_recipes.json', 'r', encoding='utf-8') as file:
    file_main_recipes = json.load(file)
    main_recipes = file_main_recipes["recipes"]

with open('recipes/dessert_recipes.json', 'r', encoding='utf-8') as file:
    file_desserts = json.load(file)
    desserts = file_desserts["recipes"]

# print(main_recipes)
# print(desserts)
