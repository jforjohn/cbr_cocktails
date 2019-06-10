from flask import Flask, render_template, request, url_for, redirect
from cocktailList import *

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
		fruits = request.form['fruit']
		vegetables = request.form['vegetable']
		alcoholic = request.form['alcoholicLiqueur']
		nonalcoholic = request.form['nonalcoholicLiqueur']
		enhancers = request.form['tasteEnhancers']
		others = request.form.getlist('others')
		put_cocktails(fruits, vegetables, alcoholic, nonalcoholic, enhancers, others)
		retrieval()
		cocktail = []
		with open('output.txt', 'r') as f:
			for line in f.readlines():
				cocktail.append(line.strip().split(','))
		return render_template('prepare.html', matchedcocktail=cocktail)
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
