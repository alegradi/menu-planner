from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from build_menu import build_main_menu
from save_recipe import save_recipe
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
    shopping_dict = {}  # Dictionary to track quantities per ingredient

    for recipe in global_menu:
        for ingredient in recipe['ingredients']:
            if ingredient:
                ingredient_name = ingredient['name']
                ingredient_quantity = ingredient['quantity']

                # If ingredient already exists, add to quantity
                if ingredient_name in shopping_dict:
                    shopping_dict[ingredient_name] += ingredient_quantity
                else:
                    shopping_dict[ingredient_name] = ingredient_quantity

    # Convert dictionary back to list of dictionaries
    shopping_list = [{"name": name, "quantity": quantity} for name, quantity in shopping_dict.items()]

    print("Final Shopping List:", shopping_list)
    return render_template("shopping_list.html", shopping_list=shopping_list)
   
@app.route('/adding', methods=['GET', 'POST'])
def add_recipes():
    if request.method == 'POST':
        ingredients = []
        # Process ingredients from form input
        raw_ingredients = request.form['ingredients'].splitlines()
        for ingredient_line in raw_ingredients:
            ingredient_parts = ingredient_line.split(",")  # Assuming ingredients are in 'quantity, name' format
            if len(ingredient_parts) == 2:
                name = ingredient_parts[1].strip()  # Remove extra spaces around name
                quantity = float(ingredient_parts[0].strip())  # Convert quantity to float
                ingredients.append({"name": name, "quantity": quantity})
        
        # Create the recipe dictionary as per the required format
        recipe = {
        "genre": request.form['genre'],
        "name": request.form['name'],
        "ingredients": ingredients,
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
