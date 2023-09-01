import logging
logging.basicConfig(level=logging.INFO)

from chemchef.engine import DocumentTable, DocumentSchema, FieldSchema, Exact, Fuzzy

RECIPES = [
    # Lamb jalfrezi
    "Lamb jalfrezi: Marinade the lamb in curry powder and yoghurt. "
    "Fry the lamb with onions, then simmer with some chopped tomatoes.",
    # Paneer jalfrezi
    "Paneer jalfrezi: Saute some onions with curry powder. "
    "Add the paneer cheese and the sliced tomatoes. Cook for 10 minutes.",
    # Lamb cops
    "Lamb chops: Sprinkle salt onto the lamb chops. Grill until brown. Garnish with coriander."
]

RECIPE_SCHEMA = DocumentSchema(fields=[
    FieldSchema(
        field_name='Dish',
        optional=False,
        multivalued=False,
        example_values={'Spaghetti bolognese'}
    ),
    FieldSchema(
        field_name='Ingredients',
        optional=False,
        multivalued=True,
        example_values={'Ginger', 'Lamb', 'Spaghetti'}
    )
])

INGREDIENT_SCHEMA = DocumentSchema(fields=[
    FieldSchema(
        field_name='Ingredient',
        optional=False,
        multivalued=False,
        example_values={'Ginger'}
    ),
    FieldSchema(
        field_name='Vegetarian/Non-vegetarian',
        optional=False,
        multivalued=False,
        allowed_values={'Vegetarian', 'Non-vegetarian'}
    )
])


def main() -> None:
    recipes_table = DocumentTable(
        format_description='Recipe',
        document_schema=RECIPE_SCHEMA,
        subject_field='Dish'
    )

    ingredients_table = DocumentTable(
        format_description='Ingredient factsheet',
        document_schema=INGREDIENT_SCHEMA,
        subject_field='Ingredient'
    )

    # Ingest the recipes into the recipes.
    # For each new ingredient appearing in our recipes, generate an ingredient factsheet
    # and store it in the ingredients table.
    for recipe in RECIPES:
        parsed_recipe_doc = recipes_table.insert(recipe)
        for ingredient_name in parsed_recipe_doc.parsed_data['Ingredients']:
            ingredients_table.auto_insert(ingredient_name)

    # Search for lamb curries
    lamb_curry_recipes_docs = recipes_table.query(Fuzzy(field='Dish', target='Lamb curry'))
    print('Lamb curries with yoghurt: ', lamb_curry_recipes_docs)

    # Search for vegetarian jalfrezis (i.e. jalfrezis where none of the ingredients are non-vegetarian)
    non_vegetarian_ingredient_docs = ingredients_table.query(Fuzzy(field='Vegetarian/Non-vegetarian', target='Non-vegetarian'))

    non_vegetarian_ingredient_names = set()
    for doc in non_vegetarian_ingredient_docs:
        non_vegetarian_ingredient_names.update(doc.parsed_data['Ingredient'])

    vegetarian_jalfrezi_recipe_docs = recipes_table.query(
        Fuzzy(field='Dish', target='Jalfrezi') &
        ~Exact(field='Ingredients', targets=non_vegetarian_ingredient_names)
    )
    print('Vegetarian Jalfrezis: ', vegetarian_jalfrezi_recipe_docs)


if __name__ == '__main__':
    main()
