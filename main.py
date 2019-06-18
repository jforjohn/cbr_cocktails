# coding: utf-8

from xml.dom import minidom

from lxml import etree
import numpy as np
import pandas as pd
from os import path
from collections import Counter
from copy import deepcopy
from math import log
from itertools import combinations


class Ingredients:
	list = {
		('liquid', 'alcohol', 'soft', 'bw'): [],
		('liquid', 'alcohol', 'soft'): [],
		('liquid', 'alcohol'): [],
		('liquid', 'juices'): [],
		('liquid', 'juices', 'citric'): [],
		('solid', 'fruits'): [],
		('solid', 'fruits', 'citric'): [],
		('solid', 'veggies'): [],
		('te', 'syrups'): [],
		('te', 'sweet'): [],
		('te',): [],
		('others',): []
	}


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


def get_ingredients_list():
	taxonomy = pd.read_csv('taxonomy.csv', header=0)
	tree = etree.parse('taxonomy/cocktails.xml')
	recipes = tree.findall('recipe')
	titles = []
	all_ingredients = {
		('alco', 'soft', 'bw'): [],
		('alco', 'soft'): [],
		('alco',): [],
		('noalco', 'fruits', 'juices', 'j_sweet'): [],
		('noalco', 'fruits', 'juices', 'j_citric'): [],
		('noalco', 'fruits', 'solid', 's_sweet'): [],
		('noalco', 'fruits', 'solid', 's_citric'): [],
		('noalco', 'veggies'): [],
		('noalco', 'fruits', 'syrups', 'j_sweet'): [],
		('te', 'sweet'): [],
		('te',): [],
		('others',): []
	}
	cocktails = {}
	for recipe in recipes:
		title = recipe[0].text
		titles.append(title)
		ingredients = recipe[1]
		ingredients_list = {
			('alco', 'soft', 'bw'): [],
			('alco', 'soft'): [],
			('alco',): [],
			('noalco', 'fruits', 'juices', 'j_sweet'): [],
			('noalco', 'fruits', 'juices', 'j_citric'): [],
			('noalco', 'fruits', 'solid', 's_sweet'): [],
			('noalco', 'fruits', 'solid', 's_citric'): [],
			('noalco', 'veggies'): [],
			('noalco', 'fruits', 'syrups', 'j_sweet'): [],
			('te', 'sweet'): [],
			('te',): [],
			('others',): []
		}

		for ingredient in ingredients:
			ingredient_val = ingredient.values()[-1].lower()
			# all_ingredients.append(ingredient_val)
			for col in taxonomy.columns:
				col_tup = tuple(col.split('-'))

				if taxonomy[col].isin([ingredient_val]).any():
					ingredients_list[col_tup].append(ingredient_val)
					all_ingredients[col_tup].append(ingredient_val)

		cocktails[title] = ingredients_list

	# globals()['all_ingredients'] = all_ingredients
	# globals()['all_cocktails'] = cocktails

	# f = open("test", "w")
	# for cocktail, ingredients in all_ingredients.items():
	# 	print(cocktail, file=f)
	# 	for category, ingredient in ingredients.items():
	# 		print(category, file=f)
	# 		print(ingredient, file=f)

	return cocktails, all_ingredients


def get_ingredient_taxonomy(ingredient, ingredients_list):
	# f = open("test", "a")
	# print(ingredient, file=f)
	for category, ingredients in ingredients_list.items():
		if ingredient in ingredients:
			return category
	return "none"


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
		file.close()

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
						print(sub_ing)
						print(cing)
						print(itype)
						if ctype == "alcoholicLiqueurs":
							alcohol_content += 1
						if scr is not None and score[itype] < float(scr):
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


# def get_recommendation(input_ingredients):
# 	cocktails_list, ingredients_list = get_ingredients_list()
# 	ingredient_taxonomies = []
# 	for ingredient in input_ingredients:
# 		taxonomy = get_ingredient_taxonomy(ingredient, ingredients_list)
# 		ingredient_taxonomies.append([taxonomy, ingredient])
#
# 	# f = open("test2", "w")
# 	# exact matching
# 	cocktail_list_copy = cocktails_list
# 	for taxonomy, ingredient in ingredient_taxonomies:
# 		for cocktail, ingredients in list(cocktail_list_copy.items()):
# 			found = False
# 			for i in ingredients.values():
# 				if ingredient in i:
# 					found = True
# 			if not found:
# 				del cocktails_list[cocktail]
#
# 	# for cocktail, ingredients in cocktails_list.items():
# 	# 	print(cocktail, file=f)
# 	# 	for category, ingredient in ingredients.items():
# 	# 		print(category, file=f)
# 	# 		print(ingredient, file=f)
#
# 	return cocktails_list


