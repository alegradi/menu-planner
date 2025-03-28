import re
from data import CATEGORIES, STOP_WORDS  # Import necessary data


def clean_ingredient_name(raw_name):
    """
    Removes unnecessary descriptive words from ingredient names.
    """
    stop_words_pattern = r'\b(' + '|'.join(re.escape(word) for word in STOP_WORDS) + r')\b'
    cleaned_name = re.sub(stop_words_pattern, '', raw_name, flags=re.IGNORECASE).strip()
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)  # Remove extra spaces
    return cleaned_name

def make_shopping_list(global_menu):
    """
    Generates a sorted shopping list based on recipes in global_menu.
    """
    shopping_dict = {}  # Store ingredient quantities and measurements

    for recipe in global_menu:
        for ingredient in recipe.get("ingredients", []):  # Directly access ingredients
            raw_name = ingredient["name"].lower()
            measurement = ingredient["measurement"]
            quantity = ingredient["quantity"]
            print(raw_name, measurement, quantity)
            cleaned_name = clean_ingredient_name(raw_name)

            # Merge quantities if ingredient already exists
            if cleaned_name in shopping_dict:
                if shopping_dict[cleaned_name]["measurement"] == measurement:
                    shopping_dict[cleaned_name]["quantity"] += quantity
                else:
                    print(f"Warning: Different measurement units for {cleaned_name}")
            else:
                shopping_dict[cleaned_name] = {"quantity": quantity, "measurement": measurement}


    print(shopping_dict)

    # Convert dictionary to list of dictionaries
    extracted_list = [
        {"name": name, "measurement": data["measurement"], "quantity": data["quantity"]}
        for name, data in shopping_dict.items()
    ]

    # Categorisation
    sorted_list = {category: [] for category in CATEGORIES}
    sorted_list["Uncategorised"] = []

    for ingredient in extracted_list:
        found = False
        for category, items in CATEGORIES.items():
            if ingredient["name"] in items:
                sorted_list[category].append(ingredient)
                found = True
                break

        if not found:
            sorted_list["Uncategorised"].append(ingredient)

    return sorted_list



# # For testing
# global_menu = {
#     "recipes": [
#         {
#             "genre": "dessert",
#             "name": "Chocolate Cake",
#             "ingredients": [
#                 {
#                     "quantity": 2,
#                     "measurement": "cups",
#                     "name":"cups flour"
#                 },
#                 {
#                     "quantity": 2,
#                     "measurement": "cups",
#                      "name":"sugar"
#                 },
#                 {
#                     "quantity": 2,
#                     "measurement": "teaspoons",
#                     "name":"baking powder"
#                 },
#                 {
#                     "quantity": 0.75,
#                     "measurement": "cups",
#                     "name":"cocoa powder"
#                 },
#                 {
#                     "quantity": 1.5,
#                     "measurement": "teaspoons",
#                     "name":"baking soda"
#                 },
#                 {
#                     "quantity": 1,
#                     "measurement": "teaspoon",
#                     "name":"salt"
#                 },
#                 {
#                     "quantity": 1,
#                     "measurement": "cup",
#                     "name":"milk"
#                 },
#                 {
#                     "quantity": 0.5,
#                     "measurement": "cup",
#                     "name":"vegetable oil"
#                 },
#                 {
#                     "quantity": 2,
#                     "measurement": "pieces",
#                     "name":"eggs"
#                 },
#                 {
#                     "quantity": 2,
#                     "measurement": "teaspoons",
#                     "name":"vanilla extract"
#                 },
#                 {
#                     "quantity": 1,
#                     "measurement": "cup",
#                     "name":"boiling water"
#                 }
#             ],
#             "instructions": [
#                 "Preheat oven to 350 degrees F (175 degrees C).",
#                 "Grease and flour two 9-inch round baking pans.",
#                 "In a large bowl, stir together the flour, sugar, cocoa, baking powder, baking soda, and salt.",
#                 "Add the milk, vegetable oil, eggs, and vanilla to the flour mixture and mix until well combined.",
#                 "Stir in the boiling water last. The batter will be thin.",
#                 "Pour the batter evenly into the prepared pans.",
#                 "Bake for 30 to 35 minutes, or until a toothpick inserted into the center comes out clean.",
#                 "Cool in the pans for 10 minutes, then remove to a wire rack to cool completely."
#             ]
#         }
#     ]
# }

