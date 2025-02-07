"""main.py

Where it all comes together
"""
import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from build_menu import build_main_menu
from save_recipe import save_recipe


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.getenv("FLASK_KEY")

# sample data

sample_data = {
    "message": "Hello Flask API world!",
    "status": "success"
}

global_menu = []

class SearchForm(FlaskForm):
    """
    FlaskForm for /search page, searches a particular recipe
    """
    genre = SelectField('Genre', choices=[('main', 'Main'), ('dessert', 'Dessert')],
                        validators=[DataRequired()])
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class DeleteForm(FlaskForm):
    """
    FlaskForm for /delete page, search and confirm delete a particular recipe
    """
    genre = SelectField('Genre', choices=[('main', 'Main'), ('dessert', 'Dessert')],
                        validators=[DataRequired()])
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    submit = SubmitField('Search')
    delete = SubmitField('Confirm Delete')

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

@app.route('/search', methods=["GET","POST"])
def search_recipe():
    """
    Route when visiting /search
    Returns:
        a search result
    """
    form = SearchForm()
    search_item = None

    if form.validate_on_submit():
        name = form.recipe_name.data
        genre = form.genre.data
        file_path = None
        if genre == "main":
            file_path = 'recipes/main_recipes.json'
        elif genre == "dessert":
            file_path = 'recipes/dessert_recipes.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            recipes = data["recipes"]

        for i in recipes:
            if name.lower() == i["name"].lower():
                search_item = i
                break

        return render_template('search_result.html', recipe=search_item)
    else:
        return render_template('search.html', form=form)

@app.route('/delete', methods=['POST','GET'])
def delete():
    """
    Route when visiting /delete
    Returns:
        delete a certain recipe as requested
    """
    form = DeleteForm()
    recipe_to_delete = None
    # grab user inputs
    if request.method == 'POST':
        name = form.recipe_name.data
        genre = form.genre.data
    # check if the recipe is in main_recipes.json or dessert_recipes.json
        file_path = None
        if genre == "main":
            file_path = 'recipes/main_recipes.json'
        elif genre == "dessert":
            file_path = 'recipes/dessert_recipes.json'
        #check if file_path is correctly assigned
        if not file_path:
            return redirect(url_for('home'))

        # open the file according to the path with read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            recipes = data["recipes"]
        # find a recipe user is looking for
        for i in recipes:
            if name.lower() == i["name"].lower():
                recipe_to_delete = i
                break
        # check if the recipe which user is looking for is in json file
        if not recipe_to_delete:
            flash(f"Recipe '{name}' not found!", "error")
            return redirect(url_for('delete'))

        # If the "Search" button was clicked
        if request.form.get('search') == 'search':
            return render_template('delete.html', form=form,
                                   recipe_to_delete=recipe_to_delete)

        name = recipe_to_delete['name']

        confirm_delete = request.form.get('delete')
        print("Confirm_delete_value:", confirm_delete)
        if confirm_delete == "yes":
            recipes.remove(recipe_to_delete)

            # Save the updated recipes list back to the file (write mode)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump({"recipes": recipes}, file, indent=4)
            # message that the recipe has been deletec
            flash(message=
                  f"Recipe '{recipe_to_delete['name']}' has been successfully deleted.",
                  category="success")
            return redirect(url_for('home'))
        else:
            # this is the page when user searched for a certain recipe after opening /delete
            return render_template('delete.html', form=form,
                                   recipe_to_delete=recipe_to_delete)
    else:
        # this is the page when opening /delete
        return render_template('delete.html',form=form)

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
            print(index, list_ingredients)
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
    with open('recipes/main_recipes.json', 'r', encoding='utf-8') as file:
        file_main_recipes = json.load(file)
        last_item = file_main_recipes["recipes"][-1]
    return render_template('successful.html', recipe=last_item)


if __name__ == '__main__':
    app.run(debug=True)