def get_adapted_recipe(name, ingredient, preparation):
	ingredient_list = ingredient.split(",")
	preparation_list = preparation.split(".")
	cocktails, ingredients = get_ingredients_list()

	recipe = ("<recipe>"+'\n')
	recipe += ("<title>"+name.strip()+"</title>"+'\n')
	recipe += ("<ingredients>"+'\n')

	f = open("test", "w")
	for i in ingredient_list:
		food = i.lower().strip().replace('[', '').replace(']', '').replace("}}", '').replace("'", '').split(' ', 1)[1]
		if "of " in food:
			food = food.split('of ', 1)[1]
		taxonomy = get_ingredient_taxonomy(food, ingredients)
		if taxonomy == "none":
			print("wrong ingredient", file=f)
			print(food, file=f)
			print(ingredients, file=f)
			return "wrong ingredient"

		recipe += ("<ingredient food=\""+food+"\">"+i+"</ingredient>"+'\n')
	recipe += ("</ingredients>"+'\n')
	recipe += ("<preparation>"+'\n')

	for i in preparation_list:
		i = i.strip().replace('[', '').replace(']', '').replace("}}", '').replace("'", '').replace("', '", '')
		recipe += ("<step>"+i.strip()+"</step>"+'\n')
	recipe += ("</preparation>"+'\n')
	recipe += ("</recipe>"+'\n')
	return recipe

def listToStringWithoutBracketsAdapted(list1):
	list2 = [i for i in list1 if len(i) > 2]
	list2 = str(list2).replace('[', '').replace(']', '').replace("}", '').split("'")
	text = ""
	for item in list2:
		if len(item) > 2:
			text += item + ", "
	return text.strip()[:-1]

def listToStringWithoutBrackets(list1):
	list2 = str(list1).replace('[', '').replace(']', '').replace("}}", '').split("'")
	return [i for i in list2 if len(i) > 2]


def write_recipe_to_catalog(recipe):
	file = open("taxonomy/cocktails.xml", "r")
	content = file.readlines()

	file = open("taxonomy/cocktails.xml", "w")
	file.writelines([item for item in content[:-1]])
	for j in recipe:
		file.write(j)
	file.write("</recipes>")


def get_adapted_cocktail_info(cocktail_name):
	file = open("adapt.txt", "r")
	content = file.readlines()

	found = False
	score = -1
	ingredients_list = []
	f = open("test2", "w")
	for line in content:
		line = line.rstrip('\n')
		if score >= 0:
			ingredients = line
			print(ingredients, file=f)
			if ingredients[0] != '[':
				break
			ingredients = ingredients[1:-1].replace("'", "").split(",")
			for i in ingredients:
				ingredients_list.append(i)
		if found and score < 0:
			score = float(line)
			print(score, file=f)
		if line == cocktail_name:
			found = True
	return score, ingredients_list


#########################
#########################


def get_recommendation(input_ingredients, preference):
	global df_pmi

	f = open("test2", "w")

	q = {
		('alco', 'soft', 'bw'): [],
		('alco', 'soft'): [],
		('alco',): [],
		('noalco', 'fruits', 'juices', 'j_sweet'): [],
		('noalco', 'fruits', 'juices', 'j_citric'): [],
		('noalco', 'fruits', 'solid', 's_sweet'): [],
		('noalco', 'fruits', 'solid', 's_citric'): [],
		('noalco', 'veggies'): [],
		('noalco', 'fruits', 'syrups', 'j_sweet'): [],
		('te', 'sweet'): [],
		('te',): [],
		('others',): []
	}
	define_globals()
	all_ingredients, cocktails = read_data()
	cocktails_list, ingredients_list = get_ingredients_list()
	ingredient_taxonomies = []
	for ingredient in input_ingredients:
		taxonomy = get_ingredient_taxonomy(ingredient, ingredients_list)
		ingredient_taxonomies.append([taxonomy, ingredient])

	# exact matching
	cocktail_list_copy = cocktails_list
	for taxonomy, ingredient in ingredient_taxonomies:
		for cocktail, ingredients in list(cocktail_list_copy.items()):
			found = False
			for i in ingredients.values():
				if ingredient in i:
					found = True
			if not found:
				del cocktails_list[cocktail]

	for ingredient in input_ingredients:
		taxonomy = get_ingredient_taxonomy(ingredient, ingredients_list)
		print(taxonomy, file=f)
		q[taxonomy].append(ingredient)

	for cocktail, ingredient in q.items():
		print(cocktail, file=f)
		print(ingredient, file=f)

	df_pmi = constract_pmi_table()
	top_n_matches = 3
	sim_match, cocktail_matches = get_matches(q, cocktails, preference, top_n=top_n_matches)
	min_difference, max_score = find_best_adaptation(q, cocktails, cocktail_matches, preference)
	return cocktails_list, min_difference, max_score


