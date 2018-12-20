from src.models.recipes.views import recipe_blueprint
from flask import Flask, render_template, request, redirect, url_for
from src.common.myspark import Myspark
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object('src.config')
app.secret_key = "123"
app.register_blueprint(recipe_blueprint, url_prefix="/recipes")
Myspark.initialize()


@app.before_first_request
def init_model():
    pass


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home.jinja2")
    else:
        return redirect(url_for('recipes.view'), code=307)


app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=5050)
