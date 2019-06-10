# coding: utf-8

from xml.dom import minidom
from lxml import etree
import os


def get_title_root(title_list, title_value):
	for title in title_list:
		if title.text == title_value:
			title_root = title.getparent()
			return title_root


def get_titles(cocktail_name):
	tree = etree.parse('taxonomy/cocktails.xml')
	root = tree.getroot()
	titles = root.findall('recipe/title')
	title_root = get_title_root(titles, cocktail_name)
	return title_root


def get_cocktail_ingredient(cocktail_name):
	ingredients_list = []
	title_root = get_titles(cocktail_name)
	for node in title_root.getchildren():
			if node.tag == 'ingredients':
				ingredients = node.getchildren()
				for i in ingredients:
					ingredients_list.append(i.text)
	return ingredients_list


def get_cocktail_preparation(cocktail_name):
	preparation_list = []
	title_root = get_titles(cocktail_name)
	for node in title_root.getchildren():
		if node.tag == "preparation":
			ingredients = node.getchildren()
			for i in ingredients:
				preparation_list.append(i.text)
	return preparation_list


def get_cocktail_list():
	xml_doc = minidom.parse('taxonomy/cocktails.xml')
	cocktail_list = [title.childNodes[0].nodeValue for title in xml_doc.getElementsByTagName('title')]
	return sorted(cocktail_list)
	
	
def get_xml_text(parent, node_name):
	node = parent.getElementsByTagName(node_name)[0]
	return "".join([child.toxml() for child in node.childNodes])


def put_cocktails(fruits, vegetables, alcoholic_liqueurs, nonalcoholic_liqueurs, taste_enhancers, others):
	cocktail_list = ",".join(others)
	text_file = open("input.txt", "w")
	text_file.write("fruit:%s" % fruits+'\n')
	text_file.write("vegetables:%s" % vegetables+'\n')
	text_file.write("alcoholicLiqueurs:%s" % alcoholic_liqueurs+'\n')
	text_file.write("nonalcoholicLiqueurs:%s" % nonalcoholic_liqueurs+'\n')
	text_file.write("tasteEnhancers:%s" % taste_enhancers+'\n')
	text_file.write("others:%s" % cocktail_list+'\n')
	text_file.close()


# define a function here to read the input text file and generate the output text file
def xml_parse():
	tree = etree.parse("taxonomy/cocktails.xml")
	root = tree.getroot()
	recipes = []

	list_alcohol = ['white rum','kirsch','Cremant','cognac','champagne','vodka','martini','Noilly_Prat','Whiskey','Benedictine','pastis','rum','malibu rum','dry white wine','Porto','dark rum','White martini','Angostura bitter','pisang ambon','cava','Prosecco','Amber rum','lemon liqueur','sparkling wine','campari','vermouth','Creme de café','triple sec','white wine','red martini','plum brandy','rice wine','calvados','cachaca']

	list_fruits = ['lemon','raspberry','citrus fruit','strawberry','kiwi fruit','orange','apricot','currant/black currant','lime','"lime zest(outer skin of lime)"','blood orange','pineapple apple','grapefruit','banana','litchi','berry','melon']

	list_veggies = ['cucumbers','lime','wasabi','lemongrass','ginger','mint','tomato','coriander','guava']

	list_liqueur = ['Lemonade','Blue curacao','syrup','passion fruit syrup','Orange juice','cointreau','grenadine','pineapple juice','coconut','lime juice','Apricot juice','Creme de cassis','apple juice','grapefruit juice','Hard cider','Cranberry juice','Banana juice','Mango juice','Passion fruit juice','rice milk','coconut milk','Tamarin juice','coffee','apple cider','apricot liqueur','worcestershire sauce','"Currant syrup(blackcurrant juice)"','orgeat syrup','grand marnier','litchi juice','berry juice','strawberry juice','coffee liqueur','coca-cola']

	list_te = ['sugar','cane sugar','sour cream','tabasco sauce','light whipping cream','egg','cinnamon','nutmeg','brown sugar','anise basil','powdered sugar','granulated sugar','vanilla sugar','celery salt','pepper','milk','salt']
	
	list_others = ['ice cube','sparkling water','ice cream','soda water','sparkling mineral water']
	
	# parsing the ingredients out of the xml file and storing them along with the categories
	for i in range(len(root)):
		recipe = []
		recipe.append(root[i][0].text)
		for ingredient in root[i][1]:
			if ingredient.attrib["food"] is None:
				continue
			if ingredient.attrib["food"] in list_alcohol:
				a = 'alcoholicLiqueurs:'+ingredient.attrib["food"]
				recipe.append(a)
				continue
			if ingredient.attrib["food"] in list_fruits:
				a = 'fruit:'+ingredient.attrib["food"]
				recipe.append(a)
				continue
			if ingredient.attrib["food"] in list_veggies:
				a = 'vegetables:'+ingredient.attrib["food"]
				recipe.append(a)
				continue
			if ingredient.attrib["food"] in list_liqueur:
				a = 'nonalcoholicLiqueurs:'+ingredient.attrib["food"]
				recipe.append(a)
				continue
			if ingredient.attrib["food"] in list_te:
				a = 'tasteEnhancers:'+ingredient.attrib["food"]
				recipe.append(a)
				continue
			if ingredient.attrib["food"].lower() in list_others:
				a = 'others:'+ingredient.attrib["food"]
				recipe.append(a)
				continue
		recipes.append(recipe)

	# Writing the parsed ingredients of the recipe into a file
	f = open("cocktail_recipe_lib", "w")

	for r in recipes:
		print(','.join(r), file=f)

	f.close()


