"""main.py

Where it all comes together
"""

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from build_menu import build_main_menu
from save_recipe import save_recipe


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
    """
    Default route when visiting /
    Returns:
        Default site
    """
    return render_template('index.html')

@app.route('/sample', methods=['GET'])
def get_data():
    """
    Route when visiting /sample
    Returns:
        Sample response
    """
    return jsonify(sample_data)

@app.route('/menu', methods=['GET'])
def get_menu():
    """
    Route when visiting /menu
    Returns:
        json response of built menu
    """
    built_menu = build_main_menu()
    return jsonify(built_menu)

@app.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Route when visiting /recipes
    Returns:
        HTML response of built menu
    """
    global global_menu    # pylint: disable=global-statement
    global_menu = build_main_menu()
    return render_template('recipes.html', menu=global_menu)

@app.route('/shopping_list')
def make_list():
    """
    Route when visiting /shopping_list
    Returns:
        HTML response of shopping list
    """
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
    shopping_list = [{"name": name, "quantity": quantity} 
                     for name, quantity in shopping_dict.items()]    
    print("Final Shopping List:", shopping_list)
    return render_template("shopping_list.html", shopping_list=shopping_list)
   
def process_webform(webform_text):
    """
    Processes a multi-line string of webform text.
    Args:
        webform_text (str): A string containing items separated by new lines.
    Returns:
        list: A list of cleaned, non-empty webform strings.
    """
    return [webform_text.strip() for webform_text in webform_text.splitlines()
            if webform_text.strip()]

@app.route('/adding', methods=['GET', 'POST'])
def add_recipes():
    """
    Route when visiting /adding
    Returns:
        Save input to existing recipes
    """
    if request.method == 'POST':
        list_ingredients = []

        index = 0
        while f'ingredients[{index}][quantity]' in request.form:
            # Extracting ingredient data
            ingredient_quantity = request.form.get(f'ingredients[{index}][quantity]')
            ingredient_name = request.form.get(f'ingredients[{index}][name]')
            list_ingredients.append({'quantity': ingredient_quantity, 'name': ingredient_name})
            index += 1      
        # Create the recipe dictionary as per the required format
        recipe = {
        "genre": request.form['genre'],
        "name": request.form['name'],
        "ingredients": list_ingredients,
        "cuisine": request.form['cuisine'],
        "weight": int(request.form['weight']),
        "link": request.form['link'],
        "instructions": process_webform(request.form['instructions'])
    }
        save_recipe(recipe)
        return redirect(url_for('successful'))
    return render_template('adding.html')

@app.route('/successful')
def successful():
    """
    Route when visiting /successful
    Returns:
        HTML response when add_recipes() ran correctly
    """
    return render_template('successful.html')


if __name__ == '__main__':
    app.run(debug=True)