def define_globals():
	global taxonomy_scheme
	global all_ingredients
	global df_pmi
	global df_preferences
	global taxonomy_general_cat
	global recipes
	taxonomy_scheme = {
		('alco', 'soft', 'bw'): [],
		('alco', 'soft'): [],
		('alco',): [],
		('noalco', 'fruits', 'juices', 'j_sweet'): [],
		('noalco', 'fruits', 'juices', 'j_citric'): [],
		('noalco', 'fruits', 'solid', 's_sweet'): [],
		('noalco', 'fruits', 'solid', 's_citric'): [],
		('noalco', 'veggies'): [],
		('noalco', 'fruits', 'syrups', 'j_sweet'): [],
		('te', 'sweet'): [],
		('te',): [],
		('others',): []
	}

	taxonomy_general_cat = [
		'alco', 'noalco', 'te', 'others'
	]

	cols = [
		('alco', 'soft', 'bw'),
		('alco', 'soft'),
		('alco',),
		('noalco', 'fruits', 'juices', 'j_sweet'),
		('noalco', 'fruits', 'juices', 'j_citric'),
		('noalco', 'fruits', 'solid', 's_sweet'),
		('noalco', 'fruits', 'solid', 's_citric'),
		('noalco', 'veggies'),
		('noalco', 'fruits', 'syrups', 'j_sweet'),
		('te', 'sweet'),
		('te',),
		('others',)
	]
	idx = ['Alcohol', 'Sweet', 'Sour', 'Fruity', 'Default']
	alco_vals = [0.85, 0.9, 1, 0.7, 0.7, 0.7, 0.7, 0.75, 0.75, 0.7, 0.8, 0.85]
	sweet_vals = [0.9, 0.95, 0.8, 0.85, 0.5, 0.9, 0.65, 0.5, 1, 1, 0.8, 0.8]
	sour_vals = [0.8, 0.6, 0.8, 0.7, 1, 0.75, 1, 0.8, 0.6, 0.6, 0.85, 0.8]
	frutti_vals = [0.85, 0.9, 0.7, 1, 1, 1, 1, 0.7, 0.9, 0.65, 0.7, 0.85]
	default = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	df_preferences = pd.DataFrame(np.array([alco_vals, sweet_vals, sour_vals, frutti_vals, default]),
								  columns=cols, index=idx)


def read_data():
	global recipes
	global all_ingredients
	# read
	taxonomy = pd.read_csv('taxonomy.csv', header=0)
	tree = etree.parse('ccc_cocktails.xml')

	recipes = tree.findall('recipe')
	titles = []
	all_ingredients = []
	cocktails = {}
	for recipe in recipes:
		title = recipe[0].text
		titles.append(title)
		ingredients = recipe[1]
		ingredients_list = deepcopy(taxonomy_scheme)
		for ingredient in ingredients:
			ingredient_val = ingredient.values()[-1].lower()
			all_ingredients.append(ingredient_val)
			for col in taxonomy.columns:
				col_tup = tuple(col.split('-'))

				if taxonomy[col].isin([ingredient_val]).any():
					ingredients_list[col_tup].append(ingredient_val)

		cocktails[title] = ingredients_list
	return all_ingredients, cocktails


def constract_pmi_table():
	unique_ingredients = set(all_ingredients)
	df_pmi = pd.DataFrame(0, columns=unique_ingredients, index=unique_ingredients)
	for recipe in recipes:
		title = recipe[0].text
		ingredients = recipe[1]
		for ingredient_row in ingredients:
			ingredient_val_row = ingredient_row.values()[-1].lower()
			for ingredient_col in ingredients:
				ingredient_val_col = ingredient_col.values()[-1].lower()
				if ingredient_val_row != ingredient_val_col:
					df_pmi.loc[ingredient_val_row, ingredient_val_col] += 1
	return df_pmi


