import json

MAIN_RECIPES = './recipes/main_recipes.json'
DESSERT_RECIPES = './recipes/dessert_recipes.json'

# Function to save new recipe to the JSON file
def save_recipe(recipe):
    if recipe['genre'].lower() == 'dessert':
        file_to_save = DESSERT_RECIPES
    else:
        file_to_save = MAIN_RECIPES

    try:
        # Open the file and load the data (which is a dictionary with a "recipes" key)
        with open(file_to_save, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty, initialize the data structure
        data = {"recipes": []}

    # Append the new recipe to the list of recipes
    data["recipes"].append(recipe)

    # Save the updated dictionary back to the JSON file
    with open(file_to_save, 'w') as file:
        json.dump(data, file, indent=4)
