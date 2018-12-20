from src.models.recipes.constants import CUISINES
from flask import request, render_template, Blueprint
from src.models.recipes.recipe import Recipe
from src.common.myspark import Myspark

recipe_blueprint = Blueprint('recipes', __name__)


@recipe_blueprint.route('/view', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        ingredients = request.form['Ingredients']
        test = Myspark.create_df_by_ingred(ingredients)
        test_vector = Myspark.PPL.transform(test)
        prediction = Myspark.LR.transform(test_vector['id', 'features'])
        label = prediction.collect()[0]['prediction']

        recipe = Recipe(ingredients, CUISINES[int(label)], CUISINES[int(label)]+'.jpg')
        recipe.get_by_cuisine()
        return render_template("recipes/view_recipes.jinja2", recipe=recipe)

    return render_template("home.jinja2")
