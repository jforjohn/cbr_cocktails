from flask import Flask, render_template, request, url_for, redirect
from main import *

app = Flask(__name__)


@app.route('/')
def goto():
	return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
	return redirect(url_for('home'))


@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
	if request.method == 'POST':
		return render_template(
			'catalog.html',
			ItemList=[],
			cocktailname=request.form['cocktailName'],
			PreparationData=listToStringWithoutBrackets(get_cocktail_preparation(request.form['cocktailName'])),
			IngredientData=listToStringWithoutBrackets(get_cocktail_ingredient(request.form['cocktailName']))
		)
	else:
		return render_template('catalog.html', ItemList=get_cocktail_list())
		

@app.route('/prepare', methods=['GET', 'POST'])
def prepare():
	if request.method == 'POST':
		fruits = [ingredient.strip() for ingredient in request.form['fruit_input'].split(',')]
		vegetables = [ingredient.strip() for ingredient in request.form['vegetable_input'].split(',')]
		alcoholic = [ingredient.strip() for ingredient in request.form['alcohol_input'].split(',')]
		nonalcoholic = [ingredient.strip() for ingredient in request.form['non_alcohol_input'].split(',')]
		enhancers = [ingredient.strip() for ingredient in request.form['enhancer_input'].split(',')]
		others = [ingredient.strip() for ingredient in request.form['other_input'].split(',')]
		preference = request.form['preferences_input']

		input_ingredients = fruits + vegetables + alcoholic + nonalcoholic + enhancers + others
		input_ingredients = list(filter(None, input_ingredients))

		# put_cocktails()
		# retrieval()
		cocktail_1, cocktail_2 = get_recommendation(input_ingredients, preference)

		cocktails = []
		cocktails.append(cocktail_1)
		cocktails.append(cocktail_2)
		cocktails_list = []
		for score, cocktail_name, ingredients in cocktails:
			ingredients_list = []
			for ingredient in ingredients.values():
				if ingredient:
					ingredients_list.append(ingredient)
			cocktails_list.append([cocktail_name, ingredients_list, score])

		# f = open("test", "w")
		# for similarity, cocktail, ingredients in cocktails:
		# 	print(similarity, file=f)
		# 	print(cocktail, file=f)
		# 	for category, ingredient in ingredients.items():
		# 		print(category, file=f)
		# 		print(ingredient, file=f)

		# cocktail = []
		# with open('output.txt', 'r') as f:
		# 	for line in f.readlines():
		# 		cocktail.append(line.strip().split(','))
		return render_template('prepare.html', matchedcocktail=cocktails_list)
	else:
		return render_template('prepare.html')


@app.route('/adapt', methods=['GET', 'POST'])
def adapt():
	if request.method == 'POST':
		check = request.form['adapt_name']
		if check == 'true':
			recipe = get_adapted_recipe(
				request.form['adapt_cname'],
				request.form['adapt_cingredients'],
				request.form['adapt_cpreparation']
			)
			if recipe != "wrong ingredient":
				write_recipe_to_catalog(recipe)
			return render_template('adapt.html', Saved="Done")
		else:
			return render_template(
				'adapt.html',
				name=request.form['adapt_name'],
				PreparationData=listToStringWithoutBrackets(get_cocktail_preparation(request.form['adapt_name'])),
				IngredientData=listToStringWithoutBrackets(get_cocktail_ingredient(request.form['adapt_name']))
			)
	else:
		return render_template('adapt.html')


if __name__ == '__main__':
	app.run(debug=True)
