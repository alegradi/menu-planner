from flask import Flask, jsonify, render_template
import subprocess
from build_menu import build_main_menu
from flask_bootstrap import Bootstrap5
import json


app = Flask(__name__)
Bootstrap5(app)


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
    shopping_list = []
    for recipe in global_menu:
        shopping_list.extend(recipe['ingredients'])
    return render_template('shopping_list.html', shopping_list=shopping_list)


if __name__ == '__main__':
    app.run(debug=True)
