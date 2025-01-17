from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from build_menu import build_main_menu
from flask_bootstrap import Bootstrap
import json



app = Flask(__name__)
Bootstrap(app)

# sample data

sample_data = {
    "message": "Hello Flask API world!",
    "status": "success"
}

global_menu = []
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sample', methods=['GET'])
def get_data():
    return jsonify(sample_data)

@app.route('/menu', methods=['GET'])
def get_menu():
    built_menu = build_main_menu()
    return jsonify(built_menu)

@app.route('/recipes', methods=['GET'])
def get_recipes():
    global global_menu
    global_menu = build_main_menu()
    return render_template('recipes.html', menu=global_menu)

@app.route('/shopping_list')
def make_list():
    shopping_list = []
    for recipe in global_menu:
        shopping_list.extend(recipe['ingredients'])
    return render_template('shopping_list.html', shopping_list=shopping_list)

@app.route('/adding', methods=['GET', 'POST'])
def add_recipes():
    if request.method == 'POST':
        # Create the recipe dictionary as per the required format
        recipe = {
        "genre": request.form['genre'],
        "name": request.form['name'],
        "ingredients": [ingredient.strip() for ingredient in request.form['ingredients'].splitlines() if ingredient.strip()],
        "cuisine": request.form['cuisine'],
        "weight": int(request.form['weight']),
        "link": request.form['link'],
        "instructions": [instruction.strip() for instruction in request.form['instructions'].splitlines() if instruction.strip()]
    }

        save_recipe(recipe)

        return redirect(url_for('successful'))

    return render_template('adding.html')

@app.route('/successful')
def successful():
    return render_template('successful.html')


if __name__ == '__main__':
    app.run(debug=True)
