import json
from requests import get

from flask import Flask, render_template, url_for, request, jsonify, current_app
from flask_bootstrap import Bootstrap

from config import app_config

app = Flask(__name__)
app.config.from_object(app_config['development'])
Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/process',methods= ['POST'])
def process():
    firstName = request.form['firstName'].strip()
    lastName = request.form['lastName'].strip()
    if firstName and lastName:
        output = firstName + " " + lastName
    else:
        output = firstName + lastName
    if firstName and lastName:
        return jsonify({'output':'Full Name: ' + output})
    return jsonify({'output' : 'Error : Missing data!'})

def make_api_request(url):
    try:
        resp = get(url).json()
        if not resp['list'] or not resp['list']['item']:
            return None
        return resp
    except Exception:
        return None

def get_food_groups(food_data):
    ''' Unique list of food groups in food_data '''
    gs = [g['group'] for g in food_data['list']['item']]
    return sorted(list(set(gs)))

def get_food_manufacturers(food_data):
    ''' create a list of unique manufacturers from the food_data dictionary '''
    mfg = [item['manu'] for item in food_data['list']['item']]
    return sorted(list(set(mfg)))

def save_food_search(results):
    # Save JSON results to a file
    with open("food_search_results.json", "w") as food_results_file:
        json.dump(results, food_results_file, indent=4)


@app.route('/lookup', methods=['POST'])
def lookup():
    # get data from form
    searchText =  request.form['searchText'].strip()
        
    if searchText:
        api_key = app.config['USDA_API_KEY']
        food_list = [food.strip() for food in searchText.split(',')]
        results = {}
        for food in food_list:
            url = f"https://api.nal.usda.gov/ndb/search/?format=json&q={food}&sort=n&max=25&offset=0&api_key={api_key}"
            items = make_api_request(url)
            food_groups = get_food_groups(items)
            manufacturers = get_food_manufacturers(items)
            results[food] = dict({'food_groups':food_groups, 'manufacturers': manufacturers, 'items': items})
        return jsonify({'results': results, 'food_list': food_list})
        # save the results of the search
        save_food_search(results)
    return jsonify({'error': "Your search did not yield any results. Try again."})