def pmi_score(ingredient1, ingredient2, df_pmi):
	fij = df_pmi.loc[ingredient1, ingredient2]
	fi = df_pmi.loc[ingredient1, :].sum()
	fj = df_pmi.loc[ingredient2, :].sum()
	sum_all = df_pmi.values.sum()
	print('fij', fij)
	print('fifj', fi*fj)
	p = fij/(fi*fj/sum_all)
	'''
	pmi = log(p, 2)
	if pmi < 0:
		pmi = 0
	return pmi, p
	'''
	return p


def get_cocktail_ingredient_list(cocktail):
	ingredient_list = []
	categories_list = []
	for cat in taxonomy_scheme.keys():
		for ingredient in cocktail[cat]:
			categories_list.append(cat)
			ingredient_list.append(ingredient)
	return categories_list, ingredient_list


def get_cocktail_pmi(cocktail, preference=''):
	# cocktail pmi
	catetgory_list, ingridient_list = get_cocktail_ingredient_list(cocktail)
	pmi_score = 0
	c_combos = 0

	for ingredient1_tup, ingredient2_tup in combinations(zip(catetgory_list, ingridient_list), 2):
		ingredient1 = ingredient1_tup[1]
		ingredient2 = ingredient2_tup[1]
		if preference:
			cat1 = ingredient1_tup[0]
			cat2 = ingredient2_tup[0]
			w = (df_preferences[cat1][preference] + df_preferences[cat2][preference]) / 2
		else:
			w = 1
		pmi_score += df_pmi.loc[ingredient1, ingredient2] * w
		c_combos += 1
	return pmi_score / c_combos


def taxonomy_score(ingredient_tup1, ingredient_tup2):
	common_ancestors = set(ingredient_tup1).intersection(set(ingredient_tup2))
	all_ancestors = set(ingredient_tup1).union(set(ingredient_tup2))
	return len(common_ancestors)/len(all_ancestors)


def transform(cocktail):
	categories = list(taxonomy_scheme.keys())
	new_form = {}
	for cat in categories:
		for ingredient in cocktail[cat]:
			ingredient_cat = tuple(list(cat) + [ingredient])
			new_form.setdefault(cat[0], []).append(ingredient_cat)
		if not cocktail[cat]:
			new_form.setdefault(cat[0], [])
	return new_form


def match_cocktails(q_ingredients_list, cocktails, preference='Default'):
	res = {}
	categories = list(taxonomy_scheme.keys())
	for title in cocktails.keys():
		cocktail = cocktails[title]
		cocktail_form = transform(cocktail)
		query_form = transform(q_ingredients_list)
		sim = 0
		for gen_cat in taxonomy_general_cat:
			for q_ingredient_cat in query_form[gen_cat]:
				sim_gen_cat = 0
				c_gen_cat = 0
				# if the same ingredient exists in the cocktail
				# assign a similarity of one and don't investigate further
				if q_ingredient_cat in cocktail_form[gen_cat]:
					sim_gen_cat = 1
					c_gen_cat = 1
				else:
					for d_ingredient_cat in cocktail_form[gen_cat]:
						q_cat = q_ingredient_cat[:-1]
						d_cat = d_ingredient_cat[:-1]
						w = (df_preferences[q_cat][preference] + df_preferences[d_cat][preference])/2
						sim_gen_cat += (taxonomy_score(q_ingredient_cat, d_ingredient_cat) * w)
						c_gen_cat += 1
				if c_gen_cat:
					sim += (sim_gen_cat/c_gen_cat)
		res[title] = (sim, cocktail)
	return res


def get_matches(q, cocktails, preference, top_n=2):
	# matches = exactMatchCocktails(q, cocktails, preference)
	matches = match_cocktails(q, cocktails, preference)
	titles_sort = sorted(matches, key=lambda x: matches[x][0], reverse=True)
	max_val = matches[titles_sort[0]][0]
	final_match = {}
	sim_match = {}
	#top_n = 4
	c_top = 0
	for title in titles_sort:
		if c_top < top_n: #matches[title][0] == max_val or
			final_match[title] = matches[title][1]
			sim_match[title] = matches[title][0]
			c_top += 1
	return sim_match, final_match


