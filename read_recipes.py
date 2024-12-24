import json

with open('recipes/main_recipes.json', 'r') as file:
    file_main_recipes = json.load(file)
    main_recipes = file_main_recipes["recipes"]

with open('recipes/dessert_recipes.json', 'r') as file:
    file_desserts = json.load(file)
    desserts = file_desserts["desserts"]

# print(main_recipes)
# print(desserts)