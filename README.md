# Menu - Planner

Flask API to create your daily menu and shopping list

## How it works

`weight` in the recipes represents the number of meals a recipe will provide.

## How to run

Create a virtual environment first. The required packages are in the `requirements.txt`.

Local testing and development can be done with running the app first:

```sh
python main.py
```

Now you are able to make requests

```sh
curl http://127.0.0.1:5000/sample
```
Response
```sh
{
  "message": "Hello Flask API world!",
  "status": "success"
}
```