def adaptation(cocktails, q_ingredients_list, preference='Default'):
	res = {}
	categories = list(taxonomy_scheme.keys())
	for title in cocktails.keys():
		cocktail = cocktails[title]
		cocktail_form = transform(cocktail)
		query_form = transform(q_ingredients_list)
		sim = 0
		df_dict = {}
		same_ingredients = []
		q_extras = []
		d_extras = []
		cols = set()
		idx = set()
		ingredient2cat = {}
		final_cocktails = []
		final_cocktails_combo = []
		# final_cocktails.append(cocktail)
		for gen_cat in taxonomy_general_cat:
			same_ingredients.extend(list(set(query_form[gen_cat]).intersection(set(cocktail_form[gen_cat]))))
			query_form[gen_cat] = list(set(query_form[gen_cat]) - set(same_ingredients))
			cocktail_form[gen_cat] = list(set(cocktail_form[gen_cat]) - set(same_ingredients))
			if not cocktail_form[gen_cat]:
				q_extras.extend(query_form[gen_cat])
			if not query_form[gen_cat]:
				d_extras.extend(cocktail_form[gen_cat])

			for q_ingredient_cat in query_form[gen_cat]:
				for d_ingredient_cat in cocktail_form[gen_cat]:
					q_cat = q_ingredient_cat[:-1]
					d_cat = d_ingredient_cat[:-1]
					w = (df_preferences[q_cat][preference] + df_preferences[d_cat][preference]) / 2
					sim_gen_cat = taxonomy_score(q_cat, d_cat) * w

					# print(d_ingredient_cat[-1], q_ingredient_cat[-1], sim_gen_cat)
					cols.add(d_ingredient_cat)
					idx.add(q_ingredient_cat)
					ingredient2cat[d_ingredient_cat[-1]] = d_ingredient_cat[:-1]
					ingredient2cat[q_ingredient_cat[-1]] = q_ingredient_cat[:-1]
					df_dict.setdefault(d_ingredient_cat[-1], {})[q_ingredient_cat[-1]] = sim_gen_cat

		df = pd.DataFrame(df_dict)
		# print(df)
		# print('extras', q_extras, d_extras)
		# we change the one in the column with the max in the index
		if df.empty:
			find_replacements = pd.DataFrame([])
		else:
			find_replacements = df.idxmax(axis=1)

		cocktail_add = deepcopy(cocktail)
		cocktail_replace = deepcopy(cocktail)
		for replace_to_ingr in find_replacements.index:
			# print(replace_to_ingr)
			replace_ingr = find_replacements[replace_to_ingr]
			replace_ingr_cat = ingredient2cat[replace_ingr]
			replace_to_ingr_cat = ingredient2cat[replace_to_ingr]

			# add the most similar ingredient
			cocktail_add[replace_to_ingr_cat].append(replace_to_ingr)

			# print(replace_ingr_cat, cocktail_replace[replace_ingr_cat], replace_ingr)
			# if cocktail ingredient had the same sim with another ingredient of the query just add it
			if replace_ingr in cocktail_replace[replace_ingr_cat]:
				cocktail_replace[replace_ingr_cat].remove(replace_ingr)
			cocktail_replace[replace_to_ingr_cat].append(replace_to_ingr)

		final_cocktails.append(cocktail_add)
		final_cocktails.append(cocktail_replace)
		# pprint(final_cocktails)
		final_cocktails_combo = []
		for final_cocktail in final_cocktails:
			for q_extra in q_extras:
				cat = q_extra[:-1]
				ingredient = q_extra[-1]
				final_cocktail[cat].append(ingredient)

			for ind in range(1, len(d_extras) + 1):
				for combo in combinations(d_extras, ind):
					tmp_cocktail = deepcopy(final_cocktail)
					# print('combo', combo)
					for d_extra in combo:
						cat = d_extra[:-1]
						ingredient = d_extra[-1]
						tmp_cocktail[cat].remove(ingredient)
					final_cocktails_combo.append(tmp_cocktail)
		final_cocktails.extend(final_cocktails_combo)
		res[title] = final_cocktails
	return res


def find_best_adaptation(q, cocktails, cocktail_matches, preference='Default'):
	final_cocktails = adaptation(cocktail_matches, q, preference)
	scores_max = []
	scores_diff = []
	for title in final_cocktails:
		adapt_cocktails = final_cocktails[title]
		cocktail_pmi = get_cocktail_pmi(cocktails[title])
		adapt_cocktail_pmi_lst = np.array([])
		for cocktail in adapt_cocktails:
			adapt_cocktail_pmi = get_cocktail_pmi(cocktail, preference=preference)
			adapt_cocktail_pmi_lst = np.append(adapt_cocktail_pmi_lst, adapt_cocktail_pmi)
		diff = np.absolute(adapt_cocktail_pmi_lst - cocktail_pmi)
		min_ind = diff.argmin()
		max_ind = adapt_cocktail_pmi_lst.argmax()
		scores_diff.append((diff[min_ind], title, adapt_cocktails[min_ind]))
		scores_max.append((diff[max_ind], title, adapt_cocktails[max_ind]))

	return min(scores_diff), max(scores_max)
