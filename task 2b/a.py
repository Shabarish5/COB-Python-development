from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import json
from datetime import datetime

app = Flask(__name__)

def recipe_search(ingredient):
    api_key = '7a7cd9b85dd6e0d516903b7c2d582bfa'
    application_id = 'a720f909'
    url = 'https://api.edamam.com/search?app_id={}&app_key={}&q={}'.format(application_id, api_key, ingredient)
    result = urllib.request.urlopen(url)
    data = json.load(result)
    return data['hits']

def save_recipe_to_file(ingredient):
    opname = ingredient + '-recipes.txt'
    intifile = "C:\\recipe\\"
    outFileName = intifile + str(opname)
    report = open(outFileName, "w", encoding="utf-8")
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    hits = recipe_search(ingredient)
    report.write("--------------------------------------------Recipe Generated From " + ingredient + "---" + dt + "--------------------------" + '\n')
    report.write('\n')
    for single_hit in hits:
        recipe_json = single_hit['recipe']
        report.write(str(recipe_json['label']) + '\n')
        report.write(str(recipe_json['ingredientLines']) + '\n')
        report.write(str(recipe_json['dietLabels']) + '\n')
        report.write('-' * 150 + '\n')
        report.write('\n')
    report.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        save_recipe_to_file(ingredient)
        hits = recipe_search(ingredient)
        return render_template('index.html', ingredient=ingredient, hits=hits)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
