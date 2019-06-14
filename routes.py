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

		input_ingredients = fruits + vegetables + alcoholic + nonalcoholic + enhancers + others
		input_ingredients = list(filter(None, input_ingredients))

		# put_cocktails()
		# retrieval()
		cocktails = get_recommendation(input_ingredients)

		cocktails_list = []
		for cocktail_name, ingredients in cocktails.items():
			ingredients_list = []
			for ingredient in ingredients.values():
				if ingredient:
					ingredients_list.append(ingredient)
			cocktails_list.append([cocktail_name, ingredients_list])

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
		check = request.form['AdaptName'] 
		if check == 'true':
			write_adapt_details(
				request.form['AdaptCName'],
				request.form['AdaptCIngredients'],
				request.form['AdaptCPreparation']
			)
			adaptXML()
			return render_template('adapt.html', Saved="Done")
		else:
			return render_template(
				'adapt.html',
				name=request.form['AdaptName'],
				PreparationData=listToStringWithoutBrackets(get_cocktail_preparation(request.form['AdaptName'])),
				IngredientData=listToStringWithoutBrackets(get_cocktail_ingredient(request.form['AdaptName']))
			)
	else:
		return render_template('adapt.html')


if __name__ == '__main__':
	app.run(debug=True)
