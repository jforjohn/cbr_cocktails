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
		type = request.form['type']
		name = request.form['cocktailName']
		if type == 'exact_match':
			return render_template(
				'catalog.html',
				ItemList=[],
				cocktailname=name,
				PreparationData=listToStringWithoutBrackets(get_cocktail_preparation(name)),
				IngredientData=listToStringWithoutBrackets(get_cocktail_ingredient(name))
			)
		else:
			score, ingredients = get_adapted_cocktail_info(name)
			f = open("test", "w")
			print(ingredients, file=f)
			return render_template(
				'catalog.html',
				ItemList=[],
				cocktailname=name,
				PreparationData="",
				IngredientData=listToStringWithoutBrackets(ingredients),
				adaptation=1
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
		matched_cocktails_list, cocktail_1, cocktail_2, cocktail_3 = get_recommendation(input_ingredients, preference)

		cocktails = []
		cocktails.append(cocktail_1)
		cocktails.append(cocktail_2)
		cocktails.append(cocktail_3)
		adapted_cocktails_list = []
		for score, cocktail_name, ingredients in cocktails:
			ingredients_list = []
			for ingredient in ingredients.values():
				if ingredient:
					ingredients_list.append(ingredient)
			adapted_cocktails_list.append([cocktail_name, ingredients_list, score])

		cocktails_list = []
		for cocktail_name, ingredients in matched_cocktails_list.items():
			ingredients_list = []
			for ingredient in ingredients.values():
				if ingredient:
					ingredients_list.append(ingredient)
			cocktails_list.append([cocktail_name, ingredients_list])

		f = open("adapt.txt", "w")
		print(adapted_cocktails_list, file=f)
		for cocktail, ingredients, score in adapted_cocktails_list:
			print(cocktail, file=f)
			print(score, file=f)
			for ingredient in ingredients:
				print(ingredient, file=f)

		# cocktail = []
		# with open('output.txt', 'r') as f:
		# 	for line in f.readlines():
		# 		cocktail.append(line.strip().split(','))
		return render_template('prepare.html', matchedcocktail=cocktails_list, adaptedcocktail=adapted_cocktails_list)
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
			f = open("test2", "w")
			print("wrong ingredient", file=f)
			print(request.form['adapt_cingredients'], file=f)
			if recipe != "wrong ingredient":
				print("not wrong ingredient", file=f)
				write_recipe_to_catalog(recipe)
			# return render_template('adapt.html', Saved="Done")
			return render_template('home.html')
		else:
			return render_template(
				'adapt.html',
				name=request.form['adapt_name'],
				PreparationData=listToStringWithoutBracketsAdapted(get_cocktail_preparation(request.form['adapt_name'])),
				IngredientData=listToStringWithoutBracketsAdapted(get_cocktail_ingredient(request.form['adapt_name']))
			)
	else:
		return render_template('adapt.html')


if __name__ == '__main__':
	app.run(debug=True)
