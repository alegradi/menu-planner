from flask import Flask, jsonify
import subprocess
from build_menu import build_main_menu

app = Flask(__name__)

# sample data

sample_data = {
    "message": "Hello Flask API world!",
    "status": "success"
}

@app.route('/sample', methods=['GET'])
def get_data():
    return jsonify(sample_data)

@app.route('/menu', methods=['GET'])
def get_menu():
    built_menu = build_main_menu()
    return jsonify(built_menu)

if __name__ == '__main__':
    app.run(debug=True)
