# Imports
import requests
from flask import Flask,render_template, redirect, url_for, request
from flask_scss import Scss


# App Setup
app = Flask(__name__)
Scss(app)



# PreDefined
BASE_URL = 'https://api.freeapi.app/api/v1/public/cats'

#Got this by running a loop and storing each unique characteristic in a list
characters = ['sociable', 'Patient', 'Mischievous', 'Social', 'clever', 'Inquisitive', 'Clever', 'Sensible', 'Interactive', 'Warm', 'Talkative', 'Loyal', 'Peaceful', 'Demanding', 'Trainable', 'Adventurous', 'Gentle', 'Quiet', 'Fun-loving', 'Intelligent', 'Tenacious', 'Independent', 'Agile', 'Easygoing', 'Sociable', 'Relaxed', 'Affectionate', 'Loving', 'Active', 'Lively', 'Calm', 'inquisitive', 'Outgoing', 'Adaptable', 'Sweet-tempered', 'Highly interactive', 'Easy Going', 'Sensitive', 'Energetic', 'Sweet', 'Sedate', 'Devoted', 'playful', 'social', 'loyal', 'Playful', 'Expressive', 'trainable', 'highly intelligent', 'Curious', 'affectionate', 'Friendly', 'Dependent', 'Alert', 'calm', 'Shy']


# Functions
def fetch_cats(url):
    response = requests.get(url).json()
    if response["success"] == True and  response["data"] != None:
        try:
            cat_data = response["data"]["data"]
        except (KeyError):
            cat_data = response["data"]
        return  cat_data

    else:
        raise  Exception("Failed to fetch cats")
def calculate_total_pages(url, limit=12):
    params = {"page": 1, "limit": limit}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return None

    data = response.json()
    if "data" not in data or "totalItems" not in data["data"]:
        print("Unexpected response structure.")
        return None

    total_items = data["data"]["totalItems"]
    total_pages = total_items // limit
    if total_items % limit != 0:
        total_pages += 1

    return total_pages

# Routes
@app.route("/")
def index():
    total_pages = calculate_total_pages(BASE_URL, limit=12)
    url = BASE_URL + "?page=1&limit=12"
    cats = fetch_cats(url)
    return render_template("index.html", cats=cats, characters = characters, total_pages = total_pages, heading = "All Cats")

@app.route("/page/<int:page>")
def nextPage(page):
    total_pages = calculate_total_pages(BASE_URL, limit=12)
    if page is None or page < 1 or page > total_pages:
        return redirect(url_for('nextPage', page=1), code=301)
    url = BASE_URL + f"?page={page}&limit=12"
    cats = fetch_cats(url)

    current_page = page
    return render_template("index.html", cats=cats, characters=characters, current_page=current_page, total_pages=total_pages, heading = "All Cats")

@app.route("/search=<string:word>")
def search(word):
    if word is None:
        return redirect(url_for('nextPage', page=1), code=301)
    word  = word.replace(" ", "+")
    url = BASE_URL + f"?query={word}&page=1&limit=60"
    total_pages = calculate_total_pages(url, limit=12)
    cats = fetch_cats(url)
    word  = word.replace("+", " ")
    return render_template("index.html", cats=cats, characters = characters, total_pages = 0, heading = "\"" +word.title() + "\"" +  " Cat Results")

@app.route("/search", methods = ["POST"])
def inputSearch():
    word = request.form["search"]
    if word:
        return redirect(url_for('search', word = word), code=302)
    else:
        return redirect(url_for('nextPage', page=1), code=301)

@app.route("/id=<int:cat_id>")
def catDetails(cat_id):
    if cat_id is None:
        return redirect(request.referrer or "/")
    if cat_id < 1 or cat_id > 65:
        return redirect(request.referrer or "/")
    url = "https://api.freeapi.app/api/v1/public/cats/" + f"{cat_id}"
    cats = fetch_cats(url)
    return render_template("detail.html", cats=cats, characters = characters, total_pages = 0, heading = cats["name"])


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if  __name__ == "__main__":
    app.run(debug = True)
