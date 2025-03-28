# config.py
from categories import vegetables, fruits, meats, spices, aisle_products, fridge_freezer

# Define category dictionary
CATEGORIES = {
    "Vegetables": [item.lower() for item in vegetables],
    "Fruits": [item.lower() for item in fruits],
    "Meats": [item.lower() for item in meats],
    "Spices": [item.lower() for item in spices],
    "Pantry & Dry Goods": [item.lower() for item in aisle_products],
    "Fridge & Freezer": [item.lower() for item in fridge_freezer]
}

# Define common stop words
STOP_WORDS = {"see note", "coarsely", "grated","and", "very", "finely",
              "chopped", "sliced", "diced",
              "crushed", "peeled", "shredded", "fresh",
              "ground", "to taste", "optional",
              "well stirred", "juice only", "diced", "chopped",
              "roughly chopped","cut into chunks", "bashed with a rolling pin",
              "to taste", "optional","fat ends", "torn into pieces",
              "if unavailable, use the grated zest of 1 lime",
              "if unavailable, use the zest of 1 lime","to serve",
              "boneless", "skinless"}