def get_similarity_score():
	def file_read(file_path, var):
		file = open(file_path)
		globals()[var] = file.readlines()
		f.close()

	file_read("taxonomy/cocktail_recipe_lib", 'recipes')
	file_read("taxonomy/alcoholicLiqueurs", 'alcoholicLiqueurs')
	file_read("taxonomy/nonalcoholicLiqueurs", 'nonalcoholicLiqueurs')
	file_read("taxonomy/fruit", 'fruit')
	file_read("taxonomy/vegetables", 'vegetables')
	file_read("taxonomy/tasteEnhancers", 'tasteEnhancers')
	file_read("taxonomy/others", 'others')
	file_read("input.txt", 'input')
	d=[]

	# Snippet to generate similarity score based on similarity matrices
	def get_score(ing, cing, itype):
			reference = eval(str(itype))
			for recs in reference:
				recs = recs.strip()
				recs = recs.split(',')
				if (recs[0] == ing and recs[1] == cing) or (recs[0] == cing and recs[1] == ing):
						return recs[2]

	# User input is verified against recipes to find out similar ones
	for recipe in recipes:
		final_score = 0  # Final score for the similarity match of the recipe against user input
		recipe = recipe.strip()
		score = {}
		alcohol_content = 0
		comp_list = recipe.split(',')
		for comps in comp_list:
			try:
				ctype, cing = comps.split(':')
			except ValueError:
				continue
			score[ctype] = 0
			for ingredients in input:
				ingredients = ingredients.strip()
				itype, ing = ingredients.split(":")
				ing_cmp = ing.split(',')
				for sub_ing in ing_cmp:
					if itype == ctype and sub_ing != '':
						# Getting score for similarities of each and every input ingredients
						# against recipes (Only that are in same category)
						scr = get_score(sub_ing, cing, itype)
						if ctype == "alcoholicLiqueurs":
								alcohol_content += 1
						if scr is not None and score[itype] < scr:
							score[ctype] = scr  # Maximum similarity will be retained
		for k, v in score.items():
			# Individual similarity values are added up to get the similarity score between input vs recipe
			final_score += float(v)
		if len(comp_list)-1 > 0:
			rec = comp_list[0], int(final_score/(len(comp_list)-1)*100), alcohol_content
		else:
			rec = comp_list[0], 0, alcohol_content
		d.append(rec)

	# Sort the matches in descending order to find the best set of matches
	e = sorted(d, key=lambda x: float(x[1]), reverse=True)
		
	# Print top 3 matching cases
	if os.path.exists("output.txt"):
		os.remove("output.txt")
	f = open("output.txt", "w")
	for a in e[0:3]:
		if a[2] == 0:
			ac = "Nil"
		elif 0 < a[2] < 3:
			ac = "Moderate"
		else:
			ac = "High"
		f.write(a[0]+","+str(a[1])+"% ,"+ac)
		f.write("\n")
	f.close()


def retrieval():
	xml_parse()
	get_similarity_score()


def write_adapt_details(cName, cIngredient, cPreparation):
	CIngredientList = cIngredient.split(",")
	CPreparationList = cPreparation.split(".")
	text_file = open("adapt.txt", "w")
	text_file.write("<recipe>"+'\n')
	text_file.write("<title>"+cName.strip()+"</title>"+'\n')
	text_file.write("<ingredients>"+'\n')
	for i in CIngredientList:
		text_file.write("<ingredient food="">"+i.strip()+"</ingredient>"+'\n')
	text_file.write("</ingredients>"+'\n')
	text_file.write("<preparation>"+'\n')
	for i in CPreparationList:
		text_file.write("<step>"+i.strip()+"</step>"+'\n')
	text_file.write("</preparation>"+'\n')
	text_file.write("</recipe>"+'\n')
	text_file.close()


def listToStringWithoutBrackets(list1):
	list2 = str(list1).replace('[', '').replace(']', '').replace("}}", '').split("'")
	return [i for i in list2 if len(i) > 2]


def adaptXML():
	f = open("taxonomy/cocktails.xml", "r")
	a = f.readlines()
	f.close()
	a.pop()
	
	g = open("adapt.txt", "r")
	h = g.readlines()
	for i in h:
		a.append(i)

	f = open("taxonomy/cocktails.xml", "w")
	for j in a:
		f.write(j)
	f.write("</recipes>